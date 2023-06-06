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
        self.username = username
        self.password = password
        self.user = user

    def __init_driver(self):
        service = ChromeService(executable_path=ChromeDriverManager().install())
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--headless=new")
        chromeOptions.add_argument("--window-size=880,1080")
        
        driver = webdriver.Chrome(service=service, options=chromeOptions)
        return driver

    def __login(self, driver):
        driver.get('https://twitter.com/i/flow/login')
        driver.implicitly_wait(60)
        driver.find_element(By.XPATH, ("//input[@autocomplete='username']")).send_keys(self.username)
        driver.implicitly_wait(60)
        driver.find_element(By.XPATH, ('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]')).click()
        driver.find_element(By.XPATH, ("//input[@autocomplete='current-password']")).send_keys(self.password)
        driver.find_element(By.XPATH, ('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div')).click()
        time.sleep(5)
        print("Pass")

    def get_following(self):
        driver = self.__init_driver()
        self.__login(driver)
        driver.get(f"https://twitter.com/{self.user}")
        driver.implicitly_wait(60)
        qtd_Following = driver.find_element(By.XPATH, ('//a[contains(@href,"/following")]/span[1]/span[1]')).text
        driver.get(f"https://twitter.com/{self.user}/following")
        follow_ids = set()
        followingList = []
        
        dot = qtd_Following.find('.')
        if dot > -1:
            qtd_Following = qtd_Following.replace('.', '')

        currentPosition = None
        pagePosition = driver.execute_script("return window.pageYOffset;")
        driver.get_screenshot_as_file("screenshot.png")
        
        while True:
            
            time.sleep(0.5)
            pagePosition = driver.execute_script("return window.pageYOffset;")
            
            # Div with all following
            driver.implicitly_wait(60)
            div_follow = driver.find_element(By.XPATH, ('//div[contains(@data-testid,"primaryColumn")]'))
            driver.get_screenshot_as_file("screenshot.png")
            
            # Div with all user cell
            driver.implicitly_wait(60)
            userCell = div_follow.find_elements(By.XPATH, ('//div[contains(@data-testid,"UserCell")]'))
            
            for card in userCell:
                driver.implicitly_wait(60)
                element = card.find_element(By.XPATH, ('.//div[1]/div[1]/div[1]//a[1]'))
                driver.implicitly_wait(60)
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
            currentPosition = driver.execute_script("return window.pageYOffset;")
            driver.implicitly_wait(60)
            driver.find_element(By.XPATH, ('/html/body')).send_keys(Keys.PAGE_DOWN)
        
        print(f"total amount registered: {len(followingList)}.")

        followingList = [x.lower() for x in followingList]
        followingList = sorted(followingList)

        return followingList

    def __find_files(self, folderPath):
        filesNoExtension = []

        # Getting all files from python folder   
        for path in os.listdir(folderPath):
            indexFollowing = path.find(f"{self.user}")
            if os.path.isfile(os.path.join(folderPath, path)) and indexFollowing == 0:
                ponto = path.index(".")
                if ponto != -1:
                    filesNoExtension.append(path.replace(str(path[ponto:]), ""))

        # Checks if the files exists
        if len(filesNoExtension) == 0:
            print("No previous files were found.")
            time.sleep(2)
            self.indexFollowing = -1
            self.last_char = 0

        else:
            self.indexFollowing = 0
            maxFileName = ""
            for i in filesNoExtension:
                if len(i) >= len(maxFileName):
                    maxFileName = i
                    last_char1 = maxFileName[-2:]
            
            self.last_char = filesNoExtension[-1][-1]
            if int(self.last_char) < int(last_char1):
                self.last_char = last_char1
    
    def create_files(self, path, following):
        self.__find_files(path)
        
        # following_string = " ".join(following)
        if self.indexFollowing == -1:
            os.system('cls')
            print(f'\nFile created: {self.user} 1.txt\n')
            with open(f'{path}{self.user} 1.txt', 'w') as f:
                f.write(following)
        elif self.indexFollowing == 0 and int(self.last_char) >= 1:
            os.system('cls')
            print(f'\nFile created: {self.user} {int(self.last_char)+1}.txt')
            with open(f'{path}{self.user} {int(self.last_char)+1}.txt', 'w') as f:
                f.write(following)