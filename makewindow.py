#!/opt/advisory/python3.7
# windows
import settings

class Make_Window():
    def __init__(self,ux,bar,content,button, button2=''):
        '''this just tees up a dict'''
 
        self.window = { 
            'app': '''/Library/Application Support/JAMF/bin/\
jamfHelper.app/Contents/MacOS/jamfHelper''',
            'cmd1': '-windowType',
            'type': ux,
            'cmd2':   '-title',
            'title': bar,
            'cmd3': '-description',
            'content': content,
            'cmd4': '-icon',
            'icon': '''/System/Library/CoreServices/Problem Reporter.app/Contents/Resources/ProblemReporter.icns''',
            'cmd5': '-defaultbutton',
            'default_btn':'1',
            'cmd6': '-button1',
            'button': button
        } 
        if button2:
            self.window['cmd7'] = '-button2'
            self.window['button2'] = button2
                   

    def create(self):
        '''this creates the completed dict'''
        self.windowz = []
        #print(self.window['app'])
        for k, v in self.window.items():
            #print(k, v)
            #windowz.append(k)
            self.windowz.append(v)
        if settings.DEVenvironment:
            print(f"DEVenvironment: creating window command: {self.windowz}")
    
        return self.windowz
