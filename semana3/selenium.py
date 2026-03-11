from selenium import webdriver
import time
from selenium.webdriver.common.by import By

#start session
driver = webdriver.Chrome()

#open page
driver.get("https://www.saucedemo.com/")

# wait for the page to load
time.sleep(2)

username = driver.find_element(By.ID, "user-name")

password = driver.find_element(By.ID, "password")

button = driver.find_element(By.ID, "login-button")

#interact with elements
username.send_keys("standard_user")
password.send_keys("secret_sauce")
button.click()

time.sleep(5)

driver.quit()