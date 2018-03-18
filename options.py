options = [
        {
            'desc': "Extract Group Events",
            'function': lambda: ExtractGroupEvents(filename=extractGroupEvents_config.filename,
                                                   dateformat=extractGroupEvents_config.dateformat, chosenGroups=grouppicker(driv)),
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
            'function': lambda: listGroupMembers(grouppicker(driv))
        }
    ]