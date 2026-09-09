is_enabled() {
    local checking=$1
    local status=$(sudo sbctl status)
    
    local ENABLED_SETUP="Setup Mode:     ✗ Enabled"
    local DISABLED_SETUP="Setup Mode:     ✓ Disabled" # OK?

    local ENABLED_SECUREBOOT="Secure Boot:    ✓ Enabled"
    local DISABLED_SECUREBOOT="Secure Boot:    ✗ Disabled"

    local ENABLED_KEYS="Vendor Keys:    ✓ Enrolled"
    local DISABLED_KEYS="Vendor Keys:    none"

    if [[ "$checking" == "setupmode" ]]; then
        if [[ "$status" == *"$ENABLED_SETUP"* ]]; then
            echo 0
        else
            echo 1
        fi

    elif [[ "$checking" == "secureboot" ]]; then
        if [[ "$status" == *"$ENABLED_SECUREBOOT"* ]]; then
            echo 0
        else
            echo 1
        fi

    elif [[ "$checking" == "keys" ]]; then
        if [[ "$status" == *"$ENABLED_KEYS"* ]]; then
            echo 0
        else
            echo 1
        fi

    else
        echo "Invalid argument: $checking. Use 'setupmode' or 'secureboot'."
        exit 1
    fi
}

progress() {
    echo $(cat "./progress/secure_boot.log" 2>/dev/null)
}

check_keys() {
    if [[ $(sudo sbctl status) == *"Vendor Keys:"* ]] && [[ ! $(sudo sbctl status) == *"none"* ]]; then
        echo "No keys found!\nCreating keys..."
        create=$(sudo sbctl create-keys)
        if [["$create" == *"Secure boot keys created!"* ]]; then
            echo "Keys created successfully!"
        else
            echo "Unexpected sbctl create-keys output:"
            echo "$create"
            exit 1
        fi
    else
        echo "Keys already exist. Please clear existing keys before proceeding."
        exit 1
    fi
}

prompt_bios() {
    product=$(sudo dmidecode -t 2 | grep "Product Name:")
    model="${product#*Product Name:}"
    clear
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
    printf "1" > "./progress/secure_boot.log"
    # systemctl reboot --firmware-setup
}

resize -s 100 10
# Progress milestones:
# 0: Initial state, no progress made.
# 1: User has been prompted to enter BIOS and pressed Enter
# 2: User has entered BIOS and set Setup Mode

if [[ ! -d "./tmp" ]]; then
    mkdir -p ./tmp
fi

if [[ ! -f "$PROGRESS_FILE" ]]; then
    touch "./progress/secure_boot.log"
    echo "0" > "$PROGRESS_FILE"
fi

sbctlInstalled=$(yay -Q sbctl 2>/dev/null)
if [[ $? -ne 0 ]]; then
    echo "Installing sbctl..."
    yay -S sbctl --noconfirm
fi

if [[ ! -f "$PROGRESS_FILE" ]]; then
    echo "Creating progress file..."
    echo "0" > "$PROGRESS_FILE"
fi

## Enter BIOS ##
if [[ $(progress) -eq 0 ]]; then
    prompt_bios
fi


echo "Checking if Setup Mode is enabled..."
status=$(is_enabled "setupmode")
if [[ "$status" -eq 0 ]]; then
    echo "Setup mode is enabled!"
    exit 0
else
    echo "Unexpected sbctl status:"
    echo "$status"
    exit 1
fi

exit 0

echo "Checking for keys..."
if [[ $(sudo sbctl status) == *"Vendor Keys:"* ]] && [[ ! $(sudo sbctl status) == *"none"* ]]; then
    echo "No keys found!\nCreating keys..."
    create=$(sudo sbctl create-keys)
    if [["$create" == *"Secure boot keys created!"* ]]; then
        echo "Keys created successfully!"
    else
        echo "Unexpected sbctl create-keys output:"
        echo "$create"
        exit 1
    fi
else
    echo "Keys already exist. Please clear existing keys before proceeding."
    exit 1
fi

echo "Enrolling keys..."
enroll=$(sudo sbctl enroll-keys --microsoft --firmware-builtin)
if [["$enroll" == *"Enrolled keys to the EFI variables!"* ]]; then
    echo "Keys enrolled successfully!"
else
    echo "Unexpected sbctl enroll-keys output:"
    echo "$enroll"
    exit 1

echo "Checking for Keys status..."
status=$(is_enabled "keys")
if [["$status" == 0]]; then
    echo "Keys enrolled successfully!"
else
    echo "Unexpected sbctl status:"
    echo "$status"
    exit 1
fi

echo "Checking if Setup Mode is disabled..."
status=$(is_enabled "setupmode")
if [[ "$status" -eq 1 ]]; then
    echo "Setup mode is disabled!"
else
    echo "Unexpected sbctl status:"
    echo "$status"
    exit 1
fi

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






