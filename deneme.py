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

sql = "SELECT name, followerNumber FROM urls"

cursor.execute(sql)

listem = cursor.fetchall()

x = 0
for i in listem:
    if x == 1:
        break
    sql = "UPDATE urls SET followerNumber = %s WHERE name = %s"
    intValue = re.findall(r'\d+', i[1])
    print(int(intValue[0]) * 1000)
    values = (int(intValue[0]) * 1000,i[0])
    cursor.execute(sql,values)
    connection.commit()

    x = x + 1