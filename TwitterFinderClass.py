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
    def __init__(self, username, password, user):
        service = ChromeService(executable_path=ChromeDriverManager().install())
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument("--window-size=880,1080")
        
        self.user = user
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(service=service, options=chromeOptions)
        
        self.connect = sl.connect("user.db")
        
        with self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS User (id_user INTEGER, user TEXT, qtd_Following INTEGER, following TEXT, PRIMARY KEY('id_user' AUTOINCREMENT))")
    
    # def find_files(self, folderPath):
    #     filesNoExtension = []

    #     # Getting all files from python folder   
    #     for path in os.listdir(folderPath):
    #         indexFollowing = path.find(f"{self.user}")
    #         if os.path.isfile(os.path.join(folderPath, path)) and indexFollowing == 0:
    #             ponto = path.index(".")
    #             if ponto != -1:
    #                 filesNoExtension.append(path.replace(str(path[ponto:]), ""))

    #     # Checks if the files exists
    #     if len(filesNoExtension) == 0:
    #         print("No previous files were found.")
    #         indexFollowing = -1
    #         last_char = 0
    #         return indexFollowing, last_char
    #     else:
    #         indexFollowing = 0
    #         maxFileName = ""
    #         for i in filesNoExtension:
    #             if len(i) >= len(maxFileName):
    #                 maxFileName = i
    #                 last_char1 = maxFileName[-2:]
            
    #         last_char = filesNoExtension[-1][-1]
    #         if int(last_char) < int(last_char1):
    #             last_char = last_char1

    #         return indexFollowing, last_char
    
    # def create_files(self, path, indexFollowing, last_char, following):
    #     following_string = " ".join(following)
    #     if indexFollowing == -1:
    #         os.system('cls')
    #         print(f'\nFile created: following 1.txt\n')
    #         with open(f'{path}{self.user} 1.txt', 'w') as f:
    #             f.write(following_string)
    #     elif indexFollowing == 0 and int(last_char) >= 1:
    #         os.system('cls')
    #         print(f'\nFile created: {self.user} {int(last_char)+1}.txt')
    #         with open(f'{path}{self.user} {int(last_char)+1}.txt', 'w') as f:
    #             f.write(following_string)

    def login(self):
        self.driver.get('https://twitter.com/i/flow/login')
        self.driver.implicitly_wait(60)
        self.driver.find_element(By.XPATH, ("//input[@autocomplete='username']")).send_keys(self.username)
        self.driver.implicitly_wait(60)
        self.driver.find_element(By.XPATH, ('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]')).click()
        self.driver.find_element(By.XPATH, ("//input[@autocomplete='current-password']")).send_keys(self.password)
        self.driver.find_element(By.XPATH, ('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div')).click()
        time.sleep(5)

    def get_following(self):
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

    def add_database(self):
        followingString = " ".join(self.followingList)
        valores = [self.user, self.qtd_Following, followingString]
        
        with self.connect:
            query = ("INSERT INTO User (user, qtd_Following, following) VALUES (?, ?, ?)")
            self.cursor.execute(query, valores)
            
    def get_database(self):
        with self.connect:
            self.cursor.execute("SELECT * FROM User WHERE id_user = 2")
            result = self.cursor.fetchall()
            return result
            
    
    
# twitterFinder = TwitterFinder()

if __name__ == '__main__':
    load_dotenv()
    username = os.getenv("UR")
    password = os.getenv("PSS")
    user = 'ArknoXI'
    tf = TwitterFinder(username=username, password=password, user=user)
    
    folderPath = r"D:\Python\followingFolder"
    
    following = tf.get_following()

    char = tf.find_files(folderPath=folderPath)
    tf.create_files(f"{folderPath}\\", char[0], char[1], following)
    intChar = int(char[1]) + 1
    fileComparison(f'{folderPath}\\{user} {intChar}.txt', f'{folderPath}\\{user} {intChar-1}.txt')
    #