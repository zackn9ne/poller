#!/opt/advisory/python3.7

# this is the actual updater tool
# checks if already upgraded
# checks for battery
# checks for installer

import subprocess
import shlex
import os.path
import makewindow
import datetime
import settings


# prog vars
logfile = '/tmp/.poller-log'
def make_log_file(where):
    if os.path.exists(where):
        #do a thing
        with open(where, mode='a') as file:
            file.write(f'Refusal log recorded at {datetime.datetime.now()}\n')
    else:
        with open(where, mode='a') as file:
            file.write(f'Refusal log recorded at {datetime.datetime.now()}\n')

 
def count_lines(where):
    lines = 0
    where = open(where, "r")
    for line in where:
        line = line.strip("\n")
        lines += 1
    return(lines)


# user vars
catalina_installer = '/Applications/Install macOS Catalina.app/Contents/\
Resources/startosinstall'
catalina_install_cmd = ('/Applications/Install macOS Catalina.app/Contents/\
Resources/startosinstall', '--agreetolicense', '--forcequitapps')
threshold = 50


class Poller():
# funcs
    def cmd_to_stdout(self, cmd):
        '''main shell interactor'''
        data = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        stdout, stderr = data.communicate()
        return str(stdout)


    def cmd_to_utf8(self, cmd):
        '''return current macos version'''
        data = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        stdout, stderr = data.communicate()
        formatted_float = stdout.decode("utf-8")
        return formatted_float


    def while_cmd(self, cmd):
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


    def check_for_file(self, cmd):
        '''is os upgrade installer on disk'''
        if os.path.isfile(cmd):
            return True
        else:
            # who cares about battery for this
            print(f'{cmd} not found')
            return False


    def check_battery(self):
        '''return battery info'''
        pmset = shlex.split('pmset -g batt')        
        batt_stdout = self.cmd_to_stdout(pmset)
        if 'AC Power' in batt_stdout:
            return True
        else:
            print(f'on battery: {batt_stdout}')
            
            plaintxt_percent=batt_stdout.split(';')
            plaintxt_percent=plaintxt_percent[0][-3:-1]
            if int(plaintxt_percent) > threshold:
                print(f'battery good enough: {plaintxt_percent}')
                return True            
            else:
                print(f'battery too low failing: {plaintxt_percent}')
                return False


    def fire_window(self, cmd):
        '''fire a window feed me a build_window list'''

        global user_agrees
        user_agrees = ''
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if proc.returncode == 0:
            if settings.DEVenvironment:
                print('user clicked 0')
            user_agrees = True
        elif proc.returncode == 2:
            if settings.DEVenvironment:
                print('user clicked 2')
            user_agrees = False
        else:
            print(f"Error: {err}")

            
def main():
    '''main'''
    make_log_file(logfile)
    count_lines(logfile)

    # if lines > 10:
    #     '''run the program'''
    settings.init()    
    p = Poller()

    '''get the classes ready'''
    Mw = makewindow.Make_Window
    uc = Mw(
        'All Set Here',
        (f'Your machine is already running {settings.target}. Thanks for checking!'),
        'Great'
        # ,button2="rad"
        )
    im = Mw(
        'installer missing',
        'Please contact support@advisory.nyc and tell them you are trying to update macOS but the installer is missing.',
        'Okay')
    if count_lines(logfile) < 200:
        choices = Mw(
            'Get Ready To Update',
            (f'To update to macOS {settings.target} click Begin. You will be offline for about a 20 minutes during the update. You have {100 - count_lines(logfile)} tries left.'),
            'Begin',
            button2="Remind Me"
            )
    else:
        choices = Mw(
            'Get Ready To Update',
            (f'Your machine is about to update to macOS {settings.target}. You will be offline for about a 20 minute portion of the update. You have {count_lines(logfile)} exceeded the max tries of 100.'),
            'Proceed')   
    ip = Mw(
        'update in progress',
        '''We need you to hold on because the installer is running.

Connect your changer and Work at your own risk a reboot is immintent.''',
        'Dismiss'
        )
    pm = Mw(
        'Your battery is too low',
        '''Please connect a charger and rerun this program.''',
        'Try Now',
        button2="Give up"
    )

    '''check if we have to do anything'''
    os_version = p.cmd_to_utf8(shlex.split('sw_vers -productVersion'))

    if settings.target in os_version:
        '''do silent things first'''
        if settings.DEVenvironment:
            exit(f'DEVenvironment: {settings.DEVenvironment}. Popup would be: error user already upgraded current: {os_version}')
        else:
            p.fire_window(uc.create())
            if user_agrees:
                exit(f'window fired: error user already upgraded: {os_version}')
            else:
                #todo start a log session because the user declined
                print('was false')

    '''if we do have to do things'''

    '''installer check'''
    if not p.check_for_file(catalina_installer):
        if settings.DEVenvironment:
            exit(f'DEVenvironment: {DEVenvironment}. Popup would be: installer missing')
        else:
            p.fire_window(im.create())
            exit(f'can"t find installer')


    '''power check'''
    if p.check_for_file(catalina_installer) and not p.check_battery():
        if settings.DEVenvironment:
            exit(f'power too low giving up')
        else:
            p.fire_window(pm.create())
            if user_agrees:
                #rerun program
                main()
            else:
                exit(f'power too and user gave up')

    
    if p.check_for_file(catalina_installer) and p.check_battery():
        '''passed checks'''
        if settings.interactive:
            if settings.DEVenvironment:            
                print('passed all checks, popups would follow')
            else:
                p.fire_window(choices.create())
                if user_agrees:
                        p.fire_window(ip.create())
                        p.while_cmd(catalina_install_cmd)
                        print(f'upgrade in progress')
                else:
                    #todo start a log session because the user declined
                    print('user bailed')
        else:
            if settings.DEVenvironment:
                print('non interactive we would upgrade you')
            else:
                p.fire_window(ip.create())
                p.while_cmd(catalina_install_cmd)


if __name__ == "__main__":
    main()
