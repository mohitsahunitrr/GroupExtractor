from __future__ import print_function
import webwhatsapi
from webwhatsapi import GroupChat
from webwhatsapi.objects.message import NotificationMessage
from webwhatsapi.helper import safe_str
import csv
import time
import ipdb
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


def convertStr(text):
    return str(text.encode('utf-8').decode('ascii', 'ignore')) if text else "(empty)"

def cleanNumber(text):
    text = "".join(text.split('@c.us'))
    if text.startswith("91"):
        text = text[2:]
    return text

ofile  = open('removals.csv', "wb")
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerow(['Group Name', 'Profile Name', 'Phone Number', 'Type', 'Date'])

chats = driv.get_all_chats()
groupchats = filter(lambda chat: isinstance(chat, GroupChat), chats)
for i in groupchats:
    name = safe_str(i.name)
    print(name)
    i.load_earlier_messages()
    notifications = filter(lambda message: isinstance(message, NotificationMessage), i.get_messages(include_notifications=True, include_me=True))
    for j in reversed(notifications):
        if j.type == 'gp2':
            if j.subtype == 'leave' or j.subtype == 'remove':
                profile = j.recipients[0]
                if isinstance(profile, basestring):
                    writer.writerow([name, "Not in Contacts", cleanNumber(profile), j.subtype, j.timestamp])
                else:
                    writer.writerow([name, profile.name, cleanNumber(profile.id), j.subtype, j.timestamp])

ofile.close()
