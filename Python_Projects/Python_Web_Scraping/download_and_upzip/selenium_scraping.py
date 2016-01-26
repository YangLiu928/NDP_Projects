from selenium import webdriver
from pyvirtualdisplay import Display
# This scrpit currently only works in Linux environment
# and requires installation of xvfb, pyvirtualdisplay and selenium

# This is intended to be used as a prototype for 
# headless scraping using Firefox as webdriver.
# Using PhantomJS as webdriver should be a valid 
# alternative to this, but finding elements in
# PhantomJS browser somehow always returns exceptions 

# initialize virtual display
display = Display(visible=0, size=(800, 600))
display.start()

# initialize webdriver (broswer)
browser = webdriver.Firefox()

url = 'http://www.python.org'
browser.get(url)

# find the search input field
input = browser.find_element_by_name('q')

# send string to the input field
input.send_keys('dictionary')

# find the search button
submit_button = browser.find_element_by_id('submit')

# click on the button and do the search
submit_button.click()

# the webpage now jumps to the search results
# get the html page source
html = browser.page_source

# TODO: extract results with the html contents
print html

# close the virtual display and the webdriver (browser)
browser.quit()
display.stop()