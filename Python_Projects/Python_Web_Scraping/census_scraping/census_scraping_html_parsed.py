from selenium import webdriver
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
import json
import lxml
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_census_data():

	# this url is essentially the <iframe> tag within the url of 'http://www.census.gov/mycd/'
	# there is a chrome tool with which you can view the elements with <frame> and <iframe>
	# within a new tab
	url = 'http://www.census.gov/mycd/application/'

	# initialize the virtual display (invisible but functional)	
	display = Display(visible=0, size=(800, 600))
	display.start()

	# initialize the web browser
	browser = webdriver.Firefox()

	# an implicit wait of 10 seconds
	# so that each line of code will wait at most 10s if the element it tries
	# to retrieve is not accessible
	browser.implicitly_wait(10)
	delay = 10

	# access the root url
	browser.get(url)

	# locate the drop down from which the state should be selected
	state_drop_down = browser.find_element_by_id('ddl_state')

	# find all options in the state drop down menu
	# the first one was ruled out because it is "select a district" text
	states = state_drop_down.find_elements_by_tag_name('option')[1:]
	
	# all_states_data returned as a dictionary
	all_states_data = {}

	state_index = 0
	while  state_index < len(states):
	# for state_index in range (0, len(states)):
	# for state in states:
		# select a state
		state = states[state_index]
		state.click()
		time.sleep(3)
		# WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'ddl_geo_level_2')))
		print state.text

		# locate the dropdown menu where district is selected
		district_drop_down = browser.find_element_by_id('ddl_geo_level_2')

		# find all options in the district dropdown menu
		# first element also excluded
		districts = district_drop_down.find_elements_by_tag_name('option')[1:]
		
		# the data of each state is also a dictionary
		state_data = {}
		all_states_data[state.text] = state_data

		# for district in districts:
		district_index = 0
		while district_index < len(districts):
			flag = True
			while flag:
				try:
					district = districts[district_index]
					district.click()
					time.sleep(5)
					# WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'text_box')))
					print district.text

					# each district's data is also a dictionary
					district_data = {}
					state_data[district.text] = district_data
					
					people_button = browser.find_element_by_id('people_button')
					people_button.click()
					WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'people')))
					people_html = browser.page_source
					district_data['people'] = _parse_data(people_html, 'people')

					jobs_button = browser.find_element_by_id('employment_button')
					jobs_button.click()
					WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'employment')))
					jobs_html = browser.page_source
					district_data['jobs'] = _parse_data(jobs_html, 'employment')

					housing_button = browser.find_element_by_id('housing_button')
					housing_button.click()
					WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'housing')))
					housing_html = browser.page_source
					district_data['housing'] = _parse_data(housing_html, 'housing')

					economic_button = browser.find_element_by_id('financial_button')
					economic_button.click()
					WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'financial')))
					economic_html = browser.page_source
					district_data['economic'] = _parse_data(economic_html, 'financial')

					education_button = browser.find_element_by_id('education_button')
					education_button.click()
					WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'education')))
					education_html = browser.page_source
					district_data['education'] = _parse_data(education_html, 'education')


					flag = False
				except:
					print 'exception met'
					print 'reseting'
					reset_data =  _reset(browser, url, states, state_index)
					browser = reset_data[0]
					states = reset_data[1]
					districts = reset_data[2]
			district_index += 1
		state_index += 1

	browser.quit()
	display.stop()

	return all_states_data

def _parse_data(html, html_id):
	result = {}
	soup = BeautifulSoup(html,'lxml')
	rows = soup.find_all('tr')
	current_sub_table = ''
	for row in rows:
		if row.find('th'):
			current_sub_table = row.find_all('th')[0].contents[0]
			result[current_sub_table] = {}
		else:
			table_data = row.find_all('td')
			if len(table_data) == 2:
				key = table_data[0].string
				value = table_data[1].contents[0]
				result[current_sub_table][key] = value
			else:
				break
	# time.sleep(3)
	return result

def _reset(driver, url, states, state_index):
	driver.get(url)
	state_drop_down = driver.find_element_by_id('ddl_state')
	states = state_drop_down.find_elements_by_tag_name('option')[1:]
	state = states[state_index]
	state.click()
	district_drop_down = driver.find_element_by_id('ddl_geo_level_2')	
	districts = district_drop_down.find_elements_by_tag_name('option')[1:]
	result = []
	result.append(driver)
	result.append(states)
	result.append(districts)
	return result







if __name__ == '__main__':
    data = get_census_data()

    with open('selenium.JSON', 'w') as outfile:
        json.dump(data, outfile, indent=4)

