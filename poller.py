#!/usr/bin/env python3
# this is the actual updater tool
import subprocess
import shlex
import os.path

# env var
DEVenvironment = True

# user vars
catalina = ('/Applications/Install macOS Catalina.app/Contents/\
Resources/startosinstall', '--agreetolicense', '--forcequitapps')
safari = ('open', '-a', 'Safari.app')
catalina_lt_pkg = ('jamf', 'policy', '-event', 'install-catalina-lt')
ls = ('ls', '-ltar')
pwd = ('pwd')
pmset = shlex.split('pmset -g ac')

# windows
popup_a = (
    '''/Library/Application Support/JAMF/bin/jamfHelper.app/\
Contents/MacOS/jamfHelper''',
    '-windowType',
    'hud',
    'update in progress',
    '-title',
    'please wait...',
    '-description',
    '''We need you to hold on because a the installer is running.

    Connect your changer and Work at your own risk a reboot is immintent.''',
    '-icon',
    '''/System/Library/CoreServices/Problem Reporter.app/Contents/\
Resources/ProblemReporter.icns''',
    '-defaultbutton',
    '1',
    'btn',
    'Great'
)
popup_b = (
    '/Library/Application Support/JAMF/bin/jamfHelper.app/Contents\
/MacOS/jamfHelper',
    '-windowType',
    'hud',
    'downloading installer',
    '-title',
    'please wait...',
    '-description',
    'We need a breif installer download, press the button to \
acknowledge and try again shortly.',
    '-icon',
    '''/System/Library/CoreServices/Problem Reporter.app/Contents/\
Resources/ProblemReporter.icns''',
    '-defaultbutton',
    '1',
    '-button1',
    'Just my luck...'
)
plug_in = (
    '''/Library/Application Support/JAMF/bin/jamfHelper.app/\
Contents/MacOS/jamfHelper''',
    '-windowType',
    'hud',
    'You are on battery',
    '-title',
    'please wait...',
    '-description',
    '''Please connect a charger and rerun this program.''',
    '-icon',
    '''/System/Library/CoreServices/Problem Reporter.app/Contents/\
Resources/ProblemReporter.icns''',
    '-defaultbutton',
    '1',
    '-button1',
    'Close'
)


def check_for_installer(cmd):
    if os.path.isfile(cmd):
        return True
    else:
        # who cares about battery for this
        print('installer not found, downloading JSS')
        fire_window(popup_b)
        run_command(catalina_lt_pkg)
        return False


def check_for_battery(cmd):
    if 'No adapter attached.' in run_regular(cmd):
        print('battery check not passed')
        return False
    else:
        return True


def run_regular(cmd):
    data = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    stdout, stderr = data.communicate()
    return str(stdout)


def run_command(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc


def fire_window(cmd):  # feed me a build_window()
    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main():
    installer_there = check_for_installer(catalina[0])
    plug_there = check_for_battery(pmset)

    if installer_there and plug_there:
        if DEVenvironment is not True:
            fire_window(popup_a)
            run_command(catalina)
        else:
            print('all conditions passed but: dev mode not making any changes')
    elif installer_there and not plug_there:
        fire_window(plug_in)
    else:
        print('giving up')


if __name__ == "__main__":
    main()
