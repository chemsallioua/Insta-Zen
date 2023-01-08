from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from random import randint
from logging import basicConfig, info, INFO
from datetime import datetime, timedelta
from subprocess import CREATE_NO_WINDOW

class InstaUnfollowers:
    def __init__(self, user, pwd , accountUrl, login = "auto", silent = False):
        
        basicConfig(filename='UnfollowBot.log',filemode='a', level=INFO)
        
        self.accountUrl = accountUrl
        options = Options()
        
        if silent == True:
            options.add_argument('--headless')
        # service=Service(ChromeDriverManager().install())
        service=Service('chromedriver')
        service.creation_flags = CREATE_NO_WINDOW
        self.driver = webdriver.Chrome(service=service, options=options)
        info("WebDriver Manager successfully initialized.")
        self.driver.get("https://instagram.com")
        
        override = "off"
        
        sleep(2)
        # Accept cookies
        try:
            accept_all_btn = self.driver.find_element(By.XPATH, '//button[text()="Allow essential and optional cookies"]')
            accept_all_btn.click()
            sleep(2)
        except:
            pass
        
        # Check if credentials are empty
        if (login == "auto" or login == "a") and (user == "" or pwd == ""):
            info("Error: No values given in credentials.py, please attempt manual login.")
            override = "manual"
        # Try auto-login
        if (login == "auto" or login == "a") and override == "off":
            username_type = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input')
            username_type.send_keys(user)
            password_type = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input")
            password_type.send_keys(pwd)
            log_in = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button')
            log_in.click()
            sleep(8)
            if self.driver.current_url == "https://instagram.com":
                info("Auto-Login unsuccessful, please attempt manual login.")
                override = "manual"
            else:
                info("Auto-Login successful.")
        # Expect Manual-Login
        if (login == "manual" or login == "m") or override == "manual":
            info("Please log in to your account in the opened window and confirm any text and press enter.")
            info("You can also exit the program with 'exit'")
            waitforinput = input(">> ")
            if waitforinput == "exit":
                quit()
            info("Continue...")

    def get_unfollowers(self):
        # Go to given account
        info("Accessing profile...")
        self.driver.get(self.accountUrl)
        sleep(3)
        # Get following people
        info("Getting following people, this might take a while...")
        following_element = self.driver.find_element(By.PARTIAL_LINK_TEXT, "following")
        following_element.click()
        following_list = self.get_people()
        # Get followers
        info("Getting followers, this might take a while...")
        followers_element = self.driver.find_element(By.PARTIAL_LINK_TEXT, "follower")
        followers_element.click()
        followers_list = self.get_people()
        # Get not following people in list
        info("Getting not following people in list...")
        self.not_following_back = [user for user in following_list if user not in followers_list]
        # print data in ordered list
        self.not_following_back.sort()
        
        info("These people are not following you:")
        # for name in self.not_following_back:
        #     info(name)
        info("Total: " + str(len(self.not_following_back)))
        with open('not_following_back.txt', 'w') as f:
            for profile in self.not_following_back:
                f.write(profile)
                f.write('\n')

    def get_people(self):  # Get people in list, return as list
        sleep(2)
        # Access scroll-box
        scroll_box = self.driver.find_element(By.CLASS_NAME, "_aano")
        prev_height, height = 0, 1
        # Execute while there are more people to load
        while prev_height != height:
            prev_height = height
            sleep(2)
            height = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        # Get people by anchor elements
        info("done scrolling...")
        links = scroll_box.find_elements(By.TAG_NAME, 'a')
        info("done scrolling...1")
        names = [name.text for name in links if name.text != '']
        info("Got one list of: " + str(len(names)))
        self.driver.get(self.accountUrl)
        info("done scrolling...2")
        sleep(3)
        return names
    
    def unfollow_not_following_back(self, max_sleep_time_minutes = 60, max_profile_count = 90):
        
        info(str(datetime.now())+" | "+"Unfollowing profiles...")
        
        with open('not_following_back.txt') as f:
            self.not_following_back = [line for line in f.readlines()]
            
        # sleep_time = rd.randint(0,9)
        profile_count = 1
        if self.not_following_back != []:
            for profile_name in self.not_following_back:
                
                if(profile_count > max_profile_count):
                    break
                
                profileUrl = "https://instagram.com/" + profile_name
                
                #Navigating to the profile page 
                not_connected = True
                while(not_connected):                
                    try:
                        self.driver.get(profileUrl)
                    except:
                        info(str(datetime.now())+" | "+"Unable to connect!... trying again")
                        sleep(4)
                    else:
                        not_connected = False
                sleep(2)
                info(str(datetime.now())+" | "+ "Profile: " + str(profile_name)+ " page opened... | Profile count : "+ str(profile_count)+"------------------------------")
                try:
                    sleep(1)
                    following = self.driver.find_element(By.XPATH, '//div[text()="Following"]')
                    following.click()
                    info(str(datetime.now())+" | "+"clicked on Following...")
                    sleep(1)
                    unfollowing = self.driver.find_element(By.XPATH, '//div[text()="Unfollow"]')
                    unfollowing.click()
                    info(str(datetime.now())+" | "+"clicked on Unfollow...")
                    profile_count = profile_count + 1
                    sleep_minutes =  randint(1, max_sleep_time_minutes)
                    end_time = datetime.now() + timedelta(minutes=sleep_minutes)
                    
                    info(str(datetime.now())+" | "+"sleeping for minutes: "+ str(sleep_minutes))
                    while datetime.now() < end_time:
                        sleep(1)
                except:
                    info(str(datetime.now())+" | "+"Following button not found...removing profile from list")

                self.not_following_back.remove(profile_name)
                with open('not_following_back.txt', 'w') as f:
                    for profile in self.not_following_back:
                        f.write(profile)    
                        
            info(str(datetime.now())+" | "+"Done unfollowing All list...")
            return   
        else:
            info(str(datetime.now())+" | "+"No profiles to be unfollowed...")  
            return
