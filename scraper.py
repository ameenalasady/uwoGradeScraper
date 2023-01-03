import requests
import time
import os
from beautifulSoup import htmlExtractor


f = open("info.txt", "r")

for i in range(4):
    f.readline()

userid = str(f.readline())[7:-1:]
password = str(f.readline())[9:-1:]

for i in range(2):
    f.readline()
n = int(str(f.readline())[16::])

for i in range(2):
    f.readline()

delay = int(str(f.readline())[6::])

for i in range(3):
    f.readline()

courses = (str(f.readline()))[8::]

if courses == "":
    courses = []
    for i in range(n):
        courses.append(i)
else:

    courses = courses.split(",")
    courses = [int(x) for x in courses]


f.close()

didCoursesChange = False

os.chdir("cache")

c = open("lastCourses.txt", "r")


if str(courses) != str(c.read()):
    if not ((str(courses) == "" and str(c.read()) == [i for i in range(n)]) or (str(courses) == [i for i in range(n)] and str(c.read()) == "")):
        c.close()
        c = open("lastCourses.txt", "w")
        c.write(str(courses))
        didCoursesChange = True
        print("Courses have been changed")

c.close()

os.chdir("..")
with open("logs.txt", "rb") as file:
    try:
        file.seek(-2, os.SEEK_END)
        while file.read(1) != b'\n':
            file.seek(-2, os.SEEK_CUR)
    except:
        file.seek(0)
    lastline = file.readline().decode()

currentMarks = lastline[1:-1].replace("'", '').replace(" ", "").split(",")

if currentMarks == ['']:
    currentMarks == []


while (True):

    loginURL = "https://student.uwo.ca/psp/heprdweb/?&cmd=login&languageCd=ENG"
    dataURL = "https://student.uwo.ca/psc/heprdweb/EMPLOYEE/SA/c/UWO_RECORDS_UP2.WSA_ES_GRADE_LIST.GBL"
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
        response = s.post(loginURL, data=formData)
        data = s.get(dataURL)
        stringData = str(data.text)
    except:
        stringData = ""

    currentMarks = htmlExtractor(
        stringData, currentMarks, courses, didCoursesChange)

    time.sleep(delay)
