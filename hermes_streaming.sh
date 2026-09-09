#! /bin/bash


if [[ ! $(cat /etc/pacman.config) == *"lizardbyte"* ]]; then
    echo ""  | sudo tee -a /etc/pacman.conf &>/dev/null
    echo "[lizardbyte]" | sudo tee -a /etc/pacman.conf &>/dev/null
    echo "SigLevel = Optional" | sudo tee -a /etc/pacman.conf &>/dev/null
    echo "Server = https://github.com/LizardByte/pacman-repo/releases/latest/download" | sudo tee -a /etc/pacman.conf &>/dev/null


    echo ""  | sudo tee -a /etc/pacman.conf &>/dev/null
    echo "[lizardbyte-beta]" | sudo tee -a /etc/pacman.conf &>/dev/null
    echo "SigLevel = Optional" | sudo tee -a /etc/pacman.conf &>/dev/null
    echo "Server = https://github.com/LizardByte/pacman-repo/releases/download/beta" | sudo tee -a /etc/pacman.conf &>/dev/null
fi

yay -S sunshine --noconfirm

mkdir sunshine
cd sunshine || exit 1
wget https://github.com/LizardByte/Sunshine/releases/latest/download/sunshine.pkg.tar.gz
tar -xvf sunshine.pkg.tar.gz

yay -Q libva-mesa-driver &>/dev/null
if [[ $? == 1 ]]; then
    yay -S libva-mesa-driver  --noconfirm # AMD GPU encoding support
fi

makepkg -si

yay -R sunshine --noconfirm

cd ..
rm -rf sunshine
rm hermes-streaming-0.5.1-1-x86_64.pkg.tar.zst
