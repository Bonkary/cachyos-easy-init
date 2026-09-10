#! /bin/bash

# TODO Look at the get started page to make sure its right
# TODO Change filepaths to account for ./tmp 

HERMES_VERSION="0.5.1"
HERMES_PACKAGE="hermes-streaming-$HERMES_VERSION-1-x86_64.pkg.tar.zst"
HERMES_DOWNLOAD="https://github.com/MrOz59/Hermes/releases/download/$HERMES_VERSION/$HERMES_PACKAGE"
HERMES_KMS_GIT=https://github.com/MrOz59/Hermes-KMS.git

SUNSHINE_DOWNLOAD=https://github.com/LizardByte/Sunshine/releases/latest/download/sunshine.pkg.tar.gz

qinstall() {
    local pkg=$1
    if [[ $pkg -eq $HERMES_PACKAGE ]]; then
        sudo pacman -U $HERMES_PACKAGE --noconfirm
    else
        echo sudo pacman -S --needed "$pkg" --noconfirm --nodeps
    fi
}

quninstall() {
    local pkg=$1
    sudo pacman "$pkg" --noconfirm
}

write_repo() {
    if [[ ! $(cat /etc/pacman.config) == *"lizardbyte"* ]]; then
        echo "Writing lizardbyte repos..."

        echo ""  | sudo tee -a /etc/pacman.conf &>/dev/null
        echo "[lizardbyte]" | sudo tee -a /etc/pacman.conf &>/dev/null
        echo "SigLevel = Optional" | sudo tee -a /etc/pacman.conf &>/dev/null
        echo "Server = https://github.com/LizardByte/pacman-repo/releases/latest/download" | sudo tee -a /etc/pacman.conf &>/dev/null


        echo ""  | sudo tee -a /etc/pacman.conf &>/dev/null
        echo "[lizardbyte-beta]" | sudo tee -a /etc/pacman.conf &>/dev/null
        echo "SigLevel = Optional" | sudo tee -a /etc/pacman.conf &>/dev/null
        echo "Server = https://github.com/LizardByte/pacman-repo/releases/download/beta" | sudo tee -a /etc/pacman.conf &>/dev/null
    
    fi
}

build_sunshine() {
    local SUNSHINE_TMP="./sunshine_tmp"
    local SUNSHINE_DEST="$HOME/sunshine"
    qinstall sunshine

    mkdir -p "$SUNSHINE_TMP"
    mkdir -p "$SUNSHINE_DEST"

    cd $SUNSHINE_TMP || exit 1
    wget $SUNSHINE_DOWNLOAD
    tar -xvf sunshine.pkg.tar.gz

    if ! sudo pacman -Q libva-mesa-driver &>/dev/null; then
        qinstall libva-mesa-driver # AMD GPU encoding support
    fi

    makepkg -sic

    sudo mv ./sunshine/* /opt/sunshine 

    cd ..
    rm -rf $SUNSHINE_TMP

    quninstall sunshine
}

install_hermes() {
    wget $HERMES_DOWNLOAD && qinstall $HERMES_PACKAGE && rm $HERMES_PACKAGE
    hermesDst=$(which hermes)
    symLink=$(readlink -f "$hermesDst")
    if ! sudo setcap -r "${symLink}"; then
        echo "Failed to setcap!"
        exit 1
    fi

    sudo ufw allow 47984,47989,48010/tcp 
    sudo ufw allow 47998:48000/udp

    systemctl --user start sunshine && systemctl --user enable sunshine
}

prepare_virt_disp() {
    echo "Configuring to allow Virtual Display"

    git clone $HERMES_KMS_GIT
    cd Hermes-KMS || exit 1
    sudo make dkms-install

    sudo modprobe hermes_kms initial_enabled=0
}

install_deps() {
    qinstall wl-clipboard
    qinstall xclip
    
    # qinstall cuda
    qinstall libva-mesa-driver

    if ! prepare_virt_disp; then
        echo "Failed to setup virtual display!"
        exit 1
    fi
}

clean_up() {
    if [[ -d "./sunshine" ]]; then
        rm -rf ./sunshine
    fi

    if [[ -f $HERMES_PACKAGE ]]; then
        rm $HERMES_PACKAGE
    fi

    if [[ -d "./Hermes-KMS" ]]; then
        rm -rf ./Hermes-KMS
    fi
}

if ! install_deps; then
    echo "Failed to install deps!"
    exit 1
fi

if ! write_repo; then
    echo "Failed to add the lizardbyte repo!"
    exit 1
fi

if ! build_sunshine; then
    echo "Failed to build sunshine binaries!"
    exit 1
fi

if ! install_hermes; then
    echo "Failed to install Hermes!"
    exit 1
fi


echo "HERMES_STREAMING=1" >> ./progress.log
