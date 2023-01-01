from win10toast import ToastNotifier
from discord import SyncWebhook


def action():
    toaster = ToastNotifier()
    toaster.show_toast(
        "MARK UPDATE", "MARKS ARE OUTTTTTTTT", duration=1000)


# Change this URL
url = "https://discord.com/api/webhooks/XXXXXXXXXXXXXXXXXXXXXXXX"


def sendMessage(message):
    webhook = SyncWebhook.from_url(url)
    webhook.send(message)
