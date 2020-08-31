#!/opt/advisory/python3.7

# this is the actual updater tool
# checks if already upgraded
# checks for battery
# checks for installer

import subprocess
import shlex
import os.path
import argparse
import makewindow


# user vars
catalina = ('/Applications/Install macOS Catalina.app/Contents/\
Resources/startosinstall', '--agreetolicense', '--forcequitapps')
safari = ('open', '-a', 'Safari.app')
catalina_lt_pkg = ('jamf', 'policy', '-event', 'install-catalina-lt')
ls = ('ls', '-ltar')
pwd = ('pwd')
pmset = shlex.split('pmset -g batt')
osv = shlex.split('sw_vers -productVersion')
target = ["10.14", "Catalina"]

# use the makewindow module
Mw = makewindow.Make_Window
uc = Mw(
    'All Set Here',
    (f'Your machine is already running {target[1]}. Thanks for checking!'),
    'Great)'
    )
im = Mw(
    'installer missing',
    'We need to run a management action to prepare your computer \
press the button to acknowledge and try again shortly.',
    'Okay')
ip = Mw(
    'update in progress',
    '''We need you to hold on because the installer is running.

    Connect your changer and Work at your own risk a reboot is immintent.''',
    'Wait'
    )
pm = Mw(
    'You are on battery',
    '''Please connect a charger and rerun this program.''',
    'Close'
)

def get_args():
    '''cli args'''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run", action="store_true", default=''
    )
    parser.add_argument(
        '-t', action='store', type=float, required=True
    )

    args = parser.parse_args()

    return args

def check_os_version(cmd):
    '''return current macos version'''
    data = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    stdout, stderr = data.communicate()
    formatted_float = stdout.decode("utf-8")
    return formatted_float


def check_for_installer(cmd):
    '''is os upgrade installer on disk'''
    if os.path.isfile(cmd):
        return True
    else:
        # who cares about battery for this
        print(f'{cmd}installer not found, running JSS command {catalina_lt_pkg}.')
        return False


def check_for_battery(cmd):
    '''is it on AC Power'''
    batt_output = run_regular(cmd)
    if 'AC Power' in batt_output:
        return True
    else:
        print(f'battery check not passed: {batt_output}')
        return False


def run_regular(cmd):
    '''run a simple shell command'''
    data = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    stdout, stderr = data.communicate()
    return str(stdout)


def run_command(cmd):
    '''run a shell command with a while loop'''
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc


def fire_window(cmd):
    '''fire a window feed me a build_window list'''
    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main():
    '''return command line args'''
    args = get_args()
    print (f'args are {args.dry_run}')
    if args.dry_run:
       DEVenvironment = True
    else:
        DEVenvironment = False
    target = str(args.t)

    '''check if we have to do anything'''
    os_version = check_os_version(osv)
    if DEVenvironment and target in os_version:
        exit(f'DEVenvironment: {DEVenvironment}. Popup would be: error user already upgraded current: {os_version}')

    elif target in os_version:
        fire_window(uc.create())
        exit(f'window fired: error user already upgraded: {os_version}')

    '''now do things'''
    installer_there = check_for_installer(catalina[0])
    plug_there = check_for_battery(pmset)

    '''installer check'''
    if DEVenvironment and not installer_there:
        print(f'DEVenvironment: {DEVenvironment}. Popup would be: installer missing')
    if not DEVenvironment and not installer_there:
        fire_window(im.create())
        run_command(catalina_lt_pkg)

    '''power check'''
    if installer_there and not plug_there:
        fire_window(pm.create())

    '''the business end'''
    if installer_there and plug_there and DEVenvironment:
        print(f'DEVenvironment: {DEVenvironment}. All clear, we would be upgrading this machine.')
    if installer_there and plug_there and not DEVenvironment:
        fire_window(ip.create())
        run_command(catalina)


if __name__ == "__main__":
    main()
