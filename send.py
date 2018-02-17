import csv
import random
import time
from datetime import datetime

import webwhatsapi
from send_config import *

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

with open(inputfile, 'rb') as csvfile:
    now = datetime.now()
    ofile = open((logfile + now.strftime(dateformat)).strip() + '.csv', "a+")
    writer = csv.writer(ofile, delimiter=csv_delimiter, quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(['Number', 'Message', 'Status'])
    reader = csv.reader(csvfile, delimiter=csv_delimiter)
    next(reader)
    for row in reader:
        print(row)
        # Throttle
        time.sleep(message_sending_rate * (1 + random.random()))

        # Fetch Message
        number = row[0]
        message = row[1]
        # Send Message
        chat = driv.get_chat_from_phone_number(number)
        if chat:
            chat.send_message(message)
            writer.writerow([number, message, "Success"])
        else:
            writer.writerow([number, message, "Failed"])

    ofile.close()
    csvfile.close()
