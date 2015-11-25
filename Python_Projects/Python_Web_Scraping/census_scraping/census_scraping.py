from selenium import webdriver
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
import json

url = 'http://www.census.gov/mycd/application/'
results = []
# initialize virtual display
display = Display(visible=0, size=(800, 600))
display.start()

# initialize webdriver (broswer)
browser = webdriver.Firefox()
browser.implicitly_wait(15)
browser.get(url)

state_drop_down = browser.find_element_by_id('ddl_state')
# find all options in the state drop down menu
# the first one was ruled out because it is "select a district" text
states = state_drop_down.find_elements_by_tag_name('option')[1:]

all_states_data = {}
for state in states:
	state.click()
	print state.text
	district_drop_down = browser.find_element_by_id('ddl_geo_level_2')
	districts = district_drop_down.find_elements_by_tag_name('option')[1:]
	state_data = {}
	all_states_data[state.text] = state_data
	for district in districts:
		try:
			print district.text
			district.click()
			district_data = {}
			state_data[district.text] = district_data
			
			people_button = browser.find_element_by_id('people_button')
			people_button.click()
			people_html = browser.page_source
			district_data['people'] =people_html
			print 'people data retrieved'


			jobs_button = browser.find_element_by_id('employment_button')
			jobs_button.click()
			jobs_html = browser.page_source
			district_data['jobs'] = jobs_html
			print 'job data retrieved'

			housing_button = browser.find_element_by_id('housing_button')
			housing_button.click()
			housing_html = browser.page_source
			district_data['housing'] = housing_html
			print 'housing data retrieved'
			
			economic_button = browser.find_element_by_id('financial_button')
			economic_button.click()
			economic_html = browser.page_source
			district_data['economic'] = economic_html
			print 'economic data retrieved'

			education_button = browser.find_element_by_id('education_button')
			education_button.click()
			education_html = browser.page_source
			district_data['education'] = education_html
			print 'education data retrieved'
		except:
			continue

with open('selenium_scraping.JSON', 'w') as outfile:
    json.dump(all_states_data, outfile, indent=4)

browser.quit()
display.stop()