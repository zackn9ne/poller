#!/opt/advisory/python3.7
# windows
class Make_Window():

    def __init__(self,bar,content,button):
        self.window = { 
            'app': '''/Library/Application Support/JAMF/bin/\
jamfHelper.app/Contents/MacOS/jamfHelper''',
            'cmd1': '-windowType',
            'type': 'hud',
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

    def create(self):
        '''internal function'''
        self.windowz = []
        #print(self.window['app'])
        for k, v in self.window.items():
            #print(k, v)
            #windowz.append(k)
            self.windowz.append(v)
        print(f"creating window command: {self.windowz}")
        return self.windowz
