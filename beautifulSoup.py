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

    # for i in courses:
    #     lookFor = "WSA_ENROLMNT_CRSE_GRADE_OFF$"+str(i)
    #     lookforTitle = "WSA_ENROLMNT_DESCR$"+str(i)

    #     marks.append(str(soup.find(id=lookFor))[68+(i//10):-7])
    #     titles.append(str(soup.find(id=lookforTitle))[59+(i//10):-7])

    return analyzeList(marks, titles, currentMarks, filename, selectedCourses)
