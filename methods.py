import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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


def scroll_down_fully():
    max_attempts = 10  # Maximum number of attempts to scroll
    attempts = 0

    while attempts < max_attempts:
        scrollableElement = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.xyi19xy.x1ccrb07.xtf3nb5.x1pc53ja.x1lliihq.x1iyjqo2.xs83m0k.xz65tgg.x1rife3k.x1n2onr6"))
        )
        last_height = driver.execute_script("return arguments[0].scrollHeight", scrollableElement)
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", scrollableElement)
        time.sleep(2)  # Adjust sleep time as needed
        new_height = driver.execute_script("return arguments[0].scrollHeight", scrollableElement)
        if new_height == last_height:
            attempts += 1
        else:
            attempts = 0


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
    hatirlaButton = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button._acan._acap._acas._aj1-._ap30"))
    )
    hatirlaButton.click()
    time.sleep(4)


signIn() 

def takeList():
    # Go to profile
    profile = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-describedby='«R2srkldd6iuspipd5aq»']"))
    )
    profile.click()

    # Open followers list
    followerList = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.xl565be.x1m39q7l.x1uw6ca5.x2pgyrj"))
    )
    followerList[2].click()

    # Wait for followers to load
    time.sleep(5)  # Adjust sleep time as needed

    scroll_down_fully()

    # Locate follower elements
    followersTable = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.x1dm5mii.x16mil14.xiojian.x1yutycm.x1lliihq.x193iq5w.xh8yej3"))
    )

    # SQL queries
    check_query = """
    SELECT url FROM urlstofollow WHERE url = %s
    """

    insert_query = """
    INSERT INTO urlstofollow (url, name)
    VALUES (%s, %s)
    """

    # Insert data one by one
    for follower in followersTable:
        try:
            # Extract data
            link_element = follower.find_element(By.CSS_SELECTOR, "a")
            href = link_element.get_attribute("href")
            username = href.split("/")[-2]  # Extract username from URL

            # Check for duplicates
            cursor.execute(check_query, (href,))  # Pass as a tuple
            result = cursor.fetchone()

            if not result:  # If no duplicate exists
                cursor.execute(insert_query, (href, username))  # Pass as a tuple
                connection.commit()
                print(f"Inserted: {username}, {href}")
            else:
                print(f"Skipped duplicate: {username}, {href}")
        except Exception as e:
            print(f"Error inserting {username}, {href}: {e}")
            connection.rollback()


takeList()




cursor.close()
connection.close()  
