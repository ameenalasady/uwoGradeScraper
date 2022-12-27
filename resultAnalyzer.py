def analyzeList(list, currentMarks):
    from win10toast import ToastNotifier

    for i in range(len(list)):
        if list[i] == '''\xa0>"''':
            list[i] = "N/A"

    f = open("logs.txt", "a")
    print(list)
    f.write(str(list))

    if currentMarks == []:
        return list

    if list != currentMarks:
        toaster = ToastNotifier()
        toaster.show_toast(
            "MARK UPDATE", "MARKS ARE OUTTTTTTTT", duration=1000)
        print("Change detected!")
        f.write("Change detected!")
        print("\n\n")
        f.write("\n\n")
        f.close()
        return list
    else:
        print("No change detected.")
        f.write("No change detected.")
        print("\n\n")
        f.write("\n\n")
        f.close()
        return list
