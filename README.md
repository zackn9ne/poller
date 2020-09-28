# poller a macOS Upgrader for use with JamfPro
polls various conditions and then updates macOS from escallated user, feedback window from jamfHelper.app

# usage
1. create a distributable python
2. get the diistributable python and this script on the end user computer
3. run things: `/opt/companyname/python3.7 /opt/companyname/poller/poller.py -t 10.15`
4. bonus items: 
    1. there are some flags like `--dry-run` which you should try, you can also try changing the `-t` for various forms of testing
    2. if conditions are met you will get a Upgrade Completed notification in case the user tries to run it on an already satisfied upgrade
    
