from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from FileComparison import fileComparison
import time
import os
from dotenv import load_dotenv
import sqlite3 as sl

class TwitterFinder:
    def __init__(self, username, password):
        service = ChromeService(executable_path=ChromeDriverManager().install())
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument("--window-size=880,1080")
        
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(service=service, options=chromeOptions)
    

    def login(self):
        self.driver.get('https://twitter.com/i/flow/login')
        self.driver.implicitly_wait(60)
        self.driver.find_element(By.XPATH, ("//input[@autocomplete='username']")).send_keys(self.username)
        self.driver.implicitly_wait(60)
        self.driver.find_element(By.XPATH, ('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]')).click()
        self.driver.find_element(By.XPATH, ("//input[@autocomplete='current-password']")).send_keys(self.password)
        self.driver.find_element(By.XPATH, ('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div')).click()
        time.sleep(5)

    def get_following(self, user):
        self.user = user
        self.login()
        self.driver.get(f"https://twitter.com/{self.user}")
        self.driver.implicitly_wait(60)
        qtd_Following = self.driver.find_element(By.XPATH, ('//a[contains(@href,"/following")]/span[1]/span[1]')).text
        self.driver.get(f"https://twitter.com/{self.user}/following")
        follow_ids = set()
        followingList = []

        currentPosition = None
        pagePosition = self.driver.execute_script("return window.pageYOffset;")
        self.driver.get_screenshot_as_file("screenshot.png")
        
        while True:
            
            time.sleep(0.5)
            pagePosition = self.driver.execute_script("return window.pageYOffset;")
            
            # Div with all following
            self.driver.implicitly_wait(60)
            div_follow = self.driver.find_element(By.XPATH, ('//div[contains(@data-testid,"primaryColumn")]'))
            self.driver.get_screenshot_as_file("screenshot.png")
            
            # Div with all user cell
            self.driver.implicitly_wait(60)
            userCell = div_follow.find_elements(By.XPATH, ('//div[contains(@data-testid,"UserCell")]'))
            
            for card in userCell:
                self.driver.implicitly_wait(60)
                element = card.find_element(By.XPATH, ('.//div[1]/div[1]/div[1]//a[1]'))
                self.driver.implicitly_wait(60)
                follow_element = element.get_attribute('href')
                follow_id = str(follow_element)
                follow_element = '@' + str(follow_element).split('/')[-1]
                
                if follow_element in followingList:
                    continue
                else:
                    follow_ids.add(follow_id)
                    followingList.append(follow_element)
                
            print(f"already registered: {len(followingList)}.")
            
            if pagePosition == currentPosition or len(followingList) == int(qtd_Following):
                break
            
            time.sleep(0.5)
            currentPosition = self.driver.execute_script("return window.pageYOffset;")
            self.driver.implicitly_wait(60)
            self.driver.find_element(By.XPATH, ('/html/body')).send_keys(Keys.PAGE_DOWN)
        
        print(f"total amount registered: {len(followingList)}.")

        self.qtd_Following = qtd_Following
        self.followingList = followingList
        return followingList 
            
    
class User:
    # Initializes the connection to the 'user' database
    def __init__(self, user):
        self.connect = sl.connect("user.db")
        
        self.user = str(user).lower()
        
        with self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.user} (id_user INTEGER, user TEXT, following TEXT, PRIMARY KEY('id_user' AUTOINCREMENT))")
       
    # Adds followingList to the 'user' database
    def add_database(self, followingList: list):
        followingString = " ".join(followingList)
        valores = [self.user, followingString]
        
        with self.connect:
            query = (f"INSERT INTO {self.user} (user, following) VALUES (?, ?)")
            self.cursor.execute(query, valores)
    
    # Returns the given user's table
    def get_database(self):
        try:
            with self.connect:
                self.cursor.execute(f"SELECT * FROM {self.user}")
                self.result = self.cursor.fetchall()
                return self.result
        except AttributeError as e:
            print("You must have forgotten to call the 'add_database' function to pass the username and add something to the database")
            print(e)
            
    def get_last_two(self):
        followingList = []
        followingDict = {}
        result = self.get_database()
        
        for user in result:
            followingDict.update({f"{user[1]}-{user[0]}":f"{user[2]}"})
        
        for item in followingDict.values():
            followingList.append(item)
        
        mostRecent = []
        secondRecent = []
        mostRecent.append(followingList[-1]) # Most recent
        try:
            secondRecent.append(followingList[-2])
            return mostRecent, secondRecent
        except IndexError as e:
            print("You need to run the program twice to compare two lists")
            print(e)

    def show_tables(self): 
        with self.connect:
            sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
            self.cursor.execute(sql_query)
            
            print("List of tables:")
            print("\t",self.cursor.fetchall())