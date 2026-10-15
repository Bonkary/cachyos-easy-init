#!/bin/sh

HERMES_HOME_DIR="$1"
PSWD="$2"

cd "$HERMES_HOME_DIR/Hermes-KMS" || exit 1
make
echo "$PSWD" | makepkg -si --noconfirm

