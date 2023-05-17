import time
import os
import pwinput
import sys
from datetime import datetime
import json

from bs4 import BeautifulSoup

from datetime import datetime
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from win10toast import ToastNotifier
from discord import SyncWebhook

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def sleepForDelay(delay):
    for remaining in range(delay, -1, -1):
        sys.stdout.write("\rTrying again in {:{}d} seconds.".format(
            remaining, len(str(delay))))
        sys.stdout.flush()
        time.sleep(1)
    print("\n")
    return


def getInfo():

    with open("info.json", "r") as f:
        userInfo = json.load(f)

    userid = userInfo["userid"]
    password = userInfo["password"]
    PATH = userInfo["ChromeDriver"]
    delay = userInfo["delay"]

    if userid == "":
        userid = input("""It seems like you have left "userid" blank in "info.txt".\n
                       Please update it or enter it now:\n
                       (The value you enter now will not be saved on your machine)\n
                       UserID:""")

    if password == "":
        print("""\nIt seems like you have left "password" blank in "info.txt".\n
              Please update it or enter it now:\n
              (The value you enter now will not be saved on your machine)\n""")
        password = pwinput.pwinput(
            mask="*", prompt="Password:")

    if delay == "":
        delay = int(
            input("How often would you like to check for updates? (seconds)\n"))

    return userid, password, PATH, int(delay)


def initDriver(PATH):

    service = Service(PATH)

    op = webdriver.ChromeOptions()
    # uncomment this if you want chrome to be hidden.
    op.add_argument('--headless')
    op.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=op)
    driver.implicitly_wait(10)

    return driver


def printInfo():
    print("\nStarting program with the following setttings:")
    print("UserID:" + userid)
    print("Password:" + "*"*len(password))
    print("Delay between checks:" + str(delay))
    return


def handleException(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print("Something went wrong. \n\n")
    print(exc_type, fname, exc_tb.tb_lineno)
    print(e)


def login():

    driver.get("https://student.uwo.ca/")

    driver.find_element(By.ID, "userid").send_keys(userid)
    driver.find_element(By.ID, "pwd").send_keys(password)

    driver.find_element(By.CLASS_NAME, "ps-button").click()

    return


def complete2FA():

    while (True):

        try:

            driver.switch_to.frame("duo_iframe")
            try:
                driver.find_element(By.CLASS_NAME, "btn-cancel").click()

            except:
                try:
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.ID, "win0divLPNAVSELECT")))
                    return
                except:
                    continue

            print("\nIgnore current 2FA notifcation.")

            time.sleep(7.5)

            driver.find_element(By.NAME, "dampen_choice").click()

            time.sleep(7.5)

            driver.find_element(
                By.XPATH, "//button[normalize-space()='Send Me a Push']").click()

            print("\nPlease complete your 2FA now.")

            driver.switch_to.default_content()

            WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.ID, "win0divLPNAVSELECT")))

            break

        except Exception as e:
            errorCount += 1
            handleException(e)
            continue
    return


def navigateToGrades():
    driver.find_element(
        By.ID, "win0divPTNUI_LAND_REC_GROUPLET$2").click()

    driver.find_element(
        By.ID, "win0divPTNUI_LAND_REC_GROUPLET$2").click()
    return


def getTerms():

    terms = driver.find_elements(By.TAG_NAME, "option")
    terms.pop(0)

    return terms


def askUserForTerm():

    print("\nSelect which term:\n")

    for i in range(len(terms)):
        print(i, ":", terms[i].text)

    selectedTerm = input("\n")

    return selectedTerm


def selectTerm():

    terms[int(selectedTerm)].click()

    driver.find_element(By.ID, "DERIVED_AA2_DERIVED_LINK3").click()


def htmlExtractor(htmldoc, currentMarks, filename, selectedCourses):
    marks = []
    titles = []

    soup = BeautifulSoup(htmldoc, "html.parser")

    marksHTML = soup.findAll(id=lambda x: x and x.startswith(
        "WSA_ENROLMNT_CRSE_GRADE_OFF$"))
    titlesHTML = soup.findAll(id=lambda x: x and x.startswith(
        "WSA_ENROLMNT_DESCR$"))

    for i in range(len(marksHTML)):
        marks.append(marksHTML[i].string)
        titles.append(titlesHTML[i].string)

    return analyzeList(marks, titles, currentMarks, filename, selectedCourses)


