#! /usr/bin/bash

PROGRESS_FILE="./progress/secure_boot.log"
# Progress Milestones
#  0: Initial state, no progress made.
#  1: User has been prompted to enter BIOS and pressed Enter
#  2: Keys created
#  3: Keys enrolled
#  4: Setup Mode disabled
#  5: Wallpaper file hashed
#  6: Enrolled config checksum
#  7: Secure boot enabled
#  8: fwupd allowed
#  9: Done


## Utils ##
status() {
    local checking=$1
    local status=$(sudo sbctl status &>/dev/null)
    
    local ENABLED_SETUP="Setup Mode:     ✗ Enabled"
    local DISABLED_SETUP="Setup Mode:     ✗ Disabled"
    local DISABLED_POST_SETUP="Setup Mode:     ✓ Disabled" #

    local ENABLED_SECUREBOOT="Secure Boot:    ✓ Enabled"
    local DISABLED_SECUREBOOT="Secure Boot:    ✗ Disabled"

    local ENABLED_KEYS="Vendor Keys:    ✓ Enrolled"
    local DISABLED_KEYS="Vendor Keys:    none"

    if [[ "$checking" == "setupmode" ]]; then
        if [[ "$status" == *"$ENABLED_SETUP"* ]]; then
            echo "enabled"

        elif [[ "$status" == *"$DISABLED_POST_SETUP"* ]]; then
            echo "complete"

        elif [[ "$status" == *"$DISABLED_SETUP"* ]]; then
            echo "disabled"

        else
            echo "Setup mode is not enabled!"
        fi

    elif [[ "$checking" == "secureboot" ]]; then
        if [[ "$status" == *"$ENABLED_SECUREBOOT"* ]]; then
            echo 0
        else
            echo "Secure Boot is not enabled!"
        fi

    elif [[ "$checking" == "keys" ]]; then
        if [[ "$status" == *"$ENABLED_KEYS"* ]]; then
            echo 0
        else
            echo "No keys registered!"
        fi

    else
        echo "Invalid argument: $checking. Use 'setupmode' or 'secureboot'."
        exit 1
    fi
}

progress() {
    cat "$PROGRESS_FILE"
}

keys_state() {
    local ENABLED_KEYS="Vendor Keys:    ✓ Enrolled"
    local NONE_KEYS="Vendor Keys:    none"
    local PENDING_KEYS="Vendor Keys:    microsoft"
    status=$(sudo sbctl status &>/dev/null)
    if [[ "$status" -eq *"$ENABLED_KEYS"* ]]; then
        echo "enabled"
    elif [[ "$status" -eq *"$NONE_KEYS"* ]]; then
        echo "none"
    elif [[ "$status" -eq *"$PENDING_KEYS"* ]]; then
        echo "pending"
    fi

}

check_files() {
    if [[ ! -d "./progress" ]]; then
        mkdir -p ./progress
    fi

    if [[ ! -f "$PROGRESS_FILE" ]]; then
        touch "./progress/secure_boot.log"
        echo "0" > "$PROGRESS_FILE"
    fi
}

setup_enabled() {
    status=$(status "setupmode")
    echo "Checking if Setup Mode is enabled..."
    if [[ "$status" == "complete" ]] || [[ "$status" == "enabled" ]]; then
        echo 0
    else
        echo 1
    fi
}



## Actions ##
install_sbctl() {
    sbctlInstalled=$(yay -Q sbctl &>/dev/null)
    if [[ $? -ne 0 ]]; then
        echo "Installing sbctl..."
        yay -S sbctl --noconfirm
    fi
}

enroll_keys() {
    enroll=$(sudo sbctl enroll-keys --microsoft --firmware-builtin &>/dev/null)
    status=$(status "setupmode")
    if [[ $status -eq 1 ]]; then
        echo "Keys enrolled successfully!"
    else
        echo "$status"
        exit 1
    fi
}

create_keys() {
    sudo rm -rf /var/lib/sbctl # Clear any previously stored keys and stuff
    create=$(sudo sbctl create-keys)
    if [[ "$create" == *"Secure boot keys created!"* ]]; then
        echo "Keys created successfully!"
        echo 2 > $PROGRESS_FILE
    elif [[ "$create" == *"Secure boot keys have already been created!"* ]]; then
        echo "We already made keys!"
        echo 2 > $PROGRESS_FILE

    else
        echo "$create"
        exit 1
    fi
}

wallpaper_hash() {
    echo ""
}




