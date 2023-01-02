import requests
import time
import os
from beautifulSoup import htmlExtractor


f = open("info.txt", "r")
userid = str(f.readline())[7:-1:]
password = str(f.readline())[9:-1:]
n = int(str(f.readline())[29::])
delay = int(str(f.readline())[9::])
f.close()

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

    currentMarks = htmlExtractor(stringData, n, currentMarks)

    time.sleep(delay)
