import webwhatsapi
import csv
from webwhatsapi import GroupChat
print("Scan QR")
driv = webwhatsapi.WhatsAPIDriver(loadstyles=True)
##Scan QR Now
print('Exporting...')
##Get all chats
chats = driv.get_all_chats()
##Filter Group chats
groupchats = filter(lambda chat:(type(chat) == GroupChat), chats)
def convertStr(text):
	return str(text.encode('utf-8').decode('ascii', 'ignore')) if text else "(empty)"
for chat in groupchats:
	##Create CSV
	safe_name = convertStr(chat.name)
	ofile  = open(str(safe_name)+'.csv', "wb")
	writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
	writer.writerow(['Name', 'Profile Name', 'Phone Number'])
	##Iterate Through Group Participants
	for participant in chat.get_participants():
	    writer.writerow([convertStr(participant.name), convertStr(participant.push_name), participant.id])
	ofile.close()
	print("Done with " + safe_name)
print("Done")
