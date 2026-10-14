# Setup Mode
<u>**Important**</u>: We are <u>**NOT**</u> enabling `Secure Boot` yet. You won't be able to boot to CachyOS.

The first step (not including Windows) is to enable `Setup Mode` in the BIOS.
I know people get scared in the BIOS, but I promise it's not <u>AS EASY</u> to break stuff as people make it seem as long as you use common sense. It's updating BIOS I worry about. Some of y'all be impatient on a slight hang. Anyways.

If you click 'Reboot' (recommended), then it should reboot you directly into your BIOS. If you choose to reboot later, you can reopen this and the option will be there.

#### All motherboards:<br>
1. If your motherboard has an `EZ Mode` and `Advanced Mode`, you'll need to switch to `Advanced Mode`. Look around the screen and somewhere it'll tell you how.
2. There should be a tab called `Boot`. Go there.<br>
3. Go to the `Secure Boot` section.
4. Do <u>**NOT**</u> reset to Factory Keys unless told otherwise. I don't know what it'll do with Windows involved. *It wouldn't break your system,* may just cause some annoyance.

*Note: If you have an `ASUS` or `MSI` motherboard, follow your own instructions below!*<br>

#### Standard:
1. Select the `Reset to Setup Mode` option (or similar).<br>
&emsp;<u>Note:</u> For an odd reason, some motherboards will ask you to if you want to 'Reset Without Saving', **please don't do that.**
2. After <u>Setup Mode</u> is enabled, go to `Save & Exit` and reboot into CachyOS and reopen this app. I'll check if it worked.

#### Asus:
1. Set `Secure Boot` to `Custom`
2. Open `Key Management` and select `Delete all Secure Boot Variables`

#### MSI:
1. Set `Secure Boot` to `Custom`
2. Select `Maximum Security` compatability option.
3. Go to `Key Management`
4. Select `Enroll all Factory Default Keys` and select `Disabled`.<br>
*Note: Kinda unsure on this part. If you see it, do it. There's a photo on the wiki, it's just too ugly for me to place it in a creation of mine.*
5. Select `Delete all Secure Boot Variables` and if there's another prompt, select the one that deletes them.

*Note: Hopefully MSI is clear. It's just same wordsfrom the wiki, I can't make better instructions sadly.*

See you soon.