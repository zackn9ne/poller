# poller. a macOS Upgrader for use with JamfPro
# the good
1. dosen't matter if users are admin
2. makes sure they have at least 50% battery
3. provides a feedback window when all the things are happening
4. low probabability of users messing this up

# usage
1. create a distributable python
2. get the diistributable python and this script on the end user computer
3. run things: `/opt/companyname/python3.7 /opt/companyname/poller/poller.py -t 10.15`
4. bonus items: 
    1. there are some flags like `--dry-run` which you should try, you can also try changing the `-t` for various forms of testing
    2. if conditions are met you will get a Upgrade Completed notification in case the user tries to run it on an already satisfied upgrade
    
