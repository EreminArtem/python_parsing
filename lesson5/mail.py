import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get('https://mail.ru/')

login_input = driver.find_element(By.CLASS_NAME, 'email-input')
login_input.send_keys('study.ai_172@mail.ru')
login_input.send_keys(Keys.ENTER)

wait = WebDriverWait(driver, 10)
password_input = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'password-input')))
password_input.send_keys('NextPassword172???')
password_input.send_keys(Keys.ENTER)

letters_list = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'letter-list')))

letters = []

last_letter = None
current_letter = None

while current_letter is None or last_letter != current_letter:
    l = letters_list.find_elements(By.CLASS_NAME, 'llc')
    letters.extend(l)
    current_letter = l[-1]
    current_letter.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    last_letter = letters_list.find_elements(By.CLASS_NAME, 'llc')[-1]

print(len(letters))
