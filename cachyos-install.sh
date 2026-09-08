## Basic Updates and yay installation ##
sudo pacman -Syu --noconfirm
sudo pacman -S yay --noconfirm
yay -Syu

./secure_boot.sh
if [[ $? -ne 0 ]]; then
    echo "Error: secure_boot.sh failed. Exiting."
    exit 1
fi








