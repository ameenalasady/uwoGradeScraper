import requests
import time
from datetime import date
from beautifulSoup import htmlExtractor


f = open("info.txt", "r")
userid = str(f.readline())[7:-1:]
password = str(f.readline())[9:-1:]
n = int(str(f.readline())[29::])
delay = int(str(f.readline())[9::])
f.close()

currentMarks = []


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
    response = s.post(loginURL, data=formData)
    data = s.get(dataURL)
    stringData = str(data.text)

    currentMarks = htmlExtractor(stringData, n, currentMarks)

    time.sleep(delay)
