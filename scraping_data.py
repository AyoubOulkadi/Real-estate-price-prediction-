# importing all the necessary libaries
import os
import csv
import time
import string
import pandas as pd
from re import search
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

def scraper():
    # defining the webdriver and config btw this code will be almost the same in all of your selenium scripts
    options = Options()
# !!! blocking browser notifications !!!
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
# starting in maximized window
    options.add_argument("start-maximized")
    options.add_argument("--disable-default-apps")
    options.add_argument("disable-infobars")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    Article= []
    Price=[]
    Location=[]
    Category=[]
    Type = []
    l = 0
    for j in range(1,400):
        try : 
            driver.get("https://www.sarouty.ma/acheter/proprietes-a-vendre.html?page="+str(j))
            ping = driver.find_element(By.CSS_SELECTOR,".card-list.card-list--property")
            pings = ping.find_elements(By.TAG_NAME,'a')
            for i in pings :
                elem =driver.find_elements(By.CSS_SELECTOR,'.card-intro__title')
                for i in elem :
                    Article+=[i.text]
                    elem = driver.find_elements(By.CSS_SELECTOR,'.card-intro__price')
                for m in elem :
                    Price+=[m.text]
                    elem = driver.find_elements(By.CSS_SELECTOR,'.card-specifications__location')
                for y in elem :
                    Location+=[y.text]
                    elem = driver.find_elements(By.CSS_SELECTOR,'.card-intro__type')
                for w in elem :
                    Type+=[w.text]
                    elem = driver.find_elements(By.CSS_SELECTOR,'.card-specifications__amenities')
                for u in elem :
                    Category+=[u.text]
        except : 
            NoSuchElementException
        res = {"Article":Article,"Price":Price,"Location":Location,"Type":Type,"Category":Category}
        df = pd.DataFrame.from_dict(res, orient='index')
        df1=df.transpose()
        df1=df1.to_csv(/home/ubuntu/Downloads/New_dataset1.csv')
    return df1