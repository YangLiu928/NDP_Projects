import json
import re


def print_member_by_committee_assignment(committee_assignment):
	with open('combined.JSON','r') as data:
		members = json.load(data)

	for member in members:
		if committee_assignment in member['committee_assignments']:
			print member['display_name']


def print_member_by_similar_committee_assignment(partial):
	with open('combined.JSON','r') as data:
		members = json.load(data)

	for member in members:
		for committee_assignment in member['committee_assignments']:
			if re.search(partial,committee_assignment):
				print member['display_name'] + '\t\t\t' + committee_assignment



if __name__ == '__main__':
	print_member_by_committee_assignment('Permanent Select Committee on')
	# print_member_by_similar_committee_assignment('Global Warming')