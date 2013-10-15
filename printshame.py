#!/usr/bin/python3.3
#Gets and updates new stuff

import urllib.parse, urllib.request, datetime
import http.cookiejar, urllib.request, string

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
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
r = opener.open("https://support.soe.ucsc.edu/printing-reports/user")

#Debugging output
#for cookie in cj:
#	print(cookie)
#	cookieheader = {'cookie':cookie.name + "=" + cookie.value}
#print(cookieheader)

#Looking for the following string name="form_build_id"
firstform = r.read().decode('utf-8')
index = firstform.index('form_build_id')
id = firstform[index+19:index+56]
#print(id)

data = urllib.parse.urlencode({'start_date': Yesterday, 'end_date': Today, 'op': 'Update+Report', 'form_build_id': id, 'form_id': 'soe_printing_user'})
data = data.encode('utf-8')

f = opener.open("https://support.soe.ucsc.edu/printing-reports/user", data)
print(f.read().decode('utf-8'))

#Todo, scrape session ID from initial get, and then send that and the cookie in a new header to get the timespan that I need.
