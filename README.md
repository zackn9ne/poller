# poller. a macOS Upgrader for use with JamfPro
A tool to run major updates to macOS.. eg 10.14->10.15.. 10.15 -> 10.16

[![poller](https://github.com/zackn9ne/poller/blob/master/img/demo.gif)](https://github.com/zackn9ne)

# flags
```
/path/to/poller.py
--dry-run runs without pop-ups and doesn't do anything
-t target eg 10.15
-i interactive mode, provides a choice about installing instead of just doing it
```

# the good
1. dosen't matter if users are admin
2. makes sure they have at least x% battery
3. provides a feedback window when all the things are happening
4. low probabability of users messing this up

# the bad?
1. you will need JamfPro (enrolled?) installed on the target computer `/Library/Application Support/JAMF/bin/\
jamfHelper.app/Contents/MacOS/jamfHelper`
2. needs python 3.7, so create a distributable python
3. get the diistributable python and this script on the end user computer
4. run things: `/opt/companyname/python3.7 /opt/companyname/poller/poller.py -t 10.15`

