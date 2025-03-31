import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Connect to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="11osman11",
    database="instagramurl"
)
cursor = connection.cursor()

# Selenium setup
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option(name='detach', value=True)

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

sql = "SELECT url FROM urls"
cursor.execute(sql)
rows = cursor.fetchall()

def random_delay(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))

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
    username.send_keys("nihilismunderrated")
    password.send_keys("11osman11*")

    girisButonu = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button._acan._acap._acas._aj1-._ap30"))
    )
    time.sleep(1)
    girisButonu.click()
    time.sleep(4)
    ivir = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Kapat"]'))
    )
    ivir.click()

signIn()

# Loop through all URLs
for index, i in enumerate(rows):
    urlx = i[0]
    driver.get(urlx)
    
    followerCount = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.html-span.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1hl2dhg.x16tdsg8.x1vvkbs"))
    )

    followerText = followerCount[2].text
    
    if followerText is not None:
        update_query = "UPDATE urls SET followerNumber = %s WHERE url = %s"
        cursor.execute(update_query, (followerText, urlx))
        connection.commit()  # Commit the changes to the database
        print(f"Updated followerNumber for {urlx} to {followerText}")
    else:
        print(f"Skipping update for {urlx} due to scraping error")

    # Break the loop if this is the last element
    if index == len(rows) - 1:
        print("Reached the last element in the database. Exiting loop.")
        break
connection.commit()
# Close the browser and database connection
driver.quit()
cursor.close()
connection.close()