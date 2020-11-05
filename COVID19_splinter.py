"""
Marcus Viscardi Nov 3, 2020
Trying to automate the covid19 survey for UCSC because clicking yes/no is annoying and I have better things to do...
    (e.g.: writing scripts like this! and hiding from the election)

This tool requires:
1. The splinter python library to be installed (this will also installed selenium):
    sudo pip3 install splinter
2. An config.py file with string variables for:
    a. USER (UCSC username, omit @ucsc.edu)
    b. PASS (your ucsc gold password - I am looking for a way to better hide this...)
    c. PI_EMAIL (the email of your manager to send the clearance confirmation)
3. Firefox and the firefox driver for automated browser interactions (geckodriver):
    https://github.com/mozilla/geckodriver/releases
    also it must be in your PATH, so move the downloaded+unpacked driver to /usr/bin/
4. alacarte if you want to set up a button on your desktop to run this script
    I can help people with this, too annoying to write out

***********************************************************************************************************
DISCLAIMER: By running this script and accepting your two factor authentication you are verifying that you:
    1. Do not have symptoms
    2. Have not taken medication for COVID symptoms
    3. Have not been in contact with anyone who has COVID19
    4. Have not received a positive test in 14 days
***********************************************************************************************************
"""

from splinter import Browser, exceptions
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from time import sleep
# config.py file must be in the same directory as COVID19_splinter.py
from config import USER, PASS, PI_EMAIL

# Option to hide the browser window while running:
HIDE_BROWSER_WINDOW = False

if __name__ == '__main__':
    # Disclaimer
    print("DISCLAIMER: By running this script and accepting your two factor authentication you are verifying that "
          "you:\n\t1. Do not have symptoms\n\t2. Have not taken medication for COVID symptoms\n\t3. Have not been in "
          "contact with anyone who has COVID19\n\t4. Have not received a positive test in 14 days")
    # Options
    options = webdriver.FirefoxOptions()
    options.add_argument("disable-notifications")
    # Browser
    browser = Browser(headless=HIDE_BROWSER_WINDOW)
    browser.visit(r"https://ucsantacruz.co1.qualtrics.com/jfe/form/SV_7WXdjRMMuOrb0yh?Q_CHL=email")

    sleep(2)

    try:  # This try is to catch if someone closes the window before the process finishes,
        #   it will not do anything if you are running without the browser shown!

        # Login to google
        email_box = browser.find_by_xpath(r'//*[@id="identifierId"]')
        email_box.fill(f"{USER}@ucsc.edu")
        email_next_button = browser.find_by_xpath(r'//*[@id="identifierNext"]/div/button').click()
        # Login to UCSC
        sleep(2)
        ucsc_user = browser.find_by_xpath(r'//*[@id="username"]').fill(USER)
        ucsc_pass = browser.find_by_xpath(r'//*[@id="password"]').fill(PASS)
        ucsc_login = browser.find_by_xpath(r'/html/body/section/div/form/button').click()

        # Catch if UCSC/Google thinks you're a bot (you are but we won't tell them)
        sleep(2)
        login = False
        while not login:
            sleep(2)
            try:
                verify_button = browser.find_by_xpath(r'//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div['
                                                      r'1]/div/div/button').click()
                login = True
            except exceptions.ElementDoesNotExist:
                # Move through first step of survey:
                try:
                    survey_one = browser.find_by_xpath(r'//*[@id="NextButton"]').click()
                    login = True
                except exceptions.ElementDoesNotExist:
                    continue
        # Second step of survey (enter email and say you will be on campus)
        manager_email = browser.find_by_xpath(r'//*[@id="QR~QID1"]').fill(PI_EMAIL)
        at_ucsc = browser.find_by_xpath(r'//*[@id="QID2-2-label"]').click()
        next = browser.find_by_xpath(r'//*[@id="NextButton"]').click()
        # Third survey step (location on campus - this is hardcoded to be Sins.)
        sleep(1)
        location = browser.find_by_xpath(r'//*[@id="QR~QID12~1"]').select("4")
        region = browser.find_by_xpath(r'//*[@id="QR~QID12~6"]').select("186")
        building = browser.find_by_xpath(r'//*[@id="QR~QID12~7"]').select("216")
        next = browser.find_by_xpath(r'//*[@id="NextButton"]').click()

        # Fourth survey step (no other location visited)
        sleep(1)
        no_other_location = browser.find_by_xpath(r'/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div['
                                                  r'3]/div[3]/div/fieldset/div/ul/li[3]').click()
        next =browser.find_by_xpath(r'//*[@id="NextButton"]').click()

        # Fifth survey step (the actual survey)
        sleep(1)
        symptoms = browser.find_by_xpath(r'/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[3]/div['
                                         r'3]/div/fieldset/div/ul/li[1]').click()
        meds = browser.find_by_xpath(r'/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[5]/div['
                                     r'3]/div/fieldset/div/ul/li[2]').click()
        contact = browser.find_by_xpath(r'/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[7]/div['
                                        r'3]/div/fieldset/div/ul/li[2]').click()
        test = browser.find_by_xpath(r'/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[9]/div['
                                     r'3]/div/fieldset/div/ul/li[2]').click()
        next = browser.find_by_xpath(r'//*[@id="NextButton"]').click()

        # Final survey step (accept acknowledgments; by using this script you are accepting these!!)
        sleep(1)
        next = browser.find_by_xpath(r'//*[@id="NextButton"]').click()

        # End of survey (script will print the result of your survey)
        sleep(1)
        result = browser.find_by_xpath(r'//*[@id="EndOfSurvey"]')
        print("\n", result.text)
        browser.quit()
    except WebDriverException:  # To catch early closures of the browser window
        print("Browser closed before process could finish!! Please try again.")

    print("\n(This window will try to close in 1 minute)")
    sleep(60)
    print("bye!")
