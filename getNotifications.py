import webwhatsapi
from webwhatsapi.objects.message import NotificationMessage
import csv
import time

print("Scan QR")
driv = webwhatsapi.WhatsAPIDriver(loadstyles=True)
##Scan QR Now
print('Exporting...')
##Get all chats
chats = driv.get_all_chats()

while len(chats) == 0:
    time.sleep(4)
    print('Retrying...')
    chats = driv.get_all_chats()


##Filter Group chats
def convertStr(text):
    return str(text.encode('utf-8').decode('ascii', 'ignore')) if text else "(empty)"


def processNotifications(notif):
    print notif

while True:
    chats = driv.get_unread(include_me=True, include_notifications=True)
# chats = driv.get_unread()
    for i in chats:
        notifications = filter(lambda message: type(message) == NotificationMessage, i.messages)
        for j in reversed(notifications):
            processNotifications(j)
    time.sleep(5)