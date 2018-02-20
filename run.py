from send_config import *
import csv
import time

import webwhatsapi

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
