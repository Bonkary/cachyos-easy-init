yay -S sbctl --noconfirm

sudo grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=cachyos --modules="tpm" --disable-shim-lock

## Enter BIOS ##
# TODO: add warning 
systemctl reboot --firmware-setup

# TODO: instructions
# Next steps in BIOS (if prompted to reset, select No):
#   1. Set Setup mode 
#   2. Clear keys/variables
#   3. Save and exit
#   4. Use boot override to boot into CachyOS


## Check sbctl install and Setup Mode active ##
echo "Checking for Setup Mode..."
status=$(sudo sbctl status)
INSTALLED="Installed:      ✘ sbctl is not installed"
SETUP="Setup Mode:     ✘ Enabled"
SECURE="Secure Boot     ✘ Disabled"
if [["$status" == *"$INSTALLED"* && "$status" == *"S$SETUP"* && "$status" == *"$SECURE"* ]]; then
    echo "Setup mode is enabled!"
else
    echo "Unexpected sbctl status:"
    echo "$status"
    exit 1
fi


## Create keys ##
echo "Creating keys..."
create=$(sudo sbctl create-keys)
if [["$create" == *"Secure boot keys created!"* ]]; then
    echo "Keys created successfully!"
else
    echo "Unexpected sbctl create-keys output:"
    echo "$create"
    exit 1
fi


## Enroll keys ##
echo "Enrolling keys..."
enroll=$(sudo sbctl enroll-keys --microsoft --firmware-builtin)
if [["$enroll" == *"Enrolled keys to the EFI variables!"* ]]; then
    echo "Keys enrolled successfully!"
else
    echo "Unexpected sbctl enroll-keys output:"
    echo "$enroll"
    exit 1


## Make sure that the keys are enrolled and setup mode is disabled ##
echo "Checking sbctl status..."
status=$(sudo sbctl status)
if [["$status" == *"Installed:      ✔ sbctl is installed"* && "$status" == *"Setup Mode:     ✔ Disabled"* && "$status" == *"Secure Boot     ✘ Disabled"* && "$status" == *"Vendor Keys:    microsoft"* ]]; then
    echo "Keys enrolled and setup mode disabled successfully!"
else
    echo "Unexpected sbctl status:"
    echo "$status"
    exit 1
fi

## Signing the Kernel Image and Boot Manager ##
echo "Signing the kernel image and boot manager..."
ENABLE_ENROLL_LIMINE_CONFIG=yes >> /etc/default/limine

# Check the current name and path of the splash image in the config file
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
path+="#${hash}"
sudo sed -i "s|wallpaper: boot():/.*|wallpaper: boot():/${path}|" /boot/limine.conf
if [[ $? -ne 0 ]]; then
    echo "Error updating limine.conf with the new wallpaper path"
    exit 1
fi 








