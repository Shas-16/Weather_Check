from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from email.message import EmailMessage
import ssl
import smtplib

#Setting email variables:
app_password = "*************"
email_sender = 's.shaswathan@gmail.com'
email_receiver = 's.shaswathan@gmail.com'

em = EmailMessage()

#------------------------------------
#Getting driver and website:
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
website = "https://www.accuweather.com/en/gb/feltwell/ip26-4/daily-weather-forecast/329746"

driver.get(website)

#------------------------------------
#Accepting cookies:
accept_cookies_button = driver.find_element(
        By.XPATH, '//button[@class="fc-button fc-cta-consent fc-primary-button"]')
accept_cookies_button.click()

#------------------------------------
#Getting tomorrow's weather:
i = 0
weather_phrases = driver.find_elements(by = "xpath", value = '//div[@class="phrase"]')
for weather_day in weather_phrases:
    weather_phrase = weather_day.text
    if i == 1:
        weather_tomorrow = weather_phrase
    i += 1

driver.quit()

#------------------------------------
#Setting up email:
subject = "Tomorrow's Weather!"
body = "The weather tomorrow will be " + weather_tomorrow.lower()

em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com',465,context = context) as smtp:
    smtp.login(email_sender,app_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
