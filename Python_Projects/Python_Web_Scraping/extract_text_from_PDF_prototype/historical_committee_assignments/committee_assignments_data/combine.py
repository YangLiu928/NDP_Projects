import json

output = []

for index in range (106,114):
	file_name = str(index)+'.JSON'
	print file_name
	with open (file_name) as data:
		input = json.load(data)
	output += input

print output
with open ('combined.JSON','w') as outfile:
	json.dump(output, outfile, indent = 4)
