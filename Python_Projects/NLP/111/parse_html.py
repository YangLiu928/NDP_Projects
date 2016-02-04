from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import lxml
import json

def _parse_html(html, file_name):
	result = {}
	soup = BeautifulSoup(html,'lxml')
	label = soup.find_all('div', class_ = 'tertiary_section')[-1].find('li').text
	summary_ps = soup.find(id='main').find_all('p')
	summary = ''

	for p in summary_ps:
		p = p.text
		summary = summary + ' ' + p 

	if len(summary.strip())==0:
		summary = soup.find(id='main').find('h3').next_sibling

	result['file_name'] = file_name[:-4]
	result['summary'] = summary
	result['policy_area'] = label

	return result




mypath = './111/'
file_names = [f for f in listdir(mypath) if isfile(join(mypath, f))]


data = []
skipped = []

count = 0
for file_name in file_names:
	html = open('./111/' + file_name,'r').read()
	count=count+1
	# if count==500:
	# 	break
	print 'processing document #' + str(count)
	try:
		new_data = _parse_html(html,file_name)
		if len(new_data['summary'].strip())==0:
			skipped.append(file_name)
		else:
			data.append(new_data)
	except:
		# raise
		skipped.append(file_name)
		print 'exception at ' + file_name
		continue


with open('data.json','w') as outfile:
	json.dump(data,outfile,indent=4)

with open('skipped.json','w') as outfile:
	json.dump(skipped,outfile,indent=4)

