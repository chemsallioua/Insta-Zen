
from followers import InstaUnfollowers

from pystray import MenuItem, Menu, Icon
from PIL import Image
from subprocess import Popen

from credentials import account, password

from logging import basicConfig, info, INFO
import os
import signal

class Instagram_Bot:
    def __init__(self):
        
        self.terminal_process = None
        self.my_bot = None
        
        with open('UnfollowBot.log', 'w') as f:
            f.seek(0)
            f.write('')
        
        basicConfig(filename='UnfollowBot.log',filemode='a', level=INFO)
        self.pid = os.getpid()

    def on_clicked(self, icon):
        # open the terminal when the tray icon is clicked
        # os.system('app.log')
        self.terminal_process = Popen(['notepad.exe', 'UnfollowBot.log'])

    def on_exit(self, icon):
        # do something when the program is exiting
        info("Exit Clicked")
        
        if self.terminal_process is not None:
            self.terminal_process.terminate()
        
        info("now closing ICON")
        try:
            icon.stop()
        except:
            os.kill(self.pid, signal.SIGTERM)
        os.kill(self.pid, signal.SIGTERM)
        
    def create_menu(self, icon):
        item_open = MenuItem('Open Logs', self.on_clicked)
        item_exit = MenuItem('Exit', self.on_exit)
        menu = Menu(item_open, item_exit)
        return menu
    
    def setup(self, icon):
        
        icon.visible = True
        
        # Run bot
        info("Initializing WebDriver Manager")
        info("--------------------------------")
        self.my_bot = InstaUnfollowers(self.account, self.password, self.accountUrl, silent= False)
        # my_bot.get_unfollowers()
        self.my_bot.unfollow_not_following_back(max_sleep_time_minutes = 15)
        if self.my_bot is not None:
            try:
                self.my_bot.driver.close()
            except:
                info("Failed to close chrome driver")
                self.my_bot.driver.close()

    def run(self, account, password):
        self.account = account
        self.password = password
        self.accountUrl = "https://instagram.com/" + str(self.account) + "/"
        
        icon = Icon('UnfollowBot')
        icon.title = 'Instagram Unfollowing Bot'
        icon.menu = self.create_menu(icon)
        icon.icon = Image.open('icon.ico')
        icon.run(self.setup)

if __name__ == '__main__':
    
    myInstaBot = Instagram_Bot()
    myInstaBot.run(account,password)