import json
import urllib2
from bs4 import BeautifulSoup
import lxml
import numpy as np
import pandas as pd
import re

#this is the starting page where each of the clickable link leads to a table with data
root_url = 'http://clerk.house.gov/evs/2015/index.asp'
#the href attribute in each of the clickable anchor tag is relative, therefore we need the header
#to construct the complete link
url_header = 'http://clerk.house.gov/evs/2015/'
branch_urls = []
response = urllib2.urlopen(root_url)
soup = BeautifulSoup(response.read(),'lxml')
anchors = soup.find_all('a')
#the href attribute of the anchor tags of interest are all in a certain pattern, which can
#be summarized with regular expression
pattern = re.compile('ROLL_[0-5]00.asp')
for anchor in anchors:
	if pattern.match(anchor.get('href')):		
		branch_urls.append(url_header+anchor.get('href'))

print branch_urls



results = []
for url in branch_urls:
	soup = BeautifulSoup(urllib2.urlopen(url).read(),'lxml')
	for row in soup.find_all('tr'):
		if len(row.find_all('td'))==0:
			continue
		roll = row.find_all('td')[0].a.contents[0]
		question = row.find_all('td')[3].font.contents[0]
		description = row.find_all('td')[5].font.contents[0]
		result = [roll,question,description]
		results.append(result)

pd.DataFrame(np.array(results),columns=['Roll','Question','Title/Description']).to_csv('house.csv',index = False,encoding = 'utf-8')



