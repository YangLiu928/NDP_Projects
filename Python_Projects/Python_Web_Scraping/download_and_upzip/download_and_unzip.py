from selenium import webdriver

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", '/zips')
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")

driver = webdriver.Firefox(firefox_profile=profile)
driver.get("http://bea.gov/iTable/bp_download_modern.cfm?pid=4")
all_tables = driver.find_element_by_xpath("//*[@id=\"promptContainer\"]/div/div[2]/a[2]")
all_tables.click()

# driver.find_element_by_xpath("//a[contains(text(), 'DEV.tgz')]").click()