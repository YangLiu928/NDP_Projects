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








def get_committee_assignments(soup):
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
	black_list = ['COMMITTEE ASSIGNMENTS','STANDING COMMITTEES']
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
	# Barbara A. Mikulski, of Maryland
	if len(member_line.split(', of ')[1].split(', ')) == 2:
		return member_line.split(', of ')[1].split(', ')[1]
	elif len(member_line.split(', of ')[1].split(', ')) == 1:
		return 'member'
	else:
		print 'cannot extract role from the follow line'
		print member_line
		print '\n'



if __name__ == '__main__':
	url = 'https://www.gpo.gov/fdsys/pkg/CCAL-113scal-2014-12-04/html/CCAL-113scal-2014-12-04-pt2.htm'
	soup = _get_soup(url)
	result = get_committee_assignments(soup)
	with open('senate_committee_assignment.JSON','w') as outfile:
		json.dump(result, outfile, indent=4)
