import csv

from helpers import convertStr, cleanNumber
from helpers import get_valid_filename
from webwhatsapi.objects.chat import GroupChat


def listGroupMembers(chosenGroups):
    for chat in chosenGroups:
        ##Create CSV
        safe_name = convertStr(chat.name)
        ofile = open(get_valid_filename(str(safe_name)) + '.csv', "w")
        writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(['Name', 'Profile Name', 'Phone Number'])
        ##Iterate Through Group Participants
        for participant in chat.get_participants():
            writer.writerow(
                [participant.get_safe_name(), convertStr(participant.push_name), cleanNumber(participant.id)])
        ofile.close()
        print("Done with " + safe_name)
    print("Done")
