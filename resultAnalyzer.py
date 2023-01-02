from datetime import datetime
from actionWhenChange import *
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style


def analyzeList(list, titles, currentMarks, n):

    colorama_init()

    for i in range(len(list)):
        if list[i] == '''\xa0''':
            list[i] = "N/A"

    for i in range(len(titles)):
        if "&amp;" in titles[i]:
            titles[i] = titles[i].replace("&amp;", "&")

    f = open("logs.txt", "a")
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    for i in range(n):
        if list[i] != "N/A":
            print(Fore.GREEN + str(titles[i]) +
                  ' : ' + str(list[i])+Style.RESET_ALL)
        else:
            print(titles[i], ":", list[i])
    f.write("\n")
    f.write(str(list))
    f.close()

    if list == ['']*n:
        print("Timeout")
        print("\n\n")
        return currentMarks

    if currentMarks == [] or currentMarks == ['']:
        print("Grades available:", n-int(list.count("N/A")))
        print("\n\n")
        return list

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
        print("Grades available:", n-int(list.count("N/A")))
        print("\n\n")
        return list
    else:
        print("No change detected.")
        print("Grades available:", n-int(list.count("N/A")))
        print("\n\n")
        return list
