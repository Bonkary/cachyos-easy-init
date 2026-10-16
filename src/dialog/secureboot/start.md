## <div align="center">Welcome to Secure Boot</div>
<br>

#### <div><u>What is Secure Boot</u></div>
Secure Boot signs the kernel and drivers and other things with special keys and some stuff happens with the bootloader. That's what I know and I'm not even sure how accurate it is.

On Linux, Secure Boot keys and signings are managed via a package called sbctl. We will be installing it if you haven't started anything at all. I will be asking for your password to do so, *but I don't store it anywhere*.
<br>

#### <div><u>Steps</u></div>
1. Installing 'sbctl'
2. Enabling 'Setup Mode' in BIOS.
3. Running some 'sbctl' commands to create and enroll the keys.
4. Signing your kernel and boot manager.
4. Enabling 'Secure Boot' in BIOS.
<br>

It's easy.