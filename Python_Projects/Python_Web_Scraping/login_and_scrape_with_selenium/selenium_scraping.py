from selenium import webdriver
import os
import time
from bs4 import BeautifulSoup
import lxml
import json
import re
import time

# It is important to setup the waiting mechanism properly
# if there is only one URL or link you want to click on a webpage, it is probably OK to simply use the implicit wait
# if there are more than one element or an array of elements you want to retrieve, using an explicity wait is probably the best
# refer waiting mechanisms here: http://selenium-python.readthedocs.org/waits.html
# open up the browser and navigate to the hompage of census.gov


url = 'https://usatrade.census.gov/index.php?do=login'
# set up the webdriver. We use Firefox for tetsing purpose due to its visiability
# during production we may want to use PhantomJS headless webdriver to save system 
# resources and speed up the program
browser = webdriver.Firefox()

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

unparsed_result = []
count = 0
while (True):
	table = browser.find_element_by_id('ContentsTable').text
	unparsed_result.append(table)
	with open('data.json', 'w') as outfile:
		json.dump(unparsed_result[-1], outfile, indent=4)
	try:
		print browser.find_element_by_id('TablePagination').find_elements_by_tag_name('td')[2].text
		while(True):			
			try:
				print '\t' + browser.find_element_by_id('TablePagination').find_elements_by_tag_name('td')[5].text
				arrow_position = 4 - (count%2)
				browser.find_element_by_id('TablePagination')\
				.find_elements_by_tag_name('td')[arrow_position]\
				.find_element_by_tag_name('a').click()
				table = browser.find_element_by_id('ContentsTable').text
				unparsed_result.append(table)
			except:
				count = count + 1
				print 'count = ' + str(count)
				break;
		browser.find_element_by_id('TablePagination')\
		.find_elements_by_tag_name('td')[1]\
		.find_element_by_tag_name('a').click()
		# time_hit+=1
		# print 'times down arrow button hit = ' + str(time_hit)
	except:
		print 'finished'
		break;



# time.sleep(10)
# browser.close()


with open('data.json', 'w') as outfile:
    json.dump(unparsed_result, outfile, indent=4)

