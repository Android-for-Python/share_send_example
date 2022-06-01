# Example of sharing from an app
#
# Files can be shared because they are in shared storage

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from os.path import join
from android import mActivity
from android_permissions import AndroidPermissions

from androidstorage4kivy import SharedStorage, Chooser, ShareSheet

class ShareSendExample(App):

    def build(self):
        self.test_uri = None
        Window.bind(on_keyboard = self.quit_app)
        b1 = Button(text='Share plain text via a ShareSheet',
                    on_press=self.button1_pressed)
        b2 = Button(text='Share "test.html" file via a ShareSheet',
                    on_press=self.button2_pressed)
        b3 = Button(text='Choose multiple files to share with Gmail',
                    on_press=self.button3_pressed)
        b4 = Button(text='Choose a video to share with the\n' +\
                    'share_recieve_example, which must be installed.',
                    on_press=self.button4_pressed)
        box = BoxLayout(orientation='vertical')
        box.add_widget(b1)
        box.add_widget(b2)
        box.add_widget(b3)
        box.add_widget(b4)
        self.box = box
        return box

    ### Start if permissions granted ###
    
    def on_start(self):
        self.dont_gc = AndroidPermissions(self.start_app)
        
    def start_app(self):
        self.dont_gc = None
        self.test_uri = self.create_test_uri()

    ### User Events ####
    
    def button1_pressed(self,b):
        ShareSheet().share_plain_text('Greetings Earthlings')
        self.button_reset(b)

    def button2_pressed(self,b):
        ShareSheet().share_file(self.test_uri)
        self.button_reset(b)
    
    def button3_pressed(self,b):
        self.target = 'com.google.android.gm'
        self.chooser = Chooser(self.chooser_callback)
        self.chooser.choose_content(multiple = True)
        self.button_reset(b)

    def button4_pressed(self,b):
        self.target = 'org.test.receive'
        self.chooser = Chooser(self.chooser_callback)
        self.chooser.choose_content('video/*')
        self.button_reset(b)

    def quit_app(self,window,key,*args):
        # back button/gesture quits app
        if key == 27:
            if self.test_uri:
                SharedStorage().delete_file(self.test_uri)
            mActivity.finishAndRemoveTask() 
            return True   
        else:
            return False

    ### Callback ####
    
    def chooser_callback(self,uri_list):
        ShareSheet().share_file_list(uri_list, self.target)
        del self.chooser

    ### Utilities ####

    def button_reset(self, b):
        # The target app may timeout the button on_touch_up() event,
        # so the button fails to reset. Explicitly reset the button.
        Clock.schedule_once(b._do_release, b.min_state_time)

    def create_test_uri(self):
        # create a file in Private storage
        filename = join(SharedStorage().get_cache_dir(),'test.html')
        with open(filename, "w") as f:
            f.write("<html>\n")
            f.write(" <head>\n")
            f.write(" </head>\n")
            f.write(" <body>\n")
            f.write("  <h1>All we are saying, is<h1>\n")
            f.write("  <h1>give bees a chance<h1>\n")
            f.write(" </body>\n")
            f.write("</html>\n")
        # Insert the test case in this app's Shared Storage so it
        # will have a Uri
        return SharedStorage().copy_to_shared(filename)
        
ShareSendExample().run()
