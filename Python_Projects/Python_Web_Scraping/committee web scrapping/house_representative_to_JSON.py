import urllib2
from bs4 import BeautifulSoup
import json
import re
import xmldict
import lxml
import pprint

# finger print for the websites used to scrape house data
# used to determine whether web structure has changed before going further for the scraping
HOUSE_VOTING_WEBSITE_FINGER_PRINT = ''

# url used for house representative list scraping
HOUSE_REPRESENTATIVE_LIST_URL = 'http://clerk.house.gov/committee_info/oal.aspx'


def get_current_house_representative_data():
    results = []
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    url = HOUSE_REPRESENTATIVE_LIST_URL
    response = opener.open(url)
    bs_object = BeautifulSoup(response.read(),'lxml')
    # remove the first table row because it is the table header
    rows = bs_object.find('table').find('tbody').find_all('tr')[1:]
    for row in rows:
        result = {}        
        if row.find_all('td')[0].find('em') and row.find_all('td')[0].find('strong'):
            # this is a democrat AND a delegate or resident commissioner
            result['name'] = row.find_all('td')[0].find('em').string
            result['party'] = 'D'
            if re.search('Delegate',row.find_all('td')[0].contents[-1]):
                result['delegate'] = 'Yes'
                result['resident_commissioner'] = None
            else:
                result['delegate'] = None
                result['resident_commissioner'] = 'Yes'
            result['state'] = row.find_all('td')[0].contents[-1][-2:]
            result['congressional_number'] = None
            result['committee_assignments'] = []
            for element in row.find_all('td')[1].contents:
                if re.search('\w+[.]',str(element)):
                    result['committee_assignments'].append(re.search('\w+',str(element)).group())                        
        elif row.find_all('td')[0].find('em'):
            # this is a democrat but Not a delegate or resident commissioner
            result['name'] = row.find_all('td')[0].find('em').string
            result['party'] = 'D'
            result['delegate'] = None
            result['resident_commissioner'] = None
            result['state'] = row.find_all('td')[0].contents[-1][-2:]

            result['congressional_number'] = re.search('([0-9]+(d|st|th)|At Large)',row.find_all('td')[0].contents[-1]).group()
            result['committee_assignments'] = []
            for element in row.find_all('td')[1].contents:
                if re.search('\w+[.]',str(element)):
                    result['committee_assignments'].append(re.search('\w+',str(element)).group())           
        elif row.find_all('td')[0].find('strong'):
            # this is a republican as well as delegate or resident commissioner
            result['name'] = row.find_all('td')[0].find('strong').string
            result['party'] = 'R'
            if re.search('Delegate',row.find_all('td')[0].contents[-1]):
                result['delegate'] = 'Yes'
                result['resident_commissioner'] = None
            else:
                result['resident_commissioner'] = 'Yes'
                result['delegate'] = None
            result['congressional_number'] = None
            result['state'] = row.find_all('td')[0].contents[-1][-2:]
            result['committee_assignments'] = []
            for element in row.find_all('td')[1].contents:
                if re.search('\w+[.]',str(element)):
                    result['committee_assignments'].append(re.search('\w+',str(element)).group())            
        else:
            # republican but not delegate or resident commissioner
            string = row.find_all('td')[0].string
            # get everything before a number is encountered

            unprocessed_name = re.search('[^0-9]+',string).group()
            if re.search('At Large',unprocessed_name):
                left = re.search('At Large',unprocessed_name).span()[0]
                unprocessed_name = unprocessed_name[:left]
            # remove the trailing comma and space
            result['name'] = unprocessed_name[:-2]
            result['party'] = 'R'
            result['congressional_number'] = re.search('([0-9]+(th|d|st)|At Large)',string).group()
            result['delegate'] = None
            result['resident_commissioner'] = None
            result['state'] = string[-2:]
            result['committee_assignments'] = []
            for element in row.find_all('td')[1].contents:
                if re.search('\w+[.]',str(element)):
                    result['committee_assignments'].append(re.search('\w+',str(element)).group())
        results.append(result)
    return results

if __name__ == '__main__':
    data = get_current_house_representative_data()
    # pprint.pprint(data)

    with open('house_representative.JSON', 'w') as outfile:
        json.dump(data, outfile, indent=4)