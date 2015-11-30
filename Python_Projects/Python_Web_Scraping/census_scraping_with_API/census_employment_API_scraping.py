from bs4 import BeautifulSoup
import urllib2
import re
import json


def _get_opener():
	# utility function that returns a configured url opener
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent','Mozilla/5.0')]
	return opener

def _get_url(fields, state_code):
	# fields is a list of fields (e.g.: [total femal population, total male population]) a user want to query
	# these 'fields' can be found at the census.gov api reference: http://api.census.gov/data/2014/acs1/variables.html 
	
	# congressional_districts is a list of congressional districts a user want to query
	# each congressional district
	# congressional_district_code_list is a list of all available congressional district codes
	# not all these codes would apply to every congressional district

	url_base = ['http://api.census.gov/data/2014/acs1?']

	url_field_pieces = ['get=NAME']
	for field in fields:
		url_field_pieces.append(','+str(field))

	with open ('constants/congressional_district_code_list.JSON') as data:
		congressional_district_code_list = json.load(data)
	url_congressional_district_pieces = ['&for=congressional+district:']
	for index in range(0,len(congressional_district_code_list)):
		congressional_district_code = congressional_district_code_list[index]
		if index == len(congressional_district_code_list) - 1:
			url_congressional_district_pieces.append(str(congressional_district_code))
		else:
			url_congressional_district_pieces.append(str(congressional_district_code) + ',')

	url_state_pieces = ['&in=state:', str(state_code)]
	
	url_key_pieces = ['&key=', '40cd6e4b41660870a606420bec41f9303164bbd5']

	url_pieces = url_base + url_field_pieces + url_congressional_district_pieces + url_state_pieces + url_key_pieces

	url = ''
	for url_piece in url_pieces:
		url += url_piece

	return url


def get_employment_census_data():
	# this function is intended to return the employment data 
	# of all US states grouped by congressional district for year 2014 
	# in the form of a dictionary

	# we need a list of fields we are interested in
	# this list is retrieved by looking up the census.gov api reference list (http://api.census.gov/data/2014/acs1/variables.html)
	# and mimic the fields in the my congressional district tool (http://www.census.gov/mycd/)
	employment_occupation_field_list = [\
	'B24050_001E',\
	'B24050_028E',\
	'B24050_055E',\
	'B24050_082E',\
	'B24050_109E',\
	'B24050_136E']

	employment_industry_field_list=[\
	'B24050_001E',\
	'B24050_002E',\
	'B24050_005E',\
	'B24050_006E',\
	'B24050_007E',\
	'B24050_008E',\
	'B24050_009E',\
	'B24050_012E',\
	'B24050_013E',\
	'B24050_016E',\
	'B24050_020E',\
	'B24050_023E',\
	'B24050_026E',\
	'B24050_027E']

	employment_occupation_field_name_list= [\
	'Total',\
	'Management, business, science, and arts occupations',\
	'Service occupations',\
	'Sales and office occupations',\
	'Natural resources, construction, and maintenance occupations',\
	'Production, transportation, and material moving occupations']

	employment_industry_field_name_list = [\
	'Total',\
	'Agriculture, forestry, fishing and hunting, and mining',\
	'Construction',\
	'Manufacturing',\
	'Wholesale trade',\
	'Retail trade',\
	'Transportation and warehousing, and utilities',\
	'Information',\
	'Finance and insurance, and real estate and rental and leasing',\
	'Professional, scientific, and management, and administrative and waste management services',\
	'Educational services, and health care and social assistance',\
	'Arts, entertainment, and recreation, and accommodations and food services',\
	'Other services except public administration',\
	'Public administration']

	employment_field_list = employment_occupation_field_list + employment_industry_field_list
	employment_field_name_list = employment_occupation_field_name_list + employment_industry_field_name_list

	# state_code_list is a list of all us state code under the FIPS systems where reference is 
	# available at http://www2.census.gov/geo/docs/reference/codes/files/national_cd113.txt
	# this url is also useful http://www.census.gov/rdo/data/113th_congressional_and_2012_state_legislative_district_plans.html 
	with open ('constants/state_code_list.JSON') as state_code_list_data:
		state_code_list = json.load(state_code_list_data)	

	all_state_data = {}
	for state_code in state_code_list:
		opener = _get_opener()
		url = _get_url(employment_field_list,state_code)
		print url
		response = opener.open(url)
		try:
			data_list = json.load(response)
		except:
			continue
		state_name = re.search(',\s[a-zA-Z ]+',data_list[1][0]).group()[2:]
		state_data = {}

		for data in data_list[1:]:
			congressional_district_name = re.search('[a-zA-Z()0-9 ]+,',data[0]).group()[:-1]
			congressional_district_data = {}
			occupation_data = {}
			industry_data = {}
			for index in range (0,len(employment_field_list)):
				if index < len(employment_occupation_field_list):
					key = employment_field_name_list[index]
					value = data[index+1]
					occupation_data[key] = value
				else:
					key = employment_field_name_list[index]
					value = data[index+1]
					industry_data[key] = value
			congressional_district_data['occupation'] = occupation_data
			congressional_district_data['industry'] = industry_data
			state_data[congressional_district_name] = congressional_district_data

		all_state_data[state_name] = state_data

	return all_state_data

if __name__ == '__main__':
    data = get_employment_census_data()
    with open('employment_census_data.JSON', 'w') as outfile:
        json.dump(data, outfile, indent=4)