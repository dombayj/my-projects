import mysql.connector
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# Selenium setup
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option(name='detach', value=True)


driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="11osman11",
    database="instagramurl"
)
cursor = connection.cursor()

sql = "SELECT url FROM urls WHERE followerNumber > 5000"
cursor.execute(sql)

liste = cursor.fetchall()
def signIn():
    driver.get("https://www.instagram.com/")
    driver.maximize_window()

    cerezKabul = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button._a9--._ap36._a9_0"))
    )
    cerezKabul.click()

    username = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input._aa4b._add6._ac4d._ap35"))
    )
    password = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[name='password']"))
    )
    username.send_keys("osmandombyj")
    password.send_keys("18osman38**")

    girisButonu = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button._acan._acap._acas._aj1-._ap30"))
    )
    time.sleep(1)
    girisButonu.click()
    hatirlaButton = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button._acan._acap._acas._aj1-._ap30"))
    )
    hatirlaButton.click()
    time.sleep(4)
df = pd.read_csv('filtered_urls.csv')
signIn()

# driver.get("https://www.instagram.com/biggroove/")
# button = wait.until(
#        EC.element_to_be_clickable((By.CSS_SELECTOR, "button._acan._acap._acat._aj1-._ap30"))
#    )

# button.cli

for index, row in df.iterrows():
   url = row["url"]
   driver.get(url)
   button = wait.until(
       EC.element_to_be_clickable((By.CSS_SELECTOR, "button._acan._acap._acat._aj1-._ap30"))
   )
   button.click()
   button2 = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[text()='Takibi Bırak']"))
            )
   button2.click()
   


        

