#!/opt/advisory/python3.7
# windows
class Make_Window():

    def __init__(self):
        self.window = { 
            'app': '''/Library/Application Support/JAMF/bin/\
jamfHelper.app/Contents/MacOS/jamfHelper''',
            'cmd1': '-windowType',
            'type': 'hud',
            'bar': 'update in progress',
            'cmd2':   '-title',
            'title': 'please wait...',
            'cmd3': '-description',
            'content': '''We need you to hold on because a the installer is running.

                Connect your changer and Work at your own risk a reboot is immintent.''',
            'cmd4': '-icon',
            'icon': '''/System/Library/CoreServices/Problem Reporter.app/Contents/Resources/ProblemReporter.icns''',
            'cmd4': '-defaultbutton',
            'default_btn':'1',
            'cmd5': 'btn',
            'button': 'Great'
        } 

    def list_it(self):
        windowz = []
        #print(self.window['app'])
        for k, v in self.window.items():
            #print(k, v)
            #windowz.append(k)
            windowz.append(v)
        #print(f"windowz is {windowz}")
        return windowz


    def make_list(self, bar, content, button):
        self.window['bar'] = bar
        self.window['content'] = content
        self.window['button'] = button
