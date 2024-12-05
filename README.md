
# KINGDOM HEARTS HD 1.5 + 2.5 ReMIX - Lite Launcher README



## What is it?
It's a really specific use-case launcher for people who have KINGDOM HEARTS HD 1.5 + 2.5 ReMIX installed from the Epic Games Store... through Heroic... On Windows... And who want to have separate non-Steam shortcuts for each game... Or to just have the luxury of skipping one set of copyright screens and logos.

Listen, I made it for me, okay? If you want it, enjoy.
## How's it work?
Heroic is already able to launch the separate executables for the games through sorcery I can't comprehend because I can't be bothered to learn. But in the spirit of specific use-cases, you can only set it to one game at a time. This rewrites the Heroic config file for KINGDOM HEARTS HD 1.5 + 2.5 ReMIX to change the game on the fly. In a fancy little launcher!
## But... Isn't that just the same shit in an extra EXE file?
Mostly! But with one important difference. Mine has launch arguments!

#### 1. Put my EXE anywhere you like. 
#### 2. I recommend running it once, as it'll prompt you for:
        
    - Your KH_1.5_2.5 install folder
         
    - Your Heroic EXE
        
    - The Heroic game config file for KINGDOM HEARTS HD 1.5 + 2.5 ReMIX
        
        (This should be ~AppData/Roaming/heroic/GamesConfig/68c214c58f694ae88c2dab6f209b43e4.json)

Now it'll have those locations saved in launcher_config.json and won't prompt you again

#### 3. Add it as a non-Steam game or make a desktop shortcut
#### 4. Add one of the following launch arguments

        --kh1   (for KINGDOM HEARTS FINAL MIX)
        --com   (for KINGDOM HEARTS Re:Chain of Memories)
        --kh2   (for KINGDOM HEARTS II FINAL MIX)
        --bbs   (for KINGDOM HEARTS Birth by Sleep FINAL MIX)

#### 5. Rename/prettify your shortcuts however you like and you're golden! With the launch argument, it'll skip the launcher and boot straight into the game (after Heroic launches in the background, unfortunately, but I'll take what I can get.)

If you prefer to just use this launcher normally, you can do that too. I worked hard on it. I know it doesn't look like it.

If you're sick of it or Re:Fined makes it obsolete (fingers crossed), just delete "KINGDOM HEARTS HD 1.5 + 2.5 ReMIX - Lite Launcher.exe" and the "kh-launcher.json" file next to it and go back to setting the alternative EXE in the KINGDOM HEARTS HD 1.5 + 2.5 ReMIX Heroic settings menu.

### Acknowledgements

This launcher is loosely based of of Heufneutje's "KingdomHeartsSteamDeckLaunch" here:

https://github.com/Heufneutje/KingdomHeartsSteamDeckLaunch

I adapted it with Python for Windows with the help and hinderance of ChatGPT and caffeine.
