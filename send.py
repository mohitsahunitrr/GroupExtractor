import csv
from datetime import datetime
import time
import random


def sendFromCSV(inputfile, logfile, dateformat, csv_delimiter, message_sending_rate, driv):
    with open(inputfile, 'r') as csvfile:
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
            try:
                chat = driv.get_chat_from_phone_number(number)
                if chat:
                    chat.send_message(message)
                    writer.writerow([number, message, "Success"])
                else:
                    writer.writerow([number, message, "Failed"])
            except:
                writer.writerow([number, message, "Failed"])

        ofile.close()
        csvfile.close()
