from selenium import webdriver
import os
import time
from bs4 import BeautifulSoup
import lxml
import json
import re
import time


# open up the browser and navigate to the hompage of careerbuilder.com
url = 'https://usatrade.census.gov/index.php?do=login'
# phantomjs_path = '../phantomjs-2.0.0-windows/bin/phantomjs.exe'
browser = webdriver.Firefox()
# browser = webdriver.Chrome('../chromedriver_win32/chromedriver.exe')

# browser = webdriver.PhantomJS(executable_path=phantomjs_path, service_log_path=os.path.devnull)
browser.implicitly_wait(10)
browser.get(url)

# locate the input fields and search buttons
user_id = browser.find_element_by_id('struserid')
user_id.send_keys('8BTJY9B')
password = browser.find_element_by_id('pwdfld')
password.send_keys('1730RhodeIsland!')

login_button = browser.find_element_by_id('btnlogin')
login_button.click()

exports = browser.find_elements_by_link_text('Exports')
exports[0].click()

report_link = browser.find_element_by_link_text('Report')
report_link.click()

table = browser.find_element_by_id('ContentsTable')
print table.get_attribute('innerHTML')

time.sleep(10)
browser.close()




