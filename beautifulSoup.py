from bs4 import BeautifulSoup
from resultAnalyzer import analyzeList


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
