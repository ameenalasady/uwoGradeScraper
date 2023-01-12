from datetime import datetime
from actionWhenChange import *
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style


def analyzeList(list, titles, currentMarks, filename, selectedCourses):

    colorama_init()

    for i in range(len(list)):
        if list[i] == '''\xa0''':
            list[i] = "N/A"

    for i in range(len(titles)):
        if "&amp;" in titles[i]:
            titles[i] = titles[i].replace("&amp;", "&")

    if selectedCourses == []:
        print("Select which courses you want to track for changes:\n")
        print("Leave blank to track all courses.")
        for i in range(len(list)):
            print(str(i)+" : "+titles[i])
        temp = input("\nFor example: 0,1,2,4\n")
        if temp == "":
            selectedCourses = [i for i in range(len(list))]
        else:
            selectedCourses = temp.split(",")

    for i in range(len(selectedCourses)):
        selectedCourses[i] = int(selectedCourses[i])

    NewList = list
    NewTitles = titles
    list = []
    titles = []

    for i in range(len(selectedCourses)):
        list.append(NewList[selectedCourses[i]])
        titles.append(NewTitles[selectedCourses[i]])

    f = open(str(filename)+".txt", "a")

    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    for i in range(len(titles)):
        if list[i] != "N/A":
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
        print("Grades available:", len(titles)-int(list.count("N/A")))
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
        print("Grades available:", len(titles)-int(list.count("N/A")))
        print("\n\n")
        return list, selectedCourses
    else:
        print("No change detected.")
        print("Grades available:", len(titles)-int(list.count("N/A")))
        print("\n\n")
        return list, selectedCourses