def analyzeList(list, titles, currentMarks, filename, selectedCourses):

    colorama_init()

    for i in range(len(list)):
        if list[i] == '''\xa0''':
            list[i] = "N/A"

    for i in range(len(titles)):
        if "&amp;" in titles[i]:
            titles[i] = titles[i].replace("&amp;", "&")

    if selectedCourses == [] and list != ['']*len(titles):
        print("\nSelect which courses you want to track changes for:")
        print("\nLeave blank to track all courses.\n")
        print("For example: 0,1,2,4")

        for i in range(len(list)):
            print(str(i)+" : "+titles[i])
        temp = input("\n")
        print("\n")
        if temp == "":
            selectedCourses = [i for i in range(len(list))]
        else:
            selectedCourses = temp.split(",")

    for i in range(len(selectedCourses)):
        selectedCourses[i] = int(selectedCourses[i])

    if list != ['']*len(titles):

        NewList = list
        NewTitles = titles
        list = []
        titles = []

        for i in range(len(selectedCourses)):
            list.append(NewList[selectedCourses[i]])
            titles.append(NewTitles[selectedCourses[i]])

    f = open(str(filename)+".txt", "a")
    print("\n")
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    for i in range(len(titles)):
        if list[i] != "N/A" and list[i] != "NGR":
            print(Fore.GREEN + str(titles[i]) +
                  ' : ' + str(list[i])+Style.RESET_ALL)
        else:
            print(titles[i], ":", list[i])
    f.write("\n")
    f.write(str(list))
    f.close()

    if list == ['']*len(titles):
        print("Timeout")
        print("\n\n")
        return currentMarks, selectedCourses

    if currentMarks == [] or currentMarks == [''] or currentMarks == ['']*len(titles):
        print("Grades available:", len(titles) -
              (int(list.count("N/A"))+int(list.count("NGR"))))
        print("\n\n")
        return list, selectedCourses

    if list != currentMarks:

        action()

        indicesOfDifference = []
        marksOfDifference = []
        titlesofDifference = []

        for i in range(len(list)):
            if list[i] != currentMarks[i]:
                indicesOfDifference.append(i)
                marksOfDifference.append(list[i])
                titlesofDifference.append(titles[i])

        sendMessage("Ameen just got", str(marksOfDifference),
                    str(titlesofDifference))

        print("Change detected!")
        print("Grades available:", len(titles) -
              (int(list.count("N/A"))+int(list.count("NGR"))))
        print("\n\n")
        return list, selectedCourses
    else:
        print("No change detected.")
        print("Grades available:", len(titles) -
              (int(list.count("N/A"))+int(list.count("NGR"))))
        print("\n")
        return list, selectedCourses


def sendMessage(message, number, title):
    webhook = SyncWebhook.from_url(url)
    webhook.send(message + " " + str(number) +
                 " in " + str(title) + "!" + " W or L?")


def action():
    toaster = ToastNotifier()
    toaster.show_toast(
        "MARK UPDATE", "MARKS ARE OUTTTTTTTT", duration=1)
    # Changing the duration to a big number will delay the program from running by however much duration is.


def initError():
    try:
        element = driver.find_element(
            By.XPATH, f"//*[text()='Please wait for the initialization to finish.']")
    except:
        return False

    return element.is_displayed() and element.is_enabled()


userid, password, PATH, delay = getInfo()

driver = initDriver(PATH)

printInfo()

# INITIALIZE VALUES
selectedCourses = []
isTermSelected = False
currentMarks = []
selectedTerm = 0
firstRun = True
errorCount = 0
url = "https://discord.com/api/webhooks/xxxxxxxxxxxxxxx/xxxxxxxxxxx"

os.chdir("logs")
now = datetime.now()
filename = now.strftime("%Y-%m-%d_%H-%M-%S")


while (True):
    try:
        if (("Discovery Credit Form" not in driver.page_source)
            or (firstRun)
                or (errorCount > 4)):

            login()

            complete2FA()

            print("\n2FA Complete.")

            firstRun = False

            navigateToGrades()

        driver.switch_to.frame(
            driver.find_element(By.ID, "main_target_win0"))

        terms = getTerms()

        if isTermSelected == False:

            selectedTerm = askUserForTerm()

            isTermSelected = True

        selectTerm()

        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "WAIT_win0")))  # This waits until the grades are displayed.

        currentMarks, selectedCourses = htmlExtractor(
            driver.page_source, currentMarks, filename, selectedCourses)

        driver.switch_to.default_content()

        errorCount = 0

        driver.refresh()

        sleepForDelay(delay)

    except Exception as e:
        errorCount += 1
        handleException(e)
        sleepForDelay(delay)
        continue
