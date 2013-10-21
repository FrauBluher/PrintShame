#!/usr/bin/python3.3
#Gets and updates new stuff

import urllib.parse, urllib.request, datetime
import http.cookiejar, urllib.request, string, re

__author__ = "Pavlo Manovi"
__copyright__ ="Copyright (C) 2013 Pavlo Manovi"
__license__ = "The MIT License (MIT)"

class PrintShame:
#HI ARI!
    def __init__(self):
        self.Now = datetime.datetime.now()
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))


    def today(self):
        return(str(self.Now.month) + '/' + str(self.Now.day) + '/' + str(self.Now.year))

    def yesterday(self):
        month = self.Now.month
        day = self.Now.day
        year = self.Now.year

    #Make sure that day subtraction wraps around months and years properly.
    #Leap year isn't implemented here because I'm lazy.
        if day == 1:
            if month == 1:
                year = year -1
                month = 12
                day = 31
            elif month == (2 or 4 or 6 or 8 or 9 or 11):
                month = month -1
                day = 31
            elif month == (5 or 7 or 10):
                month = month -1
                day = 30
            else:
                month = month -1
                day = 28
        else:
            day = day -1

        return(str(month) + '/' + str(day) + '/' + str(year))

    def get_printers_list(self):
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        r = opener.open("https://support.soe.ucsc.edu/printing-reports/user")

        #Looking for the following string name="form_build_id"
        firstform = r.read().decode('utf-8')
        index = firstform.index('form_build_id')
        id = firstform[index+19:index+56]

        #Header data construction.
        data = urllib.parse.urlencode({'start_date': self.yesterday(), 'end_date': self.today(), 'op': 'Update+Report', 'form_build_id': id, 'form_id': 'soe_printing_user'})
        data = data.encode('utf-8')

        #Get user reports from Today to Yesterday.
        f = opener.open("https://support.soe.ucsc.edu/printing-reports/user", data)

        #Decode, find the user info, and extract it.
        secondform = f.read().decode('utf-8')
        index2 = firstform.index('odd')
        topten = secondform[index2:index2+2700]
        m = re.findall(r'((?<=\">|g>)[A-z0-9():\s\-\.\,\í]*(?=\</.))', topten)
        return(m)

def main():
    ps = PrintShame()

    outputString = "TOP FIVE SOE PRINTERS LAST 24 HRs...\n "

    printersList = PrintShame.get_printers_list()
    i = 0
    for j in range(5):
        outputString += printersList[i] + "    Pages:" + printersList[i+1] + "\n"
        i += 3

    print(outputString)

if __name__==__"main"__:
    main()

