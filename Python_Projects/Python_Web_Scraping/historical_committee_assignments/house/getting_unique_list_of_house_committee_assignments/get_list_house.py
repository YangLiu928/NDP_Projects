import json



with open('combined.JSON','r') as data:
	members = json.load(data)

committee_assignments_list = set()

for member in members:
	committee_assignments = member['committee_assignments']
	for committee_assignment in committee_assignments:
		committee_assignments_list.add(committee_assignment)


for committee_assignment_element in committee_assignments_list:
	print committee_assignment_element

committee_assignments_list = list(committee_assignments_list)
committee_assignments_list.sort()

with open('unique_house_committee_assignments.JSON','w') as outfile:
	json.dump(committee_assignments_list,outfile,indent=4)