import urllib2
from bs4 import BeautifulSoup
import lxml
import json

url = 'https://en.wikipedia.org/wiki/List_of_U.S._state_abbreviations'
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
response = opener.open(url)
soup = BeautifulSoup(response.read(),'lxml')
rows = soup.find_all('table')[0].find_all('tr')[3:]

dictionary = {}
for row in rows:
	try:
		dictionary[row.find_all('td')[0].a.string] = row.find_all('td')[5].span.string
	except:
		continue

with open('states.JSON', 'w') as outfile:
	json.dump(dictionary, outfile, indent=4)