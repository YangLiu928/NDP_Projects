import urllib2
from bs4 import BeautifulSoup
import json
import re
import xmldict
import lxml
import pprint

# finger print for the websites used to scrape house data
# used to determine whether web structure has changed before going further for the scraping
WEBSITE_FINGER_PRINT = ''

# url used for house representative list scraping
SENATE_REPRESENTATIVE_LIST_URL = 'http://www.senate.gov/general/committee_assignments/assignments.htm'


def get_current_senate_representative_data():
    results = []
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    url = SENATE_REPRESENTATIVE_LIST_URL
    response = opener.open(url)
    bs_object = BeautifulSoup(response.read(),'lxml')

    # remove the first TWO rows because they are table headers
    rows = bs_object.find('table').find_all('tr')[2:]
    for row in rows:
        if row.find_all('td')[0].find('a'):
            result = {}        
            result['name'] = row.find_all('td')[0].find('a').string
            print result['name']
            unprocessed_party_and_state = re.search('\((.+?)\)',str(row.find_all('td')[0].contents[-1])).group()[1:-1]
            result['state'] = unprocessed_party_and_state[-2:]
            result['party'] = unprocessed_party_and_state[0]
            result['committees'] = []
            for committee in row.find_all('td')[1].find_all('a'):
                result['committees'].append(committee.string)
            results.append(result)
    return results
if __name__ == '__main__':
    data = get_current_senate_representative_data()
    # pprint.pprint(data)

    with open('senate_test.JSON', 'w') as outfile:
        json.dump(data, outfile, indent=4)