
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets

from gui import Ui_MainWindow
import time

from six.moves import input

import extractGroupEvents_config
import send_config
import webwhatsapi
from extractGroupEvents import ExtractGroupEvents
from listGroupMembers import listGroupMembers
from send import sendFromCSV
import sys

options = [
        {
            'desc': "Extract Group Events",
            'function': lambda: ExtractGroupEvents(filename=extractGroupEvents_config.filename,
                                                   dateformat=extractGroupEvents_config.dateformat, driv=driv),
        },
        {
            'desc': "Send Messages from CSV",
            'function': lambda: sendFromCSV(driv=driv, inputfile=send_config.inputfile,
                                            dateformat=send_config.dateformat, csv_delimiter=send_config.csv_delimiter,
                                            logfile=send_config.logfile,
                                            message_sending_rate=send_config.message_sending_rate)
        },
        {
            'desc': "List Group Members",
            'function': lambda: listGroupMembers(driv)
        }
    ]

status = False

class MainWindow(QMainWindow, Ui_MainWindow):
    def dynamic(self):

        for i in options:
            button = QtWidgets.QPushButton(self.verticalLayoutWidget)
            button.setObjectName("pushButton")
            button.setText(i["desc"])
            self.verticalLayout_2.addWidget(button)

        self.updateContent()

    def updateContent(self, *__args):
        self.statuslabel.setText("Connection Status: " + ("Connected" if status else "Not connected"))

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.dynamic()



def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()