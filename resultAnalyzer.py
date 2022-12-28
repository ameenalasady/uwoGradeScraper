from datetime import datetime
from actionWhenChange import action


def analyzeList(list, currentMarks, n):

    for i in range(len(list)):
        if list[i] == '''\xa0>"''':
            list[i] = "N/A"

    f = open("logs.txt", "a")
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), list)
    f.write(str(list))

    if list == ['']*n:
        print("Timeout")
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
