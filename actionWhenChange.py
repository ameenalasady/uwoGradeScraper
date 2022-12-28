from win10toast import ToastNotifier


def action():
    toaster = ToastNotifier()
    toaster.show_toast(
        "MARK UPDATE", "MARKS ARE OUTTTTTTTT", duration=1000)
