import requests
import time
import os
import pwinput
import sys
from datetime import datetime
from beautifulSoup import htmlExtractor
from getICSID import getICSID
from terms import getTerms

# This is for getting the user's info from info.txt

f = open("info.txt", "r")

for i in range(4):
    f.readline()

userid = str(f.readline())[7:-1:].strip()
password = str(f.readline())[9::].strip()

selectedCourses = []

# courses = (str(f.readline()))[8::].strip()

# if courses == "":
#     courses = []
#     for i in range(n):
#         courses.append(i)
# else:

#     courses = courses.split(",")
#     courses = [int(x) for x in courses]


f.close()

if userid == "":
    userid = input("""It seems like you have left "userid" blank in "info.txt".\nPlease update it or enter it now:\n(The value you enter now will not be saved on your machine)\nUserID:""")

if password == "":
    print("""\nIt seems like you have left "password" blank in "info.txt".\nPlease update it or enter it now:\n(The value you enter now will not be saved on your machine)\n""")
    password = pwinput.pwinput(
        mask="*", prompt="Password:")

delay = int(input("How often would you like to check for updates? (seconds)\n"))


# didCoursesChange = False

# studentNumber = input("Enter your student number.\n")
# year = input("Enter the year of grades\n")

# os.chdir("cache")

# c = open("lastCourses.txt", "r")

# lastCourses = str(c.readline()).strip()
# lastYear = str(c.readline()).strip()
# c.close()

# if str(lastYear) != str(year) or str(lastYear) == "":
#     c = open("lastCourses.txt", "w")
#     c.write(str(courses)+"\n"+str(year))
#     didCoursesChange = True
#     print("Courses have been changed")

# if str(courses) != lastCourses and didCoursesChange == False:
#     if ((str(courses) != "" and lastCourses == [i for i in range(n)]) or (str(courses) == [i for i in range(n)] and lastCourses == "")):
#         c = open("lastCourses.txt", "w")
#         c.write(str(courses)+"\n"+str(year))
#         didCoursesChange = True
#         print("Courses have been changed")

# c.close()

# os.chdir("..")
# with open("logs.txt", "rb") as file:
#     try:
#         file.seek(-2, os.SEEK_END)
#         while file.read(1) != b'\n':
#             file.seek(-2, os.SEEK_CUR)
#     except:
#         file.seek(0)
#     lastline = file.readline().decode()

# currentMarks = lastline[1:-1].replace("'", '').replace(" ", "").split(",")

# if currentMarks == ['']*n or currentMarks == ['']:
#     currentMarks == []

print("\nStarting program with the following setttings:")
print("UserID:" + userid)
print("Password:" + "*"*len(password))
print("Delay between checks:" + str(delay))
# print("Courses:" + str(courses))

isTermSelected = False


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://student.uwo.ca/psc/heprdweb/EMPLOYEE/SA/c/UWO_RECORDS_UP2.WSA_ES_GRADE_LIST.GBL?NavColl=true&ICAGTarget=start',
    'Origin': 'https://student.uwo.ca',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-origin',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded'
}

currentMarks = []

os.chdir("logs")
now = datetime.now()
filename = filename = now.strftime("%Y-%m-%d_%H-%M-%S")

while (True):

    loginURL = "https://student.uwo.ca/psp/heprdweb/?&cmd=login&languageCd=ENG"
    icsidURL = """https://student.uwo.ca/psc/heprdweb/EMPLOYEE/SA/c/NUI_FRAMEWORK.PT_AGSTARTPAGE_NUI.GBL?CONTEXTIDPARAMS=TEMPLATE_ID:PTPPNAVCOL&scname=WSA_GRADES&PTPPB_GROUPLET_ID=WSA_GRADES&CRefName=WSA_NAVCOLL_2"""
    GetGradesURL = "https://student.uwo.ca/psc/heprdweb/EMPLOYEE/SA/c/UWO_RECORDS_UP2.WSA_ES_GRADE_LIST.GBL?NavColl=true&ICAGTarget=start"
    URLChangeYear = "https://student.uwo.ca/psc/heprdweb/EMPLOYEE/SA/c/UWO_RECORDS_UP2.WSA_ES_GRADE_LIST.GBL"
    formData = {
        "httpPort2": "",
        "timezoneOffset": 300,
        "ptmode": "f",
        "ptlangcd": "ENG",
        "ptinstalledlang": "ENG",
        "userid": userid,
        "pwd": password
    }

    s = requests.Session()

    try:
        print("\n\nLogging in...")
        response = s.post(loginURL, data=formData)
        print("\nGetting grades...\n")
        icsidResponse = s.get(icsidURL)
        icsid = getICSID(icsidResponse.text)
        termsResponse = s.get(GetGradesURL)

        if isTermSelected == False:

            terms = getTerms(termsResponse.text)

            print("Select which term you want:")
            print("(For example, type 0)\n")
            for i in range(len(terms[0])):
                print(str(i)+" : "+str(terms[0][i]))
            termSelectedIndex = input("\n")

            print("Selected " + str(terms[0][int(termSelectedIndex)])+"\n")

            termValue = terms[1][int(termSelectedIndex)]

            isTermSelected = True

        changeYearFormData = {
            "ICAction": "DERIVED_AA2_DERIVED_LINK3",
            "ICModelCancel": "0",
            "ICXPos": "0",
            "ICYPos": "0",
            "ResponsetoDiffFrame": "-1",
            "TargetFrameName": "None",
            "FacetPath": "None",
            "ICFocus": "",
            "ICSaveWarningFilter": "0",
            "ICChanged": "-1",
            "ICSkipPending": "0",
            "ICAutoSave": "0",
            "ICResubmit": "0",
            "ICSID": str(icsid),
            "ICAGTarget": "true",
            "ICActionPrompt": "false",
            "ICBcDomData": "UnknownValue",
            "ICPanelHelpUrl": "",
            "ICPanelName": "",
            "ICFind": "",
            "ICAddCount": "",
            "ICAppClsData": "",
            "DERIVED_AA3_DERIVED_STERM": str(termValue)
        }

        data = s.post(URLChangeYear, data=changeYearFormData)
        stringData = str(data.text)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Something went wrong\n")
        print(exc_type, fname, exc_tb.tb_lineno)
        print(e)
        for remaining in range((delay), 0, -1):
            print(' ' * 40, end='\r')
            print("Trying again in " + str(remaining),
                  "seconds.", end="\r")
            sys.stdout.flush()
            time.sleep(1)
        continue

    returnedTuple = htmlExtractor(
        stringData, currentMarks, filename, selectedCourses)

    currentMarks = returnedTuple[0]
    selectedCourses = returnedTuple[1]
    timer = delay

    for remaining in range(delay, 0, -1):
        print(' ' * 40, end='\r')
        print("Trying again in " + str(remaining),
              "seconds.", end="\r")
        sys.stdout.flush()
        time.sleep(1)
