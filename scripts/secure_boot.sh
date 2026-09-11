#! /bin/bash

PROGRESS_FILE="./tmp/secure_boot.log"

status() {
    local checking="$1"
    
    local ENABLED_SETUP="Setup Mode:     ✗ Enabled"
    local DISABLED_SETUP="Setup Mode:     ✗ Disabled"
    local COMPLETE_SETUP="Setup Mode:     ✓ Disabled"

    local ENABLED_SECUREBOOT="Secure Boot:    ✓ Enabled"
    # local DISABLED_SECUREBOOT="Secure Boot:    ✗ Disabled"

    local ENABLED_KEYS="Vendor Keys:    microsoft"
    # local DISABLED_KEYS="Vendor Keys:    none"

    status=$(sudo sbctl status &>/dev/null)
    echo "$1"
    if [[ "$checking" == "setupmode" ]]; then
        if [[ "$status" == *"$ENABLED_SETUP"* ]]; then
            echo "enabled"

        elif [[ "$status" == *"$COMPLETE_SETUP"* ]]; then
            echo "complete"

        elif [[ "$status" == *"$DISABLED_SETUP"* ]]; then
            echo "disabled"
        fi
        
    elif [[ "$checking" == "secureboot" ]]; then
        if [[ "$status" == *"$ENABLED_SECUREBOOT"* ]]; then
            echo "enabled"
        else
            echo "disabled"
        fi
        
    elif [[ "$checking" == "keys" ]]; then
        if [[ "$status" == *"$ENABLED_KEYS"* ]]; then
            echo "enrolled"
        
        elif [[ "$status" == *"Owner GUID"* ]]; then
            echo "created"

        else
            echo "none"
        fi
        
    else
        echo "Invalid argument: $checking. Use 'setupmode' or 'secureboot'."
        exit 1
    fi
}

stage() {
    cat $PROGRESS_FILE 2>/dev/null
}

print_err() {
    printf '\e[31m%s\e[0m' "$1"
}

installpkg() {
    local pkg=$1
    echo sudo pacman -Sy "$pkg" --noconfirm --nodeps
}

is_installed() {
    local pkg=$1
    sudo pacman -Q "$pkg" &>/dev/null
}

#############################
##    Enrollment Utils     ##
#############################

setup_enabled() {
    status=$(status "setupmode")
    echo "Checking if Setup Mode is enabled..."
    if [[ "$status" == "complete" ]] || [[ "$status" == "enabled" ]]; then
        return 0
    else
        return 1
    fi
}

create_keys() {
    sudo rm -rf /var/lib/sbctl # Clear any previously stored keys and stuff
    create=$(sudo sbctl create-keys)
    if [[ "$create" == *"Secure boot keys created!"* ]]; then
        echo "Keys created successfully!"
    else
        echo "$create"
        exit 1
    fi
}

enroll_keys() {
    if ! sudo sbctl enroll-keys --microsoft --firmware-builtin; then
        echo "Failed to enroll keys!"
        exit 1
    fi

    status=$(status "setupmode")
    if [[ "$status" == "complete" ]]; then
        echo "Keys enrolled successfully!"
    else
        echo "$status"
        exit 1
    fi
}

