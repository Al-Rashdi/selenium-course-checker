import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.text import MIMEText
import os
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options

username = os.environ["GMAIL_USER"]
password = os.environ["GMAIL_PASS"]

def my_script():
    chromedriver_autoinstaller.install()

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://self-service.dal.ca/BannerExtensibility/customPage/page/dal.stuweb_academicTimetable")
        time.sleep(3)

        subject = driver.find_element(By.LINK_TEXT, "Select a Subject")
        driver.execute_script("arguments[0].scrollIntoView(true);", subject)
        time.sleep(0.5)
        subject.click()
        time.sleep(1)

        actions = ActionChains(driver)
        actions.send_keys("jour")
        actions.send_keys(Keys.RETURN)
        actions.perform()
        time.sleep(2)
        filter_input = driver.find_element(By.ID, "pbid-filterText")
        driver.execute_script("arguments[0].scrollIntoView(true);", filter_input)
        

        
        filter_input.click()
        filter_input.send_keys("C/D")
        time.sleep(0.5)

        full_elements = driver.find_elements(By.XPATH, "//*[text()='FULL']")
        print(f"Number of FULL appearances: {len(full_elements)}")

        if len(full_elements) < 3:
            notify("journalism avaliable")

        driver.get("https://self-service.dal.ca/BannerExtensibility/customPage/page/dal.stuweb_academicTimetable")
        time.sleep(3)
        
        subject = driver.find_element(By.ID, "s2id_pbid-subjectCode")
        driver.execute_script("arguments[0].scrollIntoView(true);", subject)
        time.sleep(0.5)
        subject.click()
        time.sleep(1)
        
        actions = ActionChains(driver)
        actions.send_keys("PSYO")
        actions.send_keys(Keys.RETURN)
        actions.perform()
        time.sleep(2)
        filter_input = driver.find_element(By.ID, "pbid-filterText")
        driver.execute_script("arguments[0].scrollIntoView(true);", filter_input)
        filter_input.click()
        filter_input.send_keys("31148")
        time.sleep(1)
        
        wlist_number= driver.find_elements(By.XPATH,"//td[.//font[text()='WLIST']]/preceding-sibling::td[1]")

        for el in wlist_number:
            print("Number to the left of WLIST:", el.text.strip())
            wlist_number = int(wlist_number[0].text.strip())

            
        with open("data.txt", "r") as f:
            old_value = int(f.read().strip())

        # New value from your Selenium script
        new_value = wlist_number  # Replace this with your actual logic

        if new_value < old_value:
            # Send email or alert
            print("List decreased! Notifying user...")
            notify("List decreased!")
        elif new_value > old_value:
            print("List increased! Notifying user...")
            notify("List increased!")
        # Update the file with the new value
        with open("data.txt", "w") as f:
            f.write(str(new_value))



    except Exception as e:
        print(f"❌ Error occurred: {e}")
        
        
    finally:
        driver.quit()
def notify(message):
    msg = MIMEText("check timetable!")
    msg["Subject"] = message
    msg["From"] = username
    msg["To"] = username

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(username, password)
        server.send_message(msg)

    print("Email sent!")

# Run once when script is triggered
my_script()