## Stages ##
stage_0() {
    product=$(sudo dmidecode -t 2 | grep "Product Name:"  &>/dev/null)
    model="${product#*Product Name:}"

    printf "\nEnter the BIOS to:\n"
    printf "  1. Put Secure Boot into Setup Mode\n"
    printf "  2. Set to the default keys.\n"
    printf "\n"
    printf "After 'Save & Exit', the script will run itself again after logging in.\n"
    printf "\n\e[34m" # Blue
    printf "If unsure, you can search:$model secure boot setup mode\n"
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
    printf "   3. Select \e[4mCompatability\e[0m\e[34m -> \e[4mMaximum Security\e[0m\e[34m.\n"
    printf "   4. Go to \e[4mKey Management\e[0m\e[34m\n"
    printf "   5. Select \e[4mEnroll all Factory Default keys\e[0m\e[34m -> \e[4mDisabled\e[0m\e[34m\n"
    printf "   6. Select \e[4mDelete all Secure Boot variables\e[0m\e[34m\n"
    

    printf "\e[0m\n\n" # End colors
    read -p "Press Enter to reboot the computer directly into the BIOS..."
    printf "1" > "$PROGRESS_FILE"
    # systemctl reboot --firmware-setup
}

stage_1() {
    echo "stage1"
    clear
    if [[ $(progress) -eq 1 ]]; then
        printf "Hi again. Password need typie.\n\n"
        read -r -p "Press Enter when you're ready..."
    fi

    if [[ $(setup_enabled) -eq 1 ]]; then
        stage_0
    fi

    echo "Creating keys..."
    create_keys

    echo "Enrolling keys..."
    enroll_keys

    echo "Checking if Setup Mode is complete..."
    setup=$(status "setupmode")
    if [[ "$setup" == "complete" ]]; then
        echo "Setup mode is done!"
        echo 2 > "$PROGRESS_FILE"
    else
        echo "$setup"
        exit 1
    fi
}

stage_2() {
    echo "stage 2"
}






if [[ $(progress) == 0 ]]; then
    clear
    check_files
    install_sbctl
    stage_0
fi

if [[ $(progress) == 1 ]]; then
    clear
    if [[ $(setup_enabled) == 1 ]]; then
        stage_0
        exit 1
    fi
    stage_1
fi

if [[ $(progress) == 2 ]]; then
    if [[ $(setup_enabled) == 1 ]]; then
        stage_0
        exit 1
    fi
    stage_2
fi

if [[ $(progress) == 3 ]]; then
    stage_3
fi

exit 0


echo "Searching for wallpaper path in limine.conf..."
ENABLE_ENROLL_LIMINE_CONFIG=yes >> /etc/default/limine
wallpaper=$(sudo cat /boot/limine.conf | grep "wallpaper: boot():/")
if [[ "$wallpaper" == *"boot():/"* ]]; then
    path=${wallpaper#*boot():/}
    echo "Wallpaper found: ${path}"
elif [[ -z "$wallpaper" ]]; then
    echo "No wallpaper found in limine.conf"
    exit 1
else
    echo "Unexpected wallpaper path in limine.conf: $wallpaper"
    exit 1
fi

echo "Generating BLAKE2B hash for the splash image..."
hash=$(sudo b2sum /boot/${path})
if [[ ${#hash} -ne 64 ]]; then
    echo "Error generating BLAKE2B hash for the splash image"
    exit 1
fi

echo "Adding the hash to wallpaper path in limine.conf..."
hashPath="boot():/${path}#${hash}"
sudo sed -i "s|wallpaper: boot():/.*|${hashPath}|" /boot/limine.conf
if [[ $? -ne 0 ]]; then
    echo "Error updating limine.conf with the new wallpaper path"
    exit 1
fi 

echo "Enrolling the config checksum and signing Limine’s EFI binary..."
sudo limine-enroll-config
sudo limine-update

echo "Checking if Secure Boot is enabled..."
status=$(is_enabled "secureboot")
if [[ "$status" -eq 0 ]]; then
    echo "Secure Boot is enabled!"
else
    echo "Unexpected sbctl status:"
    echo "$status"
    exit 1
fi 

# Allowing for fwupd to work with Secure Boot by signing the fwupdx64.efi binary and updating the fwupd configuration.
sudo sbctl sign -s -o /usr/lib/fwupd/efi/fwupdx64.efi.signed /usr/lib/fwupd/efi/fwupdx64.efi
"\n[uefi_capsule]\nDisableShimForSecureBoot=true" >> /etc/fwupd/fwupd.conf


echo "Secure Boot is setup successfully!"
exit 0






