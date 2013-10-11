#!/usr/bin/python3.3
#Gets and updates new stuff

import urllib.parse, urllib.request, datetime

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

#POST and GET http header construction and tx/rx.
data = urllib.parse.urlencode({'start_date': '10/10/2013', 'end_date': '10/11/2013'oki2571uq40e0qqj89hjsm21i5, 'op': 'Update+Report', 'form_build_id': 'form-6d1805fb97b55213757da392f93264c0', 'form_id': 'soe_printing_user'})
data = data.encode('utf-8')

request = urllib.request.Request("https://support.soe.ucsc.edu/printing-reports/user")
request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")

f = urllib.request.urlopen(request, data)
print(f.read().decode('utf-8'))

#Todo, scrape session ID from initial get, and then send that and the cookie in a new header to get the timespan that I need.
