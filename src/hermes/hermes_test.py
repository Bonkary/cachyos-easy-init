import hermes_logic as hermes
import sys

if not hermes.install_kms('password'):
    print("BOOO!")
    sys.exit(1)