is_enabled() {
    local checking=$1
    status=$(sudo sbctl status)

    if [[ "$checking" == "setupmode" ]]; then
        if [[ "$status" == *"Enabled"* ]]; then
            echo 0
        else
            echo 1
        fi

    elif [[ "$checking" == "secureboot" ]]; then
        if [[ "$status" == *"Enabled"* ]]; then
            echo 0
        else
            echo 1
        fi

    elif [[ "$checking" == "keys" ]]; then
        if [[ "$status" == *"Vendor Keys:"* ]]; then
            echo 0
        else
            echo 1
        fi

    else
        echo "Invalid argument: $checking. Use 'setupmode' or 'secureboot'."
        exit 1
    fi
}

yay -S sbctl --noconfirm

if [[ $(grub-install --version) == 0 ]]; then
    sudo grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=cachyos --modules="tpm" --disable-shim-lock
fi

## Enter BIOS ##
# TODO: add warning 
systemctl reboot --firmware-setup

# TODO: instructions
# Next steps in BIOS (if prompted to reset, select No):
#   1. Set Setup mode 
#   2. Clear keys/variables
#   3. Save and exit
#   4. Use boot override to boot into CachyOS


echo "Checking if Setup Mode is enabled..."
status=$(is_enabled "setupmode")
if [[ "$status" -eq 0 ]]; then
    echo "Setup mode is enabled!"
else
    echo "Unexpected sbctl status:"
    echo "$status"
    exit 1
fi

echo "Creating keys..."
create=$(sudo sbctl create-keys)
if [["$create" == *"Secure boot keys created!"* ]]; then
    echo "Keys created successfully!"
else
    echo "Unexpected sbctl create-keys output:"
    echo "$create"
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

# Generate a BLAKE2B hash for the splash image
hash=$(sudo b2sum /boot/${path})
if [[ ${#hash} -ne 64 ]]; then
    echo "Error generating BLAKE2B hash for the splash image"
    exit 1
fi

# Append the hash to the image file and replace the existing line with the new path.
hashPath="boot():/${path}#${hash}"
sudo sed -i "s|wallpaper: boot():/.*|${hashPath}|" /boot/limine.conf
if [[ $? -ne 0 ]]; then
    echo "Error updating limine.conf with the new wallpaper path"
    exit 1
fi 

## Enroll the config checksum and sign Limine’s EFI binary ##
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

# To use fwupd with Secure Boot enabled, sign the UEFI executable
sudo sbctl sign -s -o /usr/lib/fwupd/efi/fwupdx64.efi.signed /usr/lib/fwupd/efi/fwupdx64.efi

# And add the following to /etc/fwupd/fwupd.conf
"\n[uefi_capsule]\nDisableShimForSecureBoot=true" >> /etc/fwupd/fwupd.conf


echo "Secure Boot is setup successfully!"
exit 0






