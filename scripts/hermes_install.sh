#!/bin/sh

HERMES_DIR="/home/$USER/.hermes"

mkdir "$HERMES_DIR"
cd "$HERMES_DIR" || exit
git clone https://github.com/MrOz59/Hermes.git
git clone https://github.com/MrOz59/Hermes-KMS.git
cd "Hermes-KMS" || exit
make
makepkg -si --noconfirm
# handle pacman in use
# Reboot
# Do checks