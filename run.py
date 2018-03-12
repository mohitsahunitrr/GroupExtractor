import time

from six.moves import input

import extractGroupEvents_config
import send_config
import webwhatsapi
from extractGroupEvents import ExtractGroupEvents
from listGroupMembers import listGroupMembers
from send import sendFromCSV
import sys

def clean_up():
    driv.quit()

def custom_except(tp, val, traceback):
    try:
        clean_up()
    except:
        pass
    return sys.excepthook(tp, val, traceback)

print("Scan QR")
# firefox = os.path.abspath('/home/mukul/.mozilla/firefox/auevaw5q.default/')
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

if driv._profile_path:
    driv.save_firefox_profile(remove_old=True)

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
    print("%s : Exit"%len(options))
    option = int(input("Pick and option [0-%s]: "%len(options)))
    if option == len(options):
        break
    else:
        options[option]["function"]()

clean_up()
