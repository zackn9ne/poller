#!/opt/advisory/python3.7

# this is the actual updater tool
# checks if already upgraded
# checks for battery
# checks for installer

import subprocess
import shlex
import os.path
import makewindow

# env var
DEVenvironment = False
DEVenvironment = True

# user vars
catalina = ('/Applications/Install macOS Catalina.app/Contents/\
Resources/startosinstall', '--agreetolicense', '--forcequitapps')
safari = ('open', '-a', 'Safari.app')
catalina_lt_pkg = ('jamf', 'policy', '-event', 'install-catalina-lt')
ls = ('ls', '-ltar')
pwd = ('pwd')
pmset = shlex.split('pmset -g batt')
osv = shlex.split('sw_vers -productVersion')
target = "10.14"

# use the makewindow module
Mw = makewindow.Make_Window
uc = Mw(
    'acompleted',
    'upgrade completed',
    'great'
    )
im = Mw(
    'installer missing',
    'We need to run a management action to prepare your computer \
press the button to acknowledge and try again shortly.',
    'no')
dm = Mw(
    'dev mode',
    'conditions passed but doing nothing because dev mode',
    'great'
    )
ip = Mw(
    'update in progress',
    '''We need you to hold on because a the installer is running.

    Connect your changer and Work at your own risk a reboot is immintent.''',
    'Read Me'
    )
pm = Mw(
    'You are on battery',
    '''Please connect a charger and rerun this program.''',
    'Close'
)
uc = uc.create()
im = im.create()
dm = dm.create()
ip = ip.create()
pm = pm.create()

def check_os_version(cmd):
    '''do we even need to do this'''
    data = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    stdout, stderr = data.communicate()
    formatted_float = stdout.decode("utf-8") 
    return formatted_float



def check_for_installer(cmd):
    '''is os installer on disk'''
    if os.path.isfile(cmd):
        return True
    else:
        # who cares about battery for this
        print(f'{cmd}installer not found, running JSS command {catalina_lt_pkg}.')
        fire_window(im)
        run_command(catalina_lt_pkg)
        return False


def check_for_battery(cmd):
    '''is it plugged in'''
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
    os_version = check_os_version(osv)
    if target in os_version:
        fire_window(uc)
        exit(f'error user already upgraded: {os_version}')

    installer_there = check_for_installer(catalina[0])
    plug_there = check_for_battery(pmset)

    if installer_there and plug_there:
        if DEVenvironment is not True:
            fire_window(ip)
            run_command(catalina)
        else:
            fire_window(dm)
            print('all conditions passed but\
                    dev mode not making any changes')
    elif installer_there and not plug_there:
        fire_window(pm)
    else:
        exit('giving up, we do not know what happened')


if __name__ == "__main__":
    main()
