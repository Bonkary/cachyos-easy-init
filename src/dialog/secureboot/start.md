## Welcome to Secure Boot

#### <u>Breakdown</u>
Secure Boot signs the kernel and drivers and other things with special keys and some stuff happens with the bootloader. That's what I know and I'm not even sure how accurate it is.

On Linux, Secure Boot keys and signings are managed via a package called `sbctl`. We will be installing it if you haven't started anything at all. I will be asking for your password to do so, *but I don't store it anywhere*.

The steps we will be following are:<br>
1. Installing `sbctl`
2. Enabling `Setup Mode`
3. Running some `sbctl` commands to enroll and sign the keys.
4. Enabling Secure Boot.

It's easy.