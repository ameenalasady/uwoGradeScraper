from bs4 import BeautifulSoup
from resultAnalyzer import analyzeList


def htmlExtractor(htmldoc, currentMarks, courses, didCoursesChange):
    marks = []
    titles = []

    soup = BeautifulSoup(htmldoc, "html.parser")

    for i in courses:
        lookFor = "WSA_ENROLMNT_CRSE_GRADE_OFF$"+str(i)
        lookforTitle = "WSA_ENROLMNT_DESCR$"+str(i)

        marks.append(str(soup.find(id=lookFor))[68+(i//10):-7])
        titles.append(str(soup.find(id=lookforTitle))[59+(i//10):-7])

    return analyzeList(marks, titles, currentMarks, courses, didCoursesChange)
