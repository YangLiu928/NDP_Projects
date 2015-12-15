import json
import lxml
from bs4 import BeautifulSoup
import re
import urllib2



def extract_from_text(congress_number):
	file = open(str(congress_number) + '.txt','r')
	lines = []
	for line in file:
		line = line.replace('\n','').strip()
		lines.append(line)
	file.close()

	results = {}
	member = ''
	current_committee_assignment = ''
	for line in lines:
		# we only look at lines that displays either a committee assignment or a member
		if _is_meaningful_line(line):
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
	# we want to do the replace because lines line the following is usually seen
	# __________ , ________________
	# _____________________________
	# where there is essentially no information within the line
	line = line.replace('_','').strip()
	line = line.replace('\n','').strip()

	# this black list is basically the lines we already know that are not effective information
	# but at the same time difficult to distinguish from a committee name which is also usually
	# displayed as a string in all caps. the comma is basically the line of "_____ , ____" with 
	# underscore replaced with an empty string
	black_list = ['COMMITTEE ASSIGNMENTS','STANDING COMMITTEES',',']

	# total five conditions where the line contains no effective information:
	# (1) lines that contains brackets [], because they are typically strings representing page numbers (e.g. "[[Page (6)]]")
	# (2) lines that are basically an empty string after the strip() function, meaning the line was just a bunch of white space
	# (3) lines that are in the black list we pre-defined
	# (4) lines where the word "Room" appears. This is to exclude the titles under each committe assignments that states where and
	# when a certain meeting will be held. This actually not needed because the function _get_line_type should return this as a None
	# type line, but, again, this is just for completeness and ruling out anything that we already know we do not need
	# (5) lines where, after replacing underscore with empty string and stripping, only one or multiple '\n' were left
	# This is added because we still see some empty lines printed out from the _get_line_type function
	if (re.search('[\[\]]',line)!=None) or (line=='') or (line in black_list):
		return False
	else:
		# print line + ' is meaningful'
		return True

def _get_line_type(line):
	# this function is intended to return whether the current line we are working with is a line
	# that contains committee assignment information or a specific member's identify
	line = line.strip()

	# .upper() changes everything within a string to its upper-case counterpart
	# if line.upper() == line, the entire line must originally be all in caps, which
	# indicates this is a line that represents the committee assignment name of a new block
	if line.upper() == line:
		# this is just for degugging.....
		# print line + ' is an assignment' 
		return 'assignment'
	elif re.search(', of ',line):
		# name, of state_full_name(, Chairman) <== optional
		return 'member'
	else:
		# The following lines prints out the lines that are not recognized as either a name or an assignment
		# this is mainly for debugging purpose to make sure no important information was overlooked
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
		# this prints out the lines where members' role in the committee was not recognized
		# This is mainly for making sure we do not overlook any line that contains important
		# information
		print 'cannot extract role from the follow line'
		print member_line
		print '\n'

if __name__ == '__main__':
	congress_number = 108
	data = extract_from_text(congress_number)
	with open('output_{0}.json'.format(str(congress_number)),'w') as outfile:
		json.dump(data,outfile,indent = 4)