"""
Trying to automate the covid19 survey for UCSC

https://www.youtube.com/watch?v=ApA7EVwSzg0&ab_channel=SigmaCoding

"""

from splinter import Browser, exceptions
from selenium import webdriver
from time import sleep

USER = "mviscard"
PASS = "BLAH"

# Path to chrome driver
executable_path = {'executable_path': r'T:\COVID19_Survey\chromedriver.exe'}

if __name__ == '__main__':
    # Options
    options = webdriver.ChromeOptions()
    # options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    # Browser
    browser = Browser('chrome',
                      **executable_path,
                      headless=False,
                      options=options)
    browser.visit(r"https://ucsantacruz.co1.qualtrics.com/jfe/form/SV_7WXdjRMMuOrb0yh?Q_CHL=email")
    
    sleep(2)
    
    # Login to google
    email_box = browser.find_by_xpath(r'//*[@id="identifierId"]')
    email_box.fill(f"{USER}@ucsc.edu")
    email_next_button = browser.find_by_xpath(r'//*[@id="identifierNext"]/div/button').click()
    sleep(2)
    ucsc_user = browser.find_by_xpath(r'//*[@id="username"]').fill(USER)
    ucsc_pass = browser.find_by_xpath(r'//*[@id="password"]').fill(PASS)
    ucsc_login = browser.find_by_xpath(r'/html/body/section/div/form/button').click()
    sleep(2)
    login = False
    while not login:
        sleep(5)
        try:
            verify_button = browser.find_by_xpath(r'//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
            login = True
        except exceptions.ElementDoesNotExist:
            print("Tried!")
    
