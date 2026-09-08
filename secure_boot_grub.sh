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
sudo sbctl status
# Expected output:
    # Installed:      ✘ sbctl is not installed
    # Setup Mode:     ✘ Enabled
    # Secure Boot     ✘ Disabled


## Create keys ##
sudo sbctl create-keys
sudo sbctl enroll-keys --microsoft --firmware-builtin
# Expected output:
    # Created Owner UUID <uuid>
    # Creating secure boot keys...✔
    # Secure boot keys created!


## Enroll keys ##
sudo sbctl enroll-keys --microsoft --firmware-builtin
# Expected output:
    # Enrolling keys to EFI variables...✔
    # Enrolled keys to the EFI variables!


## Make sure that the keys are enrolled and setup mode is disabled ##
sudo sbctl status
# Expected output:
    # Installed:      ✔ sbctl is installed
    # Owner GUID:     <uuid>
    # Setup Mode:     ✔ Disabled
    # Secure Boot     ✘ Disabled
    # Vendor Keys:    microsoft

