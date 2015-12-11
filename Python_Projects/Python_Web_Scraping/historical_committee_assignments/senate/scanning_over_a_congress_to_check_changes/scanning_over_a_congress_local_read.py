import json
import lxml
from bs4 import BeautifulSoup
import re
import urllib2

def _get_soup(url):
    # returns a beautiful soup object for further operations
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)
    return BeautifulSoup(response.read(), 'lxml')

def _get_url(year, month, day):
	congress_number = str(_get_congress_number(year))
	year = str(year)
	month = str(month).zfill(2)
	day = str(day).zfill(2)
	url = 'https://www.gpo.gov/fdsys/pkg/CCAL-{c}scal-{y}-{m}-{d}/html/CCAL-{c}scal-{y}-{m}-{d}-pt2.htm'\
	.format(c=congress_number,y=year,m=month,d=day)
	return url

def _get_years(congress_number):
	# linear algebra
	return [2*congress_number + 1787,2*congress_number + 1788]

def _get_congress_number(year):
	if year%2==1:
		return (year-1787)/2
	else:
		return (year-1788)/2

def _is_valid_page(soup):
	text = soup.text
	if re.search('Error Detected - The page you requested cannot be found.',text):
		return False
	else:
		return True

def _get_date_from_url(url):
	base_index = url.find('scal-')
	# year = url[base_index+5:base_index+9]
	# month = url[base_index+10:base_index+12]
	# day = url[base_index+13:base_index+15]
	return url[base_index+5:base_index+15]



def scan_on_a_congress_number(congress_number):
	with open ('scan_on_112_congress_local_data.JSON') as data:
		all_committee_assignment_data = json.load(data)

	with open ('valid_dates.JSON') as data:
		valid_dates = json.load(data)

	result = {}
	for index in range (0, len(all_committee_assignment_data)):
		members = all_committee_assignment_data[index]
		# keys are basically all the display_name of the members in the members json data
		keys = members.keys()
		for key in keys:
			if result.has_key(key):
				for committee_assignment_name in members[key]['committee_assignments']:
					if result[key]['committee_assignments'].has_key(committee_assignment_name):
						result[key]['committee_assignments'][committee_assignment_name]['last_seen_date'] = valid_dates[index]
					else:
						result[key]['committee_assignments'][committee_assignment_name] = {}
						result[key]['committee_assignments'][committee_assignment_name]['start_date'] = valid_dates[index]
						result[key]['committee_assignments'][committee_assignment_name]['last_seen_date'] = valid_dates[index]
			else:
				# if a member has not been added to the result yet, we create an element for him/her
				result[key]={}
				result[key]['state'] = members[key]['state']
				result[key]['committee_assignments'] = {}
				for committee_assignment_name in members[key]['committee_assignments']:
					result[key]['committee_assignments'][committee_assignment_name] = {}
					result[key]['committee_assignments'][committee_assignment_name]['start_date'] = valid_dates[index]
					result[key]['committee_assignments'][committee_assignment_name]['last_seen_date'] = valid_dates[index]
	print 'finished parsing all data'
	return result


def _get_committee_assignments(soup):
	text = soup.find('pre').text
	lines = text.split('\n')
	results = {}
	member = ''
	current_committee_assignment = ''
	for line in lines:
		if _is_meaningful_line(line):
			# print line + ' is meaningful'
			line_type = _get_line_type(line)
			if line_type == 'member':
				display_name = _get_display_name(line)
				state = _get_state(line)
				# role = _get_role(line)
				if results.has_key(display_name):
					if _get_role(line) != 'member':
						results[display_name]['committee_assignments'].append(current_committee_assignment + ', ' + _get_role(line))
					else:
						results[display_name]['committee_assignments'].append(current_committee_assignment)
				else:
					results[display_name] = {}
					results[display_name]['state'] = state
					# results[display_name]['role'] = role
					results[display_name]['committee_assignments'] = []
					if _get_role(line) != 'member':
						results[display_name]['committee_assignments'].append(current_committee_assignment + ', ' + _get_role(line))
					else:
						results[display_name]['committee_assignments'].append(current_committee_assignment)
			elif line_type == 'assignment':
				current_committee_assignment = line.strip().title().replace('And','and')
				# print 'here is a new committee ' + current_committee_assignment
			else:
				print 'this line is neither a committe nor a member'
				print line
				print '\n'
	return results






def _is_meaningful_line(line):
	line = line.replace('_','').strip()
	black_list = ['COMMITTEE ASSIGNMENTS','STANDING COMMITTEES',',']
	if (re.search('[\[\]]',line)!=None) or (line=='') or (line in black_list) or (re.search('Room',line)!=None):
		# lines that include brackets are usually only for
		# page number, date of document and source of data
		
		return False

	else:
		# print line + ' is meaningful'
		return True

def _get_line_type(line):
	line = line.strip()
	if line.upper() == line:
		print line + ' is an assignment' 
		# the specific committee assignment name is displayed
		# as a string all in capital words
		return 'assignment'
	elif re.search(', of ',line):
		# name, of state_full_name(, Chairman) <== optional
		return 'member'
	else:
		print 'the following line was not recognized as either assignment or member'
		print line
		print '\n'
		return None

		
def _get_display_name(member_line):
	# Barbara A. Mikulski, of Maryland, Chairman
	return member_line.split(', of ')[0]

def _get_state(member_line):
	# Barbara A. Mikulski, of Maryland, Chairman
	return member_line.split(', of ')[1].split(', ')[0]

def _get_role(member_line):
	# Barbara A. Mikulski, of Maryland, Chairman
	if len(member_line.split(', of ')[1].split(', ')) == 2:
		return member_line.split(', of ')[1].split(', ')[1]
	elif len(member_line.split(', of ')[1].split(', ')) == 1:
		return 'member'
	else:
		print 'cannot extract role from the follow line'
		print member_line
		print '\n'



if __name__ == '__main__':
	data = scan_on_a_congress_number(112)
	with open('scan_on_112_congress.JSON','w') as outfile:
		json.dump(data, outfile, indent=4)
