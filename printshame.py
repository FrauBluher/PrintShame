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
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))


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
        first_form_raw = self.opener.open("https://support.soe.ucsc.edu/printing-reports/user")

        #Looking for the following string name="form_build_id"
        first_form = first_form_raw.read().decode('utf-8')
        index = first_form.index('form_build_id')
        id = first_form[index+19:index+56]

        #Header data construction.
        data = urllib.parse.urlencode({
                'start_date': self.yesterday(), 'end_date': self.today(),
                'op': 'Update+Report', 'form_build_id': id, 'form_id': 'soe_printing_user'
                })
        data = data.encode('utf-8')

        #Get user reports from Today to Yesterday.
        second_form_raw = self.opener.open("https://support.soe.ucsc.edu/printing-reports/user", data)

        #Decode, find the user info, and extract it.
        second_form = second_form_raw.read().decode('utf-8')
        index2 = first_form.index('odd')
        
        #RegEx Voodoo starts here.
        top_ten = second_form[index2:index2+2700]
        raw_printers = re.findall(r'((?<=\">|g>)[A-z0-9():\s\-\.\,\í]*(?=\</.))', top_ten)
        return(raw_printers)

def main():
    ps = PrintShame()

    output_string = "TOP FIVE SOE PRINTERS LAST 24 HRs...\n "

    printers_list = PrintShame.get_printers_list(ps)
    i = 0
    for j in range(5):
        output_string += printers_list[i] + "    Pages:" + printers_list[i+1] + "\n"
        i += 3

    print(output_string)

if __name__=='__main__':
    main()

