import csv
import os


# internal class for tickets
class HDTicket(object):
    # Def Ticket, just here to hel in remembering format
    def __init__(self):
        self.no = 0
        self.subject = ""
        self.request = ""
        self.note = ""
        self.codes = []

    # Main Ticket Type
    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.setValues()
        self.codes = []

    # Creates Values based on the contents of the raw_text
    def setValues(self):
        # its invalid if we can't get the ticket number, will use for filtering
        try:
            self.no = int(self.raw_text[0])
        # if raw_text[0] isn't an int
        except ValueError:
            self.no = None

        self.subject = self.raw_text[1]
        self.request = self.raw_text[2]
        self.note = self.raw_text[3]

    # figures out if this ticket is valid
    def isInvalid(self):
        # Case where a late ticket is sent to help desk
        if "Media Services Checkout" in self.subject:
            return True

        # Invalid number, therefore not a ticket
        if self.no is None:
            return True

        return False

    def rawList(self):
        return [str(self.no), self.subject, self.request, self.note]

    # To help with writing to a file
    def __str__(self):
        return str(self.no) + "\t" + self.subject + "\t" + self.request + "\t" + self.note


def convertFileHD(filename, enc):
    # Holds the ticket's contents
    tickets = []
    # Used for reading file and adding raw data from it
    with open(filename, encoding=enc) as file:
        organized = csv.reader(file, delimiter="\t")
        # avg = 0
        # cou = 0
        for cur in organized:
            # avg+= len(cur)
            # cou+= 1
            tickets.append(HDTicket(cur))
        # print(avg/cou)
    return tickets


def extractContent(content):
    st = ""
    for s in content:
        st += (str(s) + "\n")
    return st


# encoding and filename (this encoding type should work with every help desk .tsv file)
original = "C:\\Users\\megha\\OneDrive\\Desktop\\CLU\\Media_Services\\WHD_Tickets.tsv"
spam = "C:\\Users\\megha\\OneDrive\\Desktop\\CLU\\Media_Services\\SpamHD_Tickets.tsv"
general = "C:\\Users\\megha\\OneDrive\\Desktop\\CLU\\Media_Services\\GeneralHD_Tickets.tsv"
encode = 'utf-8'

# These hold the organized info given the file and the encoding
ori_tickets = convertFileHD(original, encode)
gen_tickets = convertFileHD(general, encode)
spam_tickets = convertFileHD(spam, encode)

# filters invalid request numbers, invalid subjects and spam
usable_tickets = list(filter(lambda ticket: False if (ticket.isInvalid() or
                                                      (ticket in spam_tickets)) else True, gen_tickets))

# Used this to create the new spamless file
""""
with open("C:\\Users\\megha\\OneDrive\\Desktop\\CLU\\Media_Services\\SpamLessHD_Tickets.tsv", 'w') as file:
    file.write(extractContent(usable_tickets))
"""

# TESTING-----------------------------------------------------------------------------------------------------------
# len Tests, number of tickets after filtering

# -print("# of usable Tickets: " + str(len(usable_tickets)))

# Tested if right format
""""
for t in usable_tickets:
    print(str(t) + "\n")
"""
