import re
from datetime import datetime
from os import listdir

from webwhatsapi.helper import safe_str


def convertStr(text):
    return str(text.encode('utf-8').decode('ascii', 'ignore')) if text else "(empty)"


def cleanNumber(text):
    text = "".join(text.split('@c.us'))
    if text.startswith("91"):
        text = text[2:]
    return text


def searchDir(filename, dateformat):
    regex = re.compile(filename + r'.+\.csv')
    files = listdir('.')
    backups = filter(lambda x: regex.match(x), files)
    if len(backups) > 0:
        try:
            dates = map(lambda x: datetime.strptime(str(x.replace(filename, "").replace(".csv", "")), dateformat),
                        backups)
            index = dates.index(max(dates))
        except:
            # In case of invalid format
            index = 0
        return backups[index]
    else:
        return False


class MultiPicker(npyscreen.NPSApp):
    def __init__(self, options):
        super(MultiPicker, self).__init__()

    def main(self):
        F = npyscreen.Form(name="Choose Groups to extract leaving/removing data", )
        self.ms2 = F.add(npyscreen.TitleMultiSelect, max_height=-2, name="Pick Several",
                         values=[str(i) + ". " + safe_str(x.name) for i, x in enumerate(self.options)],
                         scroll_exit=True)
        F.edit()
        F.exit_editing()

    def get_result(self):
        return [int(x.split('.')[0]) for x in self.ms2.get_selected_objects()]
