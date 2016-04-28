from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import lxml
import json

def _parse_html(html, file_name):
	result = {}
	soup = BeautifulSoup(html,'lxml')

	keywords = []
	# label = soup.find_all('div', class_ = 'tertiary_section')[-1].find('li').text
	keywords_lists = soup.find_all('ul', class_='plain margin7')
	for keywords_list in keywords_lists:
		words = keywords_list.find_all('li')
		for word in words:
			keywords.append(word.text.lower())

	summary_ps = soup.find(id='main').find_all('p')
	summary = ''

	for p in summary_ps:
		p = p.text
		summary = summary + ' ' + p 

	if len(summary.strip())==0:
		summary = soup.find(id='main').find('h3').next_sibling

	result['file_name'] = file_name[:-4]
	result['summary'] = summary
	result['keywords'] = keywords
	return result




mypath = './112/'
file_names = [f for f in listdir(mypath) if isfile(join(mypath, f))]


data = []
skipped = []

count = 0
for file_name in file_names:
	html = open('./112/' + file_name,'r').read()
	count=count+1
	# if count==10:
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

