# poller. a macOS Upgrader for use with JamfPro

[![poller](https://github.com/zackn9ne/poller/raw/master/zackn9ne/img/swag.gif)](https://github.com/zackn9ne)


# the good
1. dosen't matter if users are admin
2. makes sure they have at least x% battery
3. provides a feedback window when all the things are happening
4. low probabability of users messing this up

# the bad?
1. needs python 3.7, so create a distributable python
2. get the diistributable python and this script on the end user computer
3. run things: `/opt/companyname/python3.7 /opt/companyname/poller/poller.py -t 10.15`

# flags
```
--dry-run runs without popus and doesn't do anything
-t target eg 10.15
-i interactive mode, provides a choice about installing instead of just doing it
```
