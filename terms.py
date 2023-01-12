from bs4 import BeautifulSoup


def getTerms(htmldoc):
    soup = BeautifulSoup(htmldoc, "html.parser")

    allOptions = soup.findAll('option')

    for i in range(len(allOptions)):
        if ascii(allOptions[i].string) == ascii('\xa0 '):
            allOptions.pop(i)
            break

    # for i in range(len(allOptions)):
    #     print(str(i)+" : "+ascii(allOptions[i].string))

    termNames = []

    for i in range(len(allOptions)):
        termNames.append(allOptions[i].string)

    termValues = []

    for i in range(len(allOptions)):
        termValues.append(allOptions[i].get("value"))

    return (termNames, termValues)
    # print(allOptions[i].string)

    # return (str(soup.find(id="ICSID").get("value")))
