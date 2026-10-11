#!/bin/bash
product="$(sudo dmidecode -t 2 | grep "Product Name:"  2>/dev/null)"
model="${product#*Product Name:}"
clear
printf "\nEnter the BIOS to:\n"
printf "  1. Put Secure Boot into Setup Mode\n"
printf "  2. Set to the default keys.\n"
printf "\n"
printf "After 'Save & Exit', the script will run itself again after logging in.\n"
printf "\n\e[32m" # Blue
printf "If unsure, you can search:%s secure boot setup mode\n" "$model"
printf "\n"
printf "Note: If you do not see any options for Secure Boot, you may need to enable the 'Advanced Mode' in the BIOS first.\n"
printf "\e[35m\n" # Magenta
printf "If you have an ASUS or MSI motherboard, please follow these instructions:\n"
printf "\t\t\tI recommend taking a photo...\n"
printf "\e[32m" # Blue
printf "  ASUS:\n"
printf "   1. Navigate to \e[4m\e[32mBoot\e[0m\e[32m -> \e[4mSecure Boot\e[0m\e[32m\n"
printf "   2. Set \e[4mSecure Boot Mode\e[0m\e[32m to \e[4mCustom\e[0m\e[32m\n"
printf "   3. Open \e[4mKey Management\e[0m\e[32m -> \e[4mDelete all Secure Boot Variables\e[0m\e[32m\n"
printf "\n"
printf "  MSI:\n"
printf "   1. Navigate to \e[4mSettings\e[0m\e[32m -> \e[4mSecurity\e[0m\e[32m -> \e[4mSecure Boot\e[0m\e[32m\n"
printf "   2. Set \e[4mSecure Boot Mode\e[0m\e[32m to \e[4mCustom\e[0m\e[32m\n"
printf "   3. Select \e[4mCompatibility\e[0m\e[32m -> \e[4mMaximum Security\e[0m\e[32m.\n"
printf "   4. Go to \e[4mKey Management\e[0m\e[32m\n"
printf "   5. Select \e[4mEnroll all Factory Default keys\e[0m\e[32m -> \e[4mDisabled\e[0m\e[32m\n"
printf "   6. Select \e[4mDelete all Secure Boot variables\e[0m\e[32m\n"


printf "\e[0m\n\n" # End colors
read -r -p "Press Enter to reboot the computer directly into the BIOS..."
echo "Restarting in 5..."
sleep 1
echo "Restarting in 4..."
sleep 1
echo "Restarting in 3..."
sleep 1
echo "Restarting in 2..."
sleep 1
echo "Restarting in 1..."
sleep 1
echo "Restarting in 0..."
sudo systemctl reboot --firmware-setup