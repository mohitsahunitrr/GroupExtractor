from __future__ import print_function
import webwhatsapi
from webwhatsapi import GroupChat
from webwhatsapi.objects.message import NotificationMessage
from webwhatsapi.helper import safe_str
import csv
import time
from datetime import datetime
import npyscreen
import logging as logger
from collections import defaultdict
import six
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

logger.basicConfig(filename='progress.log',level=logger.INFO)

class NotificationExtractor(npyscreen.NPSApp):
    filename="removals.csv"
    dateformat="%d/%m/%y %H:%M"

    def getProgress(self):
        last = defaultdict(lambda :datetime.min)
        try:
            with open(self.filename, 'rb') as csvfile:
                reader = csv.reader(csvfile)
                # skipping first row(Column labels)
                next(reader)
                for row in reader:
                    last[row[0]] = max(last[row[0]], datetime.strptime(row[4], self.dateformat))

            logger.info('Detected backup, continuing progress...')
            return last
        except:
            logger.info('No backup, running from the beginning...')
            return None

    def writeToFile(self, chosenGroups, last):

        ofile = open('removals.csv', "a+")
        writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        if not last:
            writer.writerow(['Group Name', 'Profile Name', 'Phone Number', 'Type', 'Date', 'By', 'By P.No'])
            last = defaultdict(lambda: datetime.min)

        for i in chosenGroups:
            name = safe_str(i.name)
            notifications = filter(lambda message: isinstance(message, NotificationMessage),
                                   i.get_messages(include_notifications=True, include_me=True))
            for j in reversed(notifications):
                if j.timestamp < last[name]:
                    break
                if j.type == 'gp2':
                    if j.subtype in ['leave', 'remove', 'add']:
                        profile = j.recipients[0]
                        adminnum = "Unknown"
                        adminname = "Unknown"
                        if isinstance(j.sender, webwhatsapi.Contact):
                            adminnum = j.sender.id
                            adminname = j.sender.get_safe_name()
                        profilename = "Not in Contacts" if isinstance(profile, basestring) else profile.name
                        profileid = "Not in Contacts" if isinstance(profile, basestring) else profile.id
                        writer.writerow([name, profilename, cleanNumber(profileid), j.subtype,
                                             j.timestamp.strftime(self.dateformat), adminname, adminnum])
            logger.info("Written: " + name)

        ofile.close()

    def download(self, chosenGroups, last):
        for i in chosenGroups:
            name = safe_str(i.name)
            date = datetime.now()
            dateformat = "%d-%b-%Y %X"
            beginning = not last or last[i.name]==datetime.min
            logger.info("======= %s Scanning %s From <%s>====" % (date.strftime(dateformat), name, last[name].strftime(dateformat) if not beginning else "Beginning"))
            if beginning:
                i.load_all_earlier_messages()
            else:
                i.load_earlier_messages_till(last[name])
            logger.info("%s Completed." % name)



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
        self.download(chosenGroups, last)
        self.writeToFile(chosenGroups, last)

if __name__ == "__main__":
    App = NotificationExtractor()
    App.run()