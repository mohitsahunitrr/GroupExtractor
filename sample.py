import webwhatsapi
import csv
from webwhatsapi import GroupChat
print("Scan QR")
driv = webwhatsapi.WhatsAPIDriver()
##Scan QR Now
print('Exporting...')
##Get all chats
chats = driv.get_all_chats()
##Filter Group chats
groupchats = filter(lambda chat:(type(chat) == GroupChat), chats)
##Search Group chat for first occurence of group name given
for chat in groupchats:
	##Create CSV
	safe_name = str(chat.name.encode('utf-8').decode('ascii', 'ignore'))
	ofile  = open(str(safe_name)+'.csv', "wb")
	writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
	writer.writerow(['Name', 'Profile Name', 'Phone Number'])
	##Iterate Through Group Participants
	for participant in chat.get_participants():
	    writer.writerow([participant.name, participant.push_name, participant.id])
	ofile.close()
	print("Done with " + safe_name)
print("Done")