blake2b_hash() {
    local path=$1
    hash=$(sudo b2sum "/boot/${path}" 2>/dev/null)
    if [[ ! ${#hash} == 64 ]]; then
        echo "Error generating BLAKE2B hash for the splash image"
        exit 1
    fi
    echo "$hash"
    
}

write_wallpaper_hash() {
    local path=$1
    echo "Adding the hash to wallpaper path in limine.conf..."
    hash=$(blake2b_hash "$path")
    hashPath="${path}#${hash}"
    if ! sudo sed -i "s|wallpaper: boot():/.*|${hashPath}|" /boot/limine.conf; then
        printf "Error updating limine.conf with the new wallpaper path"
        exit 1
    else
        echo "Written successfully"
    fi 
}

###################
##    Prompts    ##
###################

enable_secure_boot_reboot() {
    clear
    printf "\nOkay, this is the last part for secure boot!\n\n"
    printf "Once the PC restarts, you will enter the BIOS.\n"
    printf "In there, go set Secure Boot to Enabled\n"
    printf "Then, once you come back, we'll see if everything worked.\n\n"
    read -r -p "Press Enter to reboot and enter BIOS..."
}

enable_setup_mode_reboot() {
    clear
    product=$(sudo dmidecode -t 2 | grep "Product Name:"  &>/dev/null)
    model="${product#*Product Name:}"

    printf "\nEnter the BIOS to:\n"
    printf "  1. Put Secure Boot into Setup Mode\n"
    printf "  2. Set to the default keys.\n"
    printf "\n"
    printf "After 'Save & Exit', the script will run itself again after logging in.\n"
    printf "\n\e[34m" # Blue
    printf "If unsure, you can search:%s secure boot setup mode\n" "$model"
    printf "\n"
    printf "Note: If you do not see any options for Secure Boot, you may need to enable the 'Advanced Mode' in the BIOS first.\n"
    printf "\e[35m\n" # Magenta
    printf "If you have an ASUS or MSI motherboard, please follow these instructions:\n"
    printf "\t\t\tI recommend taking a photo...\n"
    printf "\e[34m" # Blue
    printf "  ASUS:\n"
    printf "   1. Navigate to \e[4mBoot\e[0m\e[34m -> \e[4mSecure Boot\e[0m\e[34m\n"
    printf "   2. Set \e[4mSecure Boot Mode\e[0m\e[34m to \e[4mCustom\e[0m\e[34m\n"
    printf "   3. Open \e[4mKey Management\e[0m\e[34m -> \e[4mDelete all Secure Boot Variables\e[0m\e[34m\n"
    printf "\n"
    printf "  MSI:\n"
    printf "   1. Navigate to \e[4mSettings\e[0m\e[34m -> \e[4mSecurity\e[0m\e[34m -> \e[4mSecure Boot\e[0m\e[34m\n"
    printf "   2. Set \e[4mSecure Boot Mode\e[0m\e[34m to \e[4mCustom\e[0m\e[34m\n"
    printf "   3. Select \e[4mCompatibility\e[0m\e[34m -> \e[4mMaximum Security\e[0m\e[34m.\n"
    printf "   4. Go to \e[4mKey Management\e[0m\e[34m\n"
    printf "   5. Select \e[4mEnroll all Factory Default keys\e[0m\e[34m -> \e[4mDisabled\e[0m\e[34m\n"
    printf "   6. Select \e[4mDelete all Secure Boot variables\e[0m\e[34m\n"
    

    printf "\e[0m\n\n" # End colors
    read -r -p "Press Enter to reboot the computer directly into the BIOS..."
}

########################################
##     Check if completed already     ##
########################################

if [[ $(status "secureboot") == "enabled" ]]; then
    echo "Secure boot is already enabled!"
    exit 1
fi

########################################
##          Create log file           ##
########################################

if [[ ! -d './tmp' ]]; then
    mkdir ./tmp
fi

if [[ ! -f $PROGRESS_FILE ]]; then
    touch $PROGRESS_FILE
    echo 0 > $PROGRESS_FILE
fi


##################################
##      Enable Setup Mode       ##
##################################

if [[ $(stage) == 0 ]]; then
    clear
    if ! is_installed sbctl; then
        echo "Installing sbctl..."
        installpkg sbctl
    fi

    if [[ ! -f $PROGRESS_FILE ]]; then
        touch $PROGRESS_FILE
        echo "0" > $PROGRESS_FILE
    fi
    
    enable_setup_mode_reboot
    printf 1 > $PROGRESS_FILE
    # systemctl reboot --firmware-setup
    exit 0
fi

##################################
##     Create & Enroll Keys     ##
##################################

if [[ $(stage) == 1 ]]; then
    clear
    if [[ ! $(setup_enabled) ]]; then
        enable_setup_mode_reboot
    fi

    clear
    if [[ $(stage) == 1 ]]; then
        printf "Hi again. Password need typie.\n\n"
        read -r -p "Press Enter when you're ready..."
        clear
    fi

    if [[ $(status keys) == 'none' ]]; then
        echo "Creating keys..."
        create_keys
    fi

    if [[ ! $(status keys) == 'enrolled' ]]; then
        echo "Enrolling keys..."
        enroll_keys
    fi

    echo "Checking if Setup Mode is complete..."
    setup=$(status "setupmode")
    if [[ "$setup" == "complete" ]]; then
        echo "Setup mode is done!"
        echo 2 > "$PROGRESS_FILE"
    else
        print_err "$setup"
        exit 1
    fi
    echo 2 > $PROGRESS_FILE
fi

##################################
##  Enroll config and binaries  ##
##################################

if [[ $(stage) == 2 ]]; then
    mode=$(status "setupmode")
    if [[ ! "$mode" == "complete" ]]; then
        print_err "Setup Mode should be completed by now..."
        exit 1
    fi

    printf "\nEnrolling the config checksum and signing Limine's EFI binary...\n"
    sudo limine-enroll-config
    sudo limine-update
    echo 3 > $PROGRESS_FILE

    enable_secure_boot_reboot
    exit 0
fi

##################################
##      Check Secure Boot       ##
##################################

if [[ $(stage) == 3 ]]; then
    echo "Checking if Secure Boot is enabled..."
    status=$(status "secureboot")
    if [[ "$status" == "enabled" ]]; then
        echo "Secure Boot is enabled!"
    else
        enable_secure_boot_reboot
        # systemctl reboot --firmware-setup
        exit 0 # DEV
    fi 

    # Allowing for fwupd to work with Secure Boot by signing the fwupdx64.efi binary and updating the fwupd configuration.
    echo "Signing the fwupdx64.efi binary and updating the fwupd configuration..."
    if [[ ! $(sudo sbctl sign -s -o /usr/lib/fwupd/efi/fwupdx64.efi.signed /usr/lib/fwupd/efi/fwupdx64.efi
        "\n[uefi_capsule]\nDisableShimForSecureBoot=true" >> /etc/fwupd/fwupd.conf) ]]; then
        print_err "Something went wrong when allowing fwupd"
        exit 1
    fi

    echo "Secure Boot is setup successfully!"
    exit 0
fi


















