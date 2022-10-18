# Burp Suite Extender Spider Cookie and Monster
Support on Linux, Mac-OS, Windows (WSL)
## Set up: 

- Move the binary `cookiemonster` (newest) to the same directory with cookiemonster.py or modify the `cookiemonster_path` variable to your cookiemonster binary.
- Burp -> Extender -> Add. Switch to Python and select the cookiemonster.py file.
- Standard Output File: output.txt.
- Load extension. You should obtain the successful message.
- Then browse, extension will take the cookie that didn't see before and cookiemonster on it.

## Result:
- Whenever get a weak secret key, It will alert in `Dashboard` tab.
- Then check file: `output.txt` will show you the vulnerable url and its cookies.
- Run cookiemonster on that cookie to receive the key of vulnarable application

Author: @m0nsieur from VSRC <3

