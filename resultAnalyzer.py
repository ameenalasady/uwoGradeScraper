from datetime import datetime
from actionWhenChange import action
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
    f.write(str(list))

    if list == ['']*n:
        print("Timeout")
        print("\n\n")
        f.write("\n\n")
        f.close()
        return currentMarks

    if currentMarks == []:
        print("Grades available:", n-int(list.count("N/A")))
        print("\n\n")
        f.write("\n\n")
        f.close()
        return list

    if list != currentMarks:
        action()
        print("Change detected!")
        f.write("Change detected!")
        print("Grades available:", n-int(list.count("N/A")))
        print("\n\n")
        f.write("\n\n")
        f.close()
        return list
    else:
        print("No change detected.")
        f.write("No change detected.")
        print("Grades available:", n-int(list.count("N/A")))
        print("\n\n")
        f.write("\n\n")
        f.close()
        return list
