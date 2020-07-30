#!/usr/bin/python
#this is the actual updater tool
  
import subprocess
import shlex
import os.path

# env var
environment = 'DEV'

# user vars
catalina = ('/Applications/Install macOS Catalina.app/Contents/Resources/startosinstall', '--agreetolicense', '--forcequitapps')
safari = ('open', '-a', 'Safari.app')
catalina_lt_pkg = ('jamf', 'policy', '-event', 'install-catalina-lt')
ls = ('ls', '-ltar')
pwd = ('pwd')
pmset = shlex.split('pmset -g ac')

# windows
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
plug_in = (
    '/Library/Application Support/JAMF/bin/jamfHelper.app/Contents/MacOS/jamfHelper',
    '-windowType',
    'hud',
    'You are on battery',
    '-title',
    'please wait...',
    '-description',
    'Nice try but you need to have your charger plugged in, go find it and rerun this program please',
    '-icon',
    '/System/Library/CoreServices/Problem Reporter.app/Contents/Resources/ProblemReporter.icns',
    '-defaultbutton',
    '1',
    '-button1',
    'Finding Charger'
)
def check_for_installer(cmd):
    if os.path.isfile(cmd):
        fire_window(popup_a)
        return True
    else:
        print('installer not found, downloading JSS')
        fire_window(popup_b)
        run_command(catalina_lt_pkg)
        return False

def check_for_battery(cmd):
    if 'No adapter attached.' in run_regular(cmd):
        print('battery user')
    else:
        return True


def run_regular(cmd):
    data = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout,stderr = data.communicate()
    return stdout

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


def main():
    #if check_for_installer(catalina[0]) and check_for_battery(pmset):
    if check_for_battery(pmset):
        if check_for_installer(catalina[0]):
            if environment != 'DEV':
                run_command(catalina)
            else:
                print('dev mode not making any changes')
    else:
        fire_window(plug_in)


if __name__ == "__main__":
    main()
