import re
from datetime import datetime
from os import listdir
from webwhatsapi.objects.chat import GroupChat
import npyscreen

from webwhatsapi.helper import safe_str


def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

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
    backups = list(filter(lambda x: regex.match(x), files))
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

def multipicker(options):
    def options_factory(options):
        def fun(*args):
            F = npyscreen.Form(name="Choose Groups to extract leaving/removing data", )
            ms2 = F.add(npyscreen.TitleMultiSelect, max_height=-2, name="Pick Several",
                        values=[str(i) + ". " + safe_str(x.name) for i, x in enumerate(options)],
                        scroll_exit=True)
            F.edit()
            F.exit_editing()
            return [int(x.split('.')[0]) for x in ms2.get_selected_objects()]

        return fun
    x = npyscreen.wrapper_basic(options_factory(options))
    return [options[x] for x in x]

def grouppicker(driv):
    chats = driv.get_all_chats()
    groupchats = list(filter(lambda chat: isinstance(chat, GroupChat), chats))
    return multipicker(groupchats)