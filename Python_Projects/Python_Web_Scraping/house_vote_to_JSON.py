import urllib2
from bs4 import BeautifulSoup
import json
import re
import xmldict

# finger print for the websites used to scrape house data
# used to determine whether webstructure has changed before going further for the scraping
HOUSE_VOTING_WEBSITE_FINGER_PRINT=''

def _get_house_roll_call_vote_summary_url(congress_number,session_number,roll_range):
# This function is intended to return the urls like 'http://clerk.house.gov/evs/2013/ROLL_500.asp'
# These are summary of the votes and contains information about the vote results, question, issue etc.	
	url = ''
	year = _get_year_from_congress_and_session_numbers (congress_number,session_number)
	url_pieces = ['http://clerk.house.gov/evs/', str(year), '/ROLL_', str(roll_range), '00.asp']
	for url_piece in url_pieces:
		url+=url_piece
	return url
def _get_year_from_congress_and_session_numbers(congress_number, session_number):
	return 2*congress_number + session_number + 1786

def _get_house_roll_call_vote_summary(congress_number):
	summary = {}
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	session_number=1
	while session_number<3:
		roll_range = 0
		while True:
			try:				
				url = _get_house_roll_call_vote_summary_url(congress_number,session_number,roll_range)
				response = opener.open(url)
				bsObject = BeautifulSoup(response.read(),'html.parser')
				# some redirect mechanism has block the HTTP error from happenning
				# special treatment made using the redirected-page to jump out of the loop
				if re.search('404',bsObject.head.title.contents[0]):
					break				
				table_rows = bsObject.find_all('tr')
				# here only the table rows after the one with 0 index is examined
				# because the table header is also a row in this web page structure				
				for table_row in table_rows[1:]:
					table_data = table_row.find_all('td')
					# create a dictionary for each roll call vote
					summary[table_data[0].a.contents[0]] = {}
					summary[table_data[0].a.contents[0]]['Date'] = table_data[1].font.contents[0]
					# the data in the issue column can either be empty, an anchor tag with link, or just plain text
					# need to treat differently
					if table_data[2].font.a !=None:
						summary[table_data[0].a.contents[0]]['Issue'] = table_data[2].font.a.contents[0]
					elif table_data[2].font.contents == []:						
						summary[table_data[0].a.contents[0]]['Issue'] = None
					else:
						summary[table_data[0].a.contents[0]]['Issue'] = table_data[2].font.contents[0]								
					# u'\xa0' is the unicode equivalent of &nbsp
					# some question data are empty and filled with &nbsp 
					if table_data[3].font.contents[0] == u'\xa0':
						summary[table_data[0].a.contents[0]]['Question'] = None
					else:
						summary[table_data[0].a.contents[0]]['Question'] = table_data[3].font.contents[0]

					if table_data[4].font.contents !=[]:
						summary[table_data[0].a.contents[0]]['Result'] = table_data[4].font.contents[0]
					else: 
						summary[table_data[0].a.contents[0]]['Result'] = None

					if table_data[5].font.contents[0] == u'\xa0':
						summary[table_data[0].a.contents[0]]['Title/Description'] = None
					else:
						summary[table_data[0].a.contents[0]]['Title/Description'] = table_data[5].font.contents[0]
				roll_range+=1
			except urllib2.HTTPError:
				print 'http error occurred at '+ url
		session_number+=1
	return summary



def _get_house_roll_call_vote_data_url(congress_number,session_number,roll_number):
	url = ''
	year = _get_year_from_congress_and_session_numbers (congress_number,session_number)
	url_pieces = ['http://clerk.house.gov/evs/',str(year),'/roll',str(roll_number).zfill(3),'.xml']
	# can the roll number be larger than 1000? some special treatment, but not necessarily appropriate
	if (roll_number>=1000):
		url_pieces[3] = str(roll_number)
		print 'the roll number is larger than or equal to 1000, the url used may not be correct'
	for url_piece in url_pieces:
		url+=url_piece
	return url

def get_house_roll_call_vote_data(congress_number):
	data = []
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	session_number=1
	while session_number<3:
		roll_number = 1
		while roll_number<3:
			try:
				url = _get_house_roll_call_vote_data_url(congress_number,session_number,roll_number)
				response = opener.open(url)
				vote_data = response.read()
				# some redirect mechanism has blocked the HTTP error from happenning
				# special treatment made using the redirected-page to jump out of the loop
				if re.search('<!DOCTYPE html',vote_data):
					# usually an XML is rendered, but if the url is not valid
					# webpage is redirected to an html page
					break
				# data.append(_get_formatted_vote_data(vote_data))
				dict = xmldict.xml_to_dict(vote_data)
				data.append(dict)
				roll_number+=1
			except urllib2.HTTPError:
				print 'HTTP error occurred at '+ url
		session_number+=1
	return data


				

def _get_formatted_vote_data(data):
	# input data should be a string
	data = xmldict.xml_to_dict(data)
	dict = {}
	dict['members']={}
	dict['members']['member']=[]
	votes = data['rollcall-vote']['vote-data']['recorded-vote']
	for vote in votes:
		member = {}
		# with the data we have, I cannot figure out the first name
		member['last_name'] = vote['legislator']['@unaccented-name']
		member['vote_cast'] = vote['vote']
		print vote['vote']
		member['state'] = vote['legislator']['@state']
		member['party'] = vote['legislator']['@party']
		# name-id?
		# member['lis_member_id'] 
		# Akaka (D-HI) full
		member['member_full'] = member['last_name'] + ' (' + member['party'] +'-'+ member['state'] + ')'
		dict['members']['member'].append(member)
	return dict









if __name__ == '__main__':
	data = get_house_roll_call_vote_data(112)
	with open('house_scraping_roll_call_vote_data_main_entry_point.JSON', 'w') as outfile:
		json.dump(data, outfile, indent=4)