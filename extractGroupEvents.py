from __future__ import print_function

import csv
import sys
import logging as logger
from collections import defaultdict
from datetime import datetime

from helpers import cleanNumber, searchDir, MultiPicker, safe_str
from webwhatsapi.objects.chat import GroupChat
from webwhatsapi.objects.message import NotificationMessage
import webwhatsapi


#!/usr/bin/env python
# encoding: utf-8



def ExtractGroupEvents(driv, filename, dateformat):
    def getProgress():
        last = defaultdict(lambda :datetime.min)
        fname = searchDir(filename, dateformat)
        if fname:
            try:
                with open(fname, 'rb') as csvfile:
                    reader = csv.reader(csvfile)
                    # skipping first row(Column labels)
                    next(reader)
                    for row in reader:
                        last[row[0]] = max(last[row[0]], datetime.strptime(row[4], dateformat))

                logger.info('Detected backup, continuing progress...')
                return last
            except:
                logger.info('No backup, running from the beginning...')
                return None
        else:
            logger.info('No backup, running from the beginning...')
            return None

    def writeToFile(chosenGroups, last):
        now = datetime.now()
        ofile = open((filename+now.strftime(dateformat)).strip()+'.csv', "a+")
        writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        if not last:
            writer.writerow(['Group Name', 'Profile Name', 'Phone Number', 'Type', 'Date', 'By', 'By P.No'])
            last = defaultdict(lambda: datetime.min)

        for i in chosenGroups:
            name = safe_str(i.name)
            notifications = list(filter(lambda message: isinstance(message, NotificationMessage),
                                   i.get_messages(include_notifications=True, include_me=True)))
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
                        profileid = profile if isinstance(profile, basestring) else profile.id
                        writer.writerow([name, profilename, cleanNumber(profileid), j.subtype,
                                             j.timestamp.strftime(dateformat), adminname, cleanNumber(adminnum)])
            logger.info("Written: " + name)

        ofile.close()

    def download(chosenGroups, last):
        for i in chosenGroups:
            name = safe_str(i.name)
            date = datetime.now()
            beginning = not last or last[i.name]==datetime.min
            logger.info("======= %s Scanning %s From <%s>====" % (date.strftime(dateformat), name, last[name].strftime(dateformat) if not beginning else "Beginning"))
            if beginning:
                i.load_all_earlier_messages()
            else:
                i.load_earlier_messages_till(last[name])
            logger.info("%s Completed." % name)

    def grouppicker():
        chats = driv.get_all_chats()
        groupchats = list(filter(lambda chat: isinstance(chat, GroupChat), chats))
        picker = MultiPicker(groupchats)
        picker.run()
        return [groupchats[x] for x in picker.get_result()]

    logger.basicConfig(filename='progress.log', level=logger.INFO)
    chosenGroups = grouppicker()
    last = getProgress()
    download(chosenGroups, last)
    writeToFile(chosenGroups, last)
