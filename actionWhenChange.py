from win10toast import ToastNotifier
from discord import SyncWebhook


def action():
    toaster = ToastNotifier()
    toaster.show_toast(
        "MARK UPDATE", "MARKS ARE OUTTTTTTTT", duration=1)
    # Changing the duration to a big number will delay the program from running by however much duration is.


# Change this URL
url = "https://discord.com/api/xxxxxxxxxxxxxxxxxxxxxxxxxxx"


def sendMessage(message, number, title):
    webhook = SyncWebhook.from_url(url)
    webhook.send(message + " " + str(number) +
                 " in " + str(title) + "!" + " W or L?")
