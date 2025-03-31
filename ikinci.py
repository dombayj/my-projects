import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# Connect to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="11osman11",
    database="instagramurl"
)
cursor = connection.cursor()

# Selenium setup
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--ignore-ssl-errors')
# options.add_experimental_option(name='detach', value=True)

# driver = webdriver.Chrome(options=options)
# wait = WebDriverWait(driver, 20)

sql = "SELECT name ,followerNumber FROM urls"

cursor.execute(sql)

numbers = cursor.fetchall()





for index,i in enumerate(numbers):
    if 'B' in i[1]:
        sql = "UPDATE urls SET followerNumber = %s WHERE name = %s"
        intValue = re.findall(r'\d+', i[1])
        values = (int(intValue[0]) * 1000,i[0])
        print(values)
        cursor.execute(sql,values)
        connection.commit()
    if 'Mn' in i[1]:
        sql = "UPDATE urls SET followerNumber = %s WHERE name = %s"
        intValue = re.findall(r'\d+', i[1])
        values = (int(intValue[0]) * 1000000,i[0])
        print(values)
        cursor.execute(sql,values)
        connection.commit()
    if index == len(numbers) - 1:
        print("all element have changed")
        break
