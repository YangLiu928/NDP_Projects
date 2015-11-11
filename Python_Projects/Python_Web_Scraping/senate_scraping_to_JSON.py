import json
import urllib2
from bs4 import BeautifulSoup
import lxml
import numpy as np
import pandas as pd
import xmldict

url_part_one = 'http://www.senate.gov/legislative/LIS/roll_call_votes/vote1141/vote_114_1_'
url_part_two = '.xml'
count = 0
data = []

while True:
	url = url_part_one+str(count+1).zfill(5)+url_part_two
	try:
		response = urllib2.urlopen(url)
		data.append(xmldict.xml_to_dict(response.read()))
		count+=1
	except urllib2.HTTPError:
		print 'HTTPError occurred'
		break

with open('data_first_three.JSON', 'w') as outfile:
	json.dump(data, outfile,indent = 4)