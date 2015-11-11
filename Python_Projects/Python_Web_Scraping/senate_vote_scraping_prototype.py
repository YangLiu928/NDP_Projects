import json
import urllib2
from bs4 import BeautifulSoup
import lxml
import numpy as np
import pandas as pd

url_part_one = 'http://www.senate.gov/legislative/LIS/roll_call_votes/vote1141/vote_114_1_'
url_part_two = '.xml'
count = 0
#a list of lists, where in each of the element list the first represents 
#the contents of <vote_date> tag, second for <question> tag
#and the third for <vote_question_text> tag
questions = []

while True:
	#constructing the urls to be queried in a systematic way
	url = url_part_one+str(count+1).zfill(5)+url_part_two
	try:
		response = urllib2.urlopen(url)
		#customized parser, the xml parser from lxml is the only parser supported for xmls
		soup = BeautifulSoup(response.read(),'xml')
		#find_all returns a list, in our case the list contains only one element
		#.string returns the text within the tag
		questions.append([])
		questions[count].append(soup.find_all('vote_date')[0].contents[0])
		questions[count].append(soup.find_all('question')[0].contents[0])
		questions[count].append(soup.find_all('vote_question_text')[0].contents[0])
		count+=1
	except urllib2.HTTPError:
		#exception handling for the first query that failed
		print 'HTTPError occurred'
		break

print 'total '+str(count)+ ' urls queried'
data=pd.DataFrame(np.array(questions),columns=['vote_date','question','vote_question_text'])
data.to_csv('senate_vote_questions.csv',index_label = 'index')
print data