import webwhatsapi
import csv
from webwhatsapi import GroupChat
print("Scan QR")
driv = webwhatsapi.WhatsAPIDriver()
##Scan QR Now
name = raw_input("Enter Name of Group: ")
##Get all chats
chats = driv.get_all_chats()
##Filter Group chats
groupchats = filter(lambda chat:(type(chat) == GroupChat), chats)
##Search Group chat for first occurence of group name given
chat = next(x for x in groupchats if x.name == name)
##Create CSV
ofile  = open('output.csv', "wb")
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerow(['Name', 'Profile Name', 'Phone Number'])
##Iterate Through Group Participants
for participant in chat.get_participants():
    writer.writerow([participant.name, participant.push_name, participant.id])
ofile.close()
print("Done")
