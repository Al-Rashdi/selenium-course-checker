import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # Optional helper
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.text import MIMEText
import schedule
import time
import os
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options


# Automatically install compatible chromedriver if not already installed


username = os.environ["GMAIL_USER"]
password = os.environ["GMAIL_PASS"]

def run_script():
    # put your Selenium code here or call it from a separate file
    print("Running script...")
    my_script()  # or import your function

def my_script():
    chromedriver_autoinstaller.install()
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)


    driver.get("https://self-service.dal.ca/BannerExtensibility/customPage/page/dal.stuweb_academicTimetable")

    time.sleep(3)

    subject = driver.find_element(By.LINK_TEXT, "Select a Subject")
    driver.execute_script("arguments[0].scrollIntoView(true);", subject)
    time.sleep(0.5)
    subject.click()

    time.sleep(3)


    actions = ActionChains(driver)
    actions.send_keys("jour")
    actions.send_keys(Keys.RETURN)
    actions.perform()


    time.sleep(3)

    filter_input = driver.find_element(By.ID, "pbid-filterText")
    filter_input.click()
    filter_input.send_keys("C/D")

    time.sleep(3)

    full_elements = driver.find_elements(By.XPATH, "//*[text()='FULL']")
    print(f"Number of FULL appearances: {len(full_elements)}")

    if len(full_elements) < 3:
        msg = MIMEText("check timetable!")
        msg["Subject"] = "Course Notification"
        msg["From"] = "akrashdi7410@gmail.com"
        msg["To"] = "akrashdi7410@gmail.com"  # or another email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(username, password)
            server.send_message(msg)

        print("Email sent!")
    driver.quit()
    
schedule.every(2).minutes.do(my_script)

while True:
    schedule.run_pending()
    time.sleep(1)



