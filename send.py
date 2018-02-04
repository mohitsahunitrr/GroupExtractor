import webwhatsapi
import time
import csv

print("Scan QR")
driv = webwhatsapi.WhatsAPIDriver(loadstyles=True)
##Scan QR Now
print('Sending...')
##Get all chats
chats = driv.get_all_chats()

while len(chats) == 0:
    time.sleep(4)
    print('Retrying...')
    chats = driv.get_all_chats()

with open('messages.csv', 'rb') as csvfile:
    ofile = open('status.csv', "a+")
    writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(['Number', 'Status'])
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        number = row[0]
        message = row[1]
        chat = driv.get_chat_from_phone_number(number)
        if chat:
            chat.send_message(message)
            writer.writerow([number, "Success"])
        else:
            writer.writerow([number, "Failed"])

    ofile.close()
    csvfile.close()
