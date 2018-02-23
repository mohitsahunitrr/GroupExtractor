import time

from six.moves import input

import extractGroupEvents_config
import send_config
import webwhatsapi
from extractGroupEvents import ExtractGroupEvents
from listGroupMembers import listGroupMembers
from send import sendFromCSV

print("Scan QR")
driv = webwhatsapi.WhatsAPIDriver(loadstyles=True)

# Scan QR Now
print('Sending...')

# Get all chats
chats = driv.get_all_chats()

# Make sure webwhatsapp has completely loaded
while len(chats) == 0:
    time.sleep(4)
    print('Retrying...')
    chats = driv.get_all_chats()

while True:
    options = [
        {
            'desc': "Extract Group Events",
            'function': lambda: ExtractGroupEvents(filename=extractGroupEvents_config.filename,
                                                   dateformat=extractGroupEvents_config.dateformat, driv=driv),
        },
        {
            'desc': "Send Messages from CSV",
            'function': lambda: sendFromCSV(driv=driv, inputfile=send_config.inputfile,
                                            dateformat=send_config.dateformat, csv_delimiter=send_config.csv_delimiter,
                                            logfile=send_config.logfile,
                                            message_sending_rate=send_config.message_sending_rate)
        },
        {
            'desc': "List Group Members",
            'function': lambda: listGroupMembers(driv)
        }
    ]
    for i, v in enumerate(options):
        print(" ".join([str(i), ":", v["desc"]]))
    option = int(input("Pick and option [0-2]"))
    options[option]["function"]