import json

with open('scan_on_109_to_114_congress_new.JSON','r') as input:
	data = json.load(input)

keys = data.keys()

names = set()
for key in keys:
	name = data[key]['display_name']
	if name in names:
		print name
	else:
		names.add(name)