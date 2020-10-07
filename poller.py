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
import re

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
chances = 15


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
        global pct
        pmset = shlex.split('pmset -g batt')        
        pmset = self.cmd_to_stdout(pmset)
        if settings.DEVenvironment:
            print(f'Battery info is: {pmset}')

        pct=pmset.split(';')
        pct = re.search("\\d+(?:\\.\\d+)?%", str(pct))
        pct = pct.group()
        pct = int(pct[:-1])            

        if 'AC Power' in pmset:
            pct = (f'AC Power {pct}%')
            return True
        else:
            if pct > threshold:
                return True
       
            else:
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
    '''get the classes ready'''
    p = Poller()
    Mw = makewindow.Make_Window
    settings.init()        
    '''gather info'''
    os_version = p.cmd_to_utf8(shlex.split('sw_vers -productVersion')).strip()
    make_log_file(logfile)
    count_lines(logfile)    
    '''make windows'''
    uc = Mw(
        'hud',
        'All Set Here',
        (f'Your machine is already running {os_version}minimum required is: {settings.target}. Thanks for checking!'),
        'Great'
        # ,button2="rad"
        )
    im = Mw(
        'hud',
        'installer missing',
        'Please contact support@advisory.nyc and tell them you are trying to update macOS but the installer is missing.',
        'Okay')
    if count_lines(logfile) < chances:
        gatekeeper = Mw(
            'utility',
            'Get Ready To Update',
            (f'To update to macOS {settings.target} click Begin. You will be offline for about a 20 minutes during the update. You have {chances - count_lines(logfile)} tries left.'),
            'Begin',
            button2="Remind Me"
            )
    else:
        gatekeeper = Mw(
            'utility',
            'Get Ready To Update',
            (f'Your machine is about to update to macOS {settings.target}. You will be offline for about a 20 minute portion of the update. You posponed {count_lines(logfile)} times and exceeded the max tries of {chances}.'),
            'Proceed')   
    ip = Mw(
        'hud',
        'update in progress',
        '''We need you to hold on because the installer is running.

Connect your changer and Work at your own risk a reboot is immintent.''',
        'Dismiss'
        )
    pm = Mw(
        'utility',
        'We want to update macOS but your battery is too low.',
        '''Simply connect a charger and click Try Now to start updating.''',
        'Try Now',
        button2="Give up"
    )
    bye = Mw(
        'hud',
        'macOS too old',
        '''Sorry your macOS is over 3 years old you will need a support technician to assit you. Simply email support@advisory.nyc Now to get started, and mention you need help updating.''',
        'Try Now',
        button2="Give up"
    )

    '''kick out ancient macos'''
    if str(os_version) < str(10.14):
        if settings.DEVenvironment:
            exit(f'DEVenvironment: {settings.DEVenvironment}. Popup would be: pre 10.14 system {os_version}')
        else:
            p.fire_window(bye.create())
            exit(f'OS too old. {os_version} exiting.')

    '''gather the rest'''
    p.check_battery()
    print(f'welcome to poller {settings.version} deferals at {count_lines(logfile)}/{chances} system at {os_version} on {pct}% target at {settings.target}')

    if settings.target in os_version:
        '''do silent things first'''
        if settings.DEVenvironment:
            exit(f'DEVenvironment: {settings.DEVenvironment}. Popup would be: error user already upgraded current: {os_version}')
        else:
            p.fire_window(uc.create())
            if user_agrees:
                exit(f'window fired: error user already upgraded: \
                current mac version {os_version}/{settings.target}')
            else:
                exit(f'window fired: error user already upgraded: \
                current mac version {os_version}/{settings.target}')                
                #exit just in case you gave them a two  button


    '''if we made it here we have to do things'''

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
                p.fire_window(gatekeeper.create())
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
