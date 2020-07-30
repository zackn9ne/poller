#!/usr/bin/python
#this is the actual updater tool
  
import subprocess
import shlex
import os.path
catalina = ('/Applications/Install macOS Catalina.app/Contents/Resources/startosinstall', '--agreetolicense', '--forcequitapps')
safari = ('open', '-a', 'Safari.app')
catalina_lt_pkg = ('jamf', 'policy', '-event', 'install-catalina-lt')
ls = ('ls', '-ltar')
pwd = ('pwd')
def check_for_installer(cmd):
    if os.path.isfile(cmd):
        print('installer found')
        fire_window(popup_a)
        return True
    else:
        print('installer not found, downloading JSS')
        fire_window(popup_b)
        run_command(catalina_lt_pkg)
        return False
def run_command(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break   
        if output: 
            print output.strip()
    rc = process.poll()
    return rc

def fire_window(cmd): #feed me a build_window()

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
popup_a = (
    '/Library/Application Support/JAMF/bin/jamfHelper.app/Contents/MacOS/jamfHelper',
    '-windowType',
    'hud',
    'update in progress',
    '-title',
    'please wait...',
    '-description',
    '''We need you to hold on because a the installer is running. 
    
    Connect your changer and Work at your own risk a reboot is immintent.''',
    '-icon',
    '/System/Library/CoreServices/Problem Reporter.app/Contents/Resources/ProblemReporter.icns',
    '-defaultbutton',
    '1',
    'btn',
    'Great'
)
popup_b = (
    '/Library/Application Support/JAMF/bin/jamfHelper.app/Contents/MacOS/jamfHelper',
    '-windowType',
    'hud',
    'downloading installer',
    '-title',
    'please wait...',
    '-description',
    'We need a breif installer download, press the button to acknowledge and try again shortly.',
    '-icon',
    '/System/Library/CoreServices/Problem Reporter.app/Contents/Resources/ProblemReporter.icns',
    '-defaultbutton',
    '1',
    '-button1',
    'Just my luck...'
)
def main():
    if check_for_installer(catalina[0]):
        run_command(catalina)
    
if __name__ == "__main__":
    main()           
