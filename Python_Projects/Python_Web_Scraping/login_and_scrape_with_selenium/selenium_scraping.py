from selenium import webdriver
import os
from bs4 import BeautifulSoup
import lxml
import json
import re
import time
from selenium.webdriver.support.ui import Select

def _parse_html(html,result):

	soup = BeautifulSoup(html,'lxml')

	header_table = soup.find(id='headerRowTable')
	header_table_rows = header_table.find_all('tr')

	times = {}

	time_cells = header_table_rows[0].find_all('th')
	for time_cell in time_cells:
		time_id = time_cell['id']
		time_value = time_cell.text
		times[time_id] = time_value
	# time_text = header_table_rows[0].text
	# times[time_id] = time_text

	measures = {}
	for th in header_table_rows[1].find_all('th'):
		id = th['id']
		value = th.text
		measures[id] = value
		# print 'a new measure ' + value

	commodities = {}
	for th in header_table_rows[2].find_all('th'):
		id = th['id']
		value = th.text
		commodities[id]= value
		# print 'a new commodity ' + value

	countries = {}
	trs = soup.find(id='headerColumnTable')
	trs = trs.find_all('tr')
	for tr in trs:
		id = tr.find('th')['id']
		value = tr.text
		countries[id] = value
		# print 'a new country ' + value

	for time_key in times:
		time = times[time_key]
		if time not in result:
			result[time] = {}
		for measure_key in measures:
			measure = measures[measure_key]
			if measure not in result[time]:
				result[time][measure] = {}
			for commodity_key in commodities:
				commodity = commodities[commodity_key]
				if commodity not in result[time][measure]:
					result[time][measure][commodity] = {}

	table = soup.find(id='bodyTD')
	rows = table.find_all('tr')
	for row in rows:
		cells = row.find_all('td')
		for cell in cells:
			features = cell['headers']
			time = times[features[0]]
			measure = measures[features[1]]
			commodity = commodities[features[2]]
			country = countries[features[3]]
			number = cell.text
			result[time][measure][commodity][country]= number
			# print time + '\t' + measure + '\t' + commodity + '\t' + country + '\t' + number

	# return result






# It is important to setup the waiting mechanism properly
# if there is only one URL or link you want to click on a webpage, it is probably OK to simply use the implicit wait
# if there are more than one element or an array of elements you want to retrieve, using an explicity wait is probably the best
# refer waiting mechanisms here: http://selenium-python.readthedocs.org/waits.html
# open up the browser and navigate to the hompage of census.gov

start_time = time.time()
url = 'https://usatrade.census.gov/index.php?do=login'
# set up the webdriver. We use Firefox for tetsing purpose due to its visiability
# during production we may want to use PhantomJS headless webdriver to save system 
# resources and speed up the program
browser = webdriver.Firefox()
# phantomjs_path = './phantomjs-2.0.0-windows/bin/phantomjs.exe'
# browser = webdriver.PhantomJS(executable_path=phantomjs_path, service_log_path=os.path.devnull)

# setting up implicit wait mechanism, here, the webdriver will try to fetch the elements
# for up to 10 seconds until  
browser.implicitly_wait(10)
browser.get(url)

# locate the input fields and login buttons
user_id = browser.find_element_by_id('struserid')
user_id.send_keys('8BTJY9B')

password = browser.find_element_by_id('pwdfld')
password.send_keys('1730RhodeIsland!')

login_button = browser.find_element_by_id('btnlogin')
login_button.click()

# click on the exports anchor tag 
# things may go wrong here because we did "find_elementS", and this function
# treats empty list as a valid result. If the internets is slow and the function
# returns an empty list, our attempt to fetch the element at index = 0 will 
# raise out of bound exception
exports = browser.find_elements_by_link_text('Exports')
exports[0].click()

# click on the report link
# report_link = browser.find_element_by_link_text('Report')
# report_link.click()

# table = browser.find_element_by_id('ContentsTable')
# print table.get_attribute('innerHTML')

# options box represents the <div> on the left hand side of the webpage 
# it includes all the options like commodity, country etc.
options_box = browser.find_element_by_id('ctl00_RadDimensionsTree')
options_box.find_element_by_link_text('Measures').click()
browser.find_element_by_id('AllSelectImage').click()

# each time you click on something, the web page CHANGES
# Therefore you have to find the options box every time after you have
# clicked something
options_box = browser.find_element_by_id('ctl00_RadDimensionsTree')
options_box.find_element_by_link_text('Commodity').click()
browser.find_element_by_id('ctl00_MainContent_RadMembersTree').\
find_elements_by_tag_name('label')[1].find_elements_by_tag_name('input')[1].click()

options_box = browser.find_element_by_id('ctl00_RadDimensionsTree')
options_box.find_element_by_link_text('Country').click()
browser.find_element_by_id('ctl00_MainContent_RadMembersTree').\
find_elements_by_tag_name('label')[0].find_elements_by_tag_name('input')[1].click()


options_box = browser.find_element_by_id('ctl00_RadDimensionsTree')
options_box.find_element_by_link_text('Time').click()
browser.find_element_by_id('ctl00_MainContent_RadMembersTree').\
find_elements_by_tag_name('label')[0].find_elements_by_tag_name('input')[1].click()

report_link = browser.find_element_by_link_text('Report')
report_link.click()

browser.find_element_by_id('anch_368').click()
browser.find_element_by_link_text('Table display settings...').click()

select = Select(browser.find_element_by_id('TableRowPageSizeLB'))
select.select_by_visible_text('200')

# wrapping = browser.find_element_by_id('WrappingOn').click()

browser.find_element_by_name('TableOptionsGo').click()

# time.sleep(5)
result = {}
count = 0
while (True):
	table = browser.find_element_by_id('ContentsTable').get_attribute('innerHTML')
	_parse_html(table,result)
	# print result
	# break 
	try:
		# print browser.find_element_by_id('TablePagination').find_elements_by_tag_name('td')[2].text
		while(True):			
			try:
				# print '\t' + browser.find_element_by_id('TablePagination').find_elements_by_tag_name('td')[5].text
				arrow_position = 4 - (count%2)
				browser.find_element_by_id('TablePagination')\
				.find_elements_by_tag_name('td')[arrow_position]\
				.find_element_by_tag_name('a').click()
				table = browser.find_element_by_id('ContentsTable').get_attribute('innerHTML')
				_parse_html(table,result)
			except:
				count = count + 1
				# print 'count = ' + str(count)
				break
		browser.find_element_by_id('TablePagination')\
		.find_elements_by_tag_name('td')[1]\
		.find_element_by_tag_name('a').click()
		# time_hit+=1
		# print 'times down arrow button hit = ' + str(time_hit)
	except:
		print 'total run time = ' + str(time.time()-start_time)
		break



# time.sleep(10)
# browser.close()


with open('data2.json', 'w') as outfile:
    json.dump(result, outfile, indent=4)





