import time
import os
import pwinput
import sys
from datetime import datetime
from beautifulSoup import htmlExtractor
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# This is for getting the user's info from info.json

with open("info.json", "r") as f:
    userInfo = json.load(f)

selectedCourses = []

userid = userInfo["userid"]

password = userInfo["password"]

PATH = userInfo["ChromeDriver"]

if userid == "":
    userid = input("""It seems like you have left "userid" blank in "info.txt".\nPlease update it or enter it now:\n(The value you enter now will not be saved on your machine)\nUserID:""")

if password == "":
    print("""\nIt seems like you have left "password" blank in "info.txt".\nPlease update it or enter it now:\n(The value you enter now will not be saved on your machine)\n""")
    password = pwinput.pwinput(
        mask="*", prompt="Password:")


delay = int(input("How often would you like to check for updates? (seconds)\n"))


service = Service(PATH)

op = webdriver.ChromeOptions()
# uncomment this if you want chrome to be hidden.
# op.add_argument('--headless')
op.add_argument('--service')
op.add_argument('--hide-scrollbars')
op.add_argument('--disable-gpu')
op.add_argument('--log-level=3')
driver = webdriver.Chrome(options=op)
driver.implicitly_wait(10)


print("\nStarting program with the following setttings:")
print("UserID:" + userid)
print("Password:" + "*"*len(password))
print("Delay between checks:" + str(delay))

isTermSelected = False


currentMarks = []
selectedTerm = 0
errorCount = 999  # Anything big so that it can run the first time.

os.chdir("logs")
now = datetime.now()
filename = now.strftime("%Y-%m-%d_%H-%M-%S")


while (True):
    try:
        if (errorCount > 5):
            try:

                driver.get("https://student.uwo.ca/")

                useridField = driver.find_element(By.ID, "userid")
                passwordField = driver.find_element(By.ID, "pwd")

                useridField.send_keys(userid)
                passwordField.send_keys(password)

                submitButton = driver.find_element(By.CLASS_NAME, "ps-button")
                submitButton.click()

                print("\nPlease complete your 2FA.\n")

                while (True):

                    try:
                        passedYet = WebDriverWait(driver, 60).until(
                            EC.presence_of_element_located((By.ID, "win0divLPNAVSELECT")))
                        break
                    except:
                        print("2FA failed, trying again.\n")
                        driver.refresh()

                print("2FA complete.\n")

                driver.find_element(
                    By.ID, "win0divPTNUI_LAND_REC_GROUPLET$2").click()

                driver.find_element(
                    By.ID, "win0divPTNUI_LAND_REC_GROUPLET$2").click()

                errorCount = 0

            except:
                errorCount += 1
                print(
                    f"Something went wrong. Error count:{errorCount}. Will reattempt logging in at error count greater than 5.\n")
        driver.refresh()

        time.sleep(0.3)

        iframeForTerms = driver.find_element(By.ID, "main_target_win0")

        driver.switch_to.frame(iframeForTerms)

        terms = driver.find_elements(By.TAG_NAME, "option")

        terms.pop(0)
        if isTermSelected == False:

            print("Select which term:\n")

            for i in range(len(terms)):
                print(i, ":", terms[i].text)

            selectedTerm = input("\n")

            isTermSelected = True

        terms[int(selectedTerm)].click()

        changeLink = driver.find_element(By.ID, "DERIVED_AA2_DERIVED_LINK3")
        changeLink.click()

        time.sleep(1)

        errorCount = 0

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        errorCount += 1
        print(
            f"Something went wrong. Error count: {errorCount}. Will reattempt logging in at error count greater than 5.\n\n")
        print(exc_type, fname, exc_tb.tb_lineno)
        print(e)
        for remaining in range((delay), 0, -1):
            print(' ' * 40, end='\r')
            print("Trying again in " + str(remaining),
                  "seconds.", end="\r")
            sys.stdout.flush()
            time.sleep(1)
        continue
    time.sleep(2)
    returnedTuple = htmlExtractor(
        driver.page_source, currentMarks, filename, selectedCourses)

    driver.switch_to.default_content()

    currentMarks = returnedTuple[0]
    selectedCourses = returnedTuple[1]
    timer = delay

    for remaining in range(delay, 0, -1):
        print(' ' * 40, end='\r')
        print("Trying again in " + str(remaining),
              "seconds.", end="\r")
        sys.stdout.flush()
        time.sleep(1)

    print(' ' * 40, end='\r')
    print("Trying again in 0 seconds.", end="\r")
