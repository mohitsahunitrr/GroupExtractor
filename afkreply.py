import time
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message
from webwhatsapi.objects.chat import UserChat

afkmessage = "I'm outside right now. Will be back in an hour."
driver = WhatsAPIDriver(loadstyles=True)
print("Waiting for QR")
driver.wait_for_login()

print("Bot started")

def loop():
    time.sleep(3)
    print('Checking for more messages')
    tobeunread = []
    for chat in driver.get_unread():
        for i in chat.messages:
            tobeunread.append(i.id)
        if isinstance(chat.chat, UserChat):
            chat.chat.send_message(afkmessage)

def done():
    for i in tobeunread:
        driver.get

if __name__ == "__main__":
    while True:
        loop()
    done()
