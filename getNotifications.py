from __future__ import print_function
import webwhatsapi
from webwhatsapi import GroupChat
from webwhatsapi.objects.message import NotificationMessage
from webwhatsapi.helper import safe_str
import csv
import time
from datetime import datetime
import npyscreen
import logging
import ipdb

def convertStr(text):
    return str(text.encode('utf-8').decode('ascii', 'ignore')) if text else "(empty)"

def cleanNumber(text):
    text = "".join(text.split('@c.us'))
    if text.startswith("91"):
        text = text[2:]
    return text

#!/usr/bin/env python
# encoding: utf-8

logger = logging.getLogger("Get Notifications")


class NotificationExtractor(npyscreen.NPSApp):
    filename="removals.csv"
    def getProgress(self):
        try:
            with open(self.filename, 'rb') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                last = max([datetime.strptime(row[4], "%d/%m/%y %H:%M") for row in reader])

            logger.info('Detected backup, continuing progress...')
            return last
        except:
            logger.info('No backup, running from the beginning...')
            return None

    def writeToFile(self, chosenGroups, last):
        ofile = open('removals.csv', "a+")
        writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(['Group Name', 'Profile Name', 'Phone Number', 'Type', 'Date'])
        if not last:
            last = datetime.min
        for i in chosenGroups:
            name = safe_str(i.name)
            notifications = filter(lambda message: isinstance(message, NotificationMessage),
                                   i.get_messages(include_notifications=True, include_me=True))
            for j in reversed(notifications):
                if j.timestamp < last:
                    print("Done with: " + name)
                    break
                if j.type == 'gp2':
                    if j.subtype == 'leave' or j.subtype == 'remove':
                        profile = j.recipients[0]
                        if isinstance(profile, basestring):
                            writer.writerow([name, "Not in Contacts", cleanNumber(profile), j.subtype,
                                             j.timestamp.strftime("%d/%m/%y %H:%M")])
                        else:
                            writer.writerow([name, profile.name, cleanNumber(profile.id), j.subtype,
                                             j.timestamp.strftime("%d/%m/%y %H:%M")])

        ofile.close()

    def download(self, chosenGroups, last):
        if not last:
            for i in chosenGroups:
                name = safe_str(i.name)
                logger.info("Downloading Group: " + name)
                i.load_all_earlier_messages()
                logger.info("Completed.")

        else:
            for i in chosenGroups:
                name = safe_str(i.name)
                logger.info("Downloading Group: " + name)
                i.load_earlier_messages_till(last)
                logger.info("Completed.")

    def main(self):
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

        chats = driv.get_all_chats()
        groupchats = filter(lambda chat: isinstance(chat, GroupChat), chats)

        F  = npyscreen.Form(name = "Choose Groups to extract leaving/removing data",)
        ms2= F.add(npyscreen.TitleMultiSelect, max_height =-2, name="Pick Several",
        values = [ str(i) + ". "+safe_str(x.name) for i,x in enumerate(groupchats)], scroll_exit=True)
        F.edit()
        F.exit_editing()
        chosenGroups = [ groupchats[int(x.split('.')[0])] for x in ms2.get_selected_objects() ]
        last = self.getProgress()
        logger.info("Last backed up: ", last)
        self.download(chosenGroups, last)
        self.writeToFile(chosenGroups, last)

if __name__ == "__main__":
    App = NotificationExtractor()
    App.run()