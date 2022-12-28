from bs4 import BeautifulSoup
from resultAnalyzer import analyzeList


def htmlExtractor(htmldoc, n, currentMarks):
    marks = []

    soup = BeautifulSoup(htmldoc, "html.parser")

    for i in range(n):
        lookFor = "WSA_ENROLMNT_CRSE_GRADE_OFF$"+str(i)
        marks.append(str(soup.find(id=lookFor))[-8:-11:-1])

    return analyzeList(marks, currentMarks, n)
