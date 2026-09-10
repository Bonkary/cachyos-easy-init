#! /bin/bash

cd ./scripts || exit 1

install() {
    local pkg=$1
    echo sudo pacman "$pkg" --noconfirm --nodeps
}

if [[ ! -d "./tmp" ]]; then
    mkdir -p ./tmp
fi

sudo pacman -Syu --noconfirm --nodeps

if ! ./secure_boot.sh; then
    echo "Error: secure_boot.sh failed. Exiting..."
    exit 1
fi








