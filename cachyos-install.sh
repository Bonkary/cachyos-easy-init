## Basic Updates and yay installation ##
sudo pacman -Syu --noconfirm

if [[ $(pacman -Q yay) == "error: package 'yay' was not found" ]]; then
    echo "Installing yay..."
    sudo pacman -S yay --noconfirm
fi

yay -Syu --noconfirm

# Dependencies
yay -S xterm

./secure_boot.sh
if [[ $? -ne 0 ]]; then
    echo "Error: secure_boot.sh failed. Exiting."
    exit 1
fi








