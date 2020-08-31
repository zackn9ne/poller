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
target = "10.14"
can_i_run = shlex.split('pgrep startosinstall')
stop = ''

# use the makewindow module
Mw = makewindow.Make_Window
ar = Mw(
    'sorry already running',
    'Please be patient the updater is already running',
    'great'
    )
uc = Mw(
    'acompleted',
    'upgrade completed',
    'great'
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

def return_stdout_utf8_encoded(cmd):
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
        #print(f'{cmd}installer not found, running JSS command {catalina_lt_pkg}.')
        return False


def check_for_ac(cmd):
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




def check_candidate(target):
    os_version = return_stdout_utf8_encoded(osv)
    if target in os_version:
        return False
    else:
        return True

def eval_dry_run(args):
     if args.dry_run:
         return True
     else:
         return False

def main():
    args = get_args()
    target = str(args.t)
    is_running = return_stdout_utf8_encoded(can_i_run)
    
    ac = check_for_ac(pmset)
    pkg = check_for_installer(catalina[0])
    vok = check_candidate(target)
    dry = eval_dry_run(args)
    etasks = ['ac', 'pkg', 'vok', 'dry']
    tasks = [ac, pkg, vok, dry]
    for p,i  in enumerate(tasks):
        if not i:
            print(f'error task {etasks[p]} is missing')
            #break
        else:
            print('doin stuff')
    # def error_window_maker():
    #     if not vok: 
    #         print('version is fine')
    #         break
    #     if not ac:
    #         print('no charger')
    #     if not pkg: 
    #         print('no pkg')
    #     else:
    #         print('doing things')


    error_window_maker()


if __name__ == "__main__":
    main()
