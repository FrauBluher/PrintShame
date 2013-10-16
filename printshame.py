#!/usr/bin/python3.3
#Gets and updates new stuff

import urllib.parse, urllib.request, datetime
import http.cookiejar, urllib.request, string, re

#Get current time information.
Now = datetime.datetime.now()

month = Now.month
day = Now.day
year = Now.year

Today = str(month) + '/' + str(day) + '/' + str(year)

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

Yesterday = str(month) + '/' + str(day) + '/' + str(year)

#Printer object for later use with priting data
class Printer(object):
    ident = ""
    pages = ""
    percentage = ""

    def __init__(self, ident, pages, percentage):
        self.ident = ident
        self.pages = pages
        self.percentage = percentage

def make_printer(ident, pages, percentage):
    printer = Printer(ident, pages, percentage)
    return printer

#POST and GET http header construction and tx/rx.
#Here we make the first handshake to get our cookies.
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
r = opener.open("https://support.soe.ucsc.edu/printing-reports/user")

#Looking for the following string name="form_build_id"
firstform = r.read().decode('utf-8')
index = firstform.index('form_build_id')
id = firstform[index+19:index+56]

#Header data construction.
data = urllib.parse.urlencode({'start_date': Yesterday, 'end_date': Today, 'op': 'Update+Report', 'form_build_id': id, 'form_id': 'soe_printing_user'})
data = data.encode('utf-8')

#Get user reports from Today to Yesterday.
f = opener.open("https://support.soe.ucsc.edu/printing-reports/user", data)

#Decode, find the user info, and extract it.
secondform = f.read().decode('utf-8')
index2 = firstform.index('odd')
topten = secondform[index2:index2+2700]
m = re.findall(r'((?<=\">|g>)[A-z0-9():\s\-\.\,]*(?=\</.))', topten)

print(m)
#for i in range(len(m)-3):
#	make_printer(m[i], m[i+1], m[i+2])


#Todo, scrape session ID from initial get, and then send that and the cookie in a new header to get the timespan that I need.
