import csv

from helpers import convertStr, cleanNumber, MultiPicker
from webwhatsapi.objects.chat import GroupChat


def listGroupMembers(driv):
    def grouppicker():
        chats = driv.get_all_chats()
        groupchats = list(filter(lambda chat: isinstance(chat, GroupChat), chats))
        picker = MultiPicker(groupchats)
        picker.run()
        return [groupchats[x] for x in picker.get_result()]

    chosenGroups = grouppicker()

    for chat in chosenGroups:
        try:
            ##Create CSV
            safe_name = convertStr(chat.name)
            ofile = open(str(safe_name) + '.csv', "wb")
            writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(['Name', 'Profile Name', 'Phone Number'])
            ##Iterate Through Group Participants
            for participant in chat.get_participants():
                writer.writerow(
                    [convertStr(participant.name), convertStr(participant.push_name), cleanNumber(participant.id)])
            ofile.close()
            print("Done with " + safe_name)
        except:
            pass
    print("Done")
