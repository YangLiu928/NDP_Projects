import codecs
from os.path import join,isfile,isdir
from os import mkdir







def get_intervals(layout):
	results = []
	layout = codecs.open(layout,'r')
	count = 0
	for line in layout:
		count = count + 1
		if count < 8:
			continue
		if line.strip()=='':
			continue
		# print line.split(' ')
		numbers = ''
		segments = line.split(' ')
		for index in range (0,len(segments)):
			numbers = segments[index]
			if len(numbers)!=0:
				break
		left = int(numbers.split('\t')[0].split('-')[0]) - 1
		right = int(numbers.split('\t')[0].split('-')[1])
		results.append([left,right])
	return results


def pipe_delimition(import_or_export):
	if import_or_export.lower()!='import' and import_or_export.lower()!='export':
		return
	if import_or_export.lower() == 'export':
		layout = 'EXP_DETL.lay'
		input_file = 'EXP_DETL.TXT'
		# input_folder = 'MERCHEXH2014'
		output_file = 'PIPE_DELIMITED_EXP_DETL.TXT'
	else:
		layout = 'IMP_DETL.lay'
		input_file = 'IMP_DETL.TXT'
		# input_folder = 'MERCHIMH2014'
		output_file = 'PIPE_DELIMITED_IMP_DETL.TXT'

	# input_path = join(input_folder,input_file)
	input_path = input_file

	output = codecs.open(output_file,'w','utf-8')
	input = codecs.open(input_path,'r','utf-8')

	intervals = get_intervals(layout)
	print intervals
	line_count = 0
	for line in input:
		line_count = line_count + 1
		string = u''
		for index in range (0,len(intervals)-1):
			string = string + line[intervals[index][0]:intervals[index][1]].strip() + '|'
		string = string + line[intervals[len(intervals)-1][0]:intervals[len(intervals)-1][1]].strip() + '\r'
		output.write(string)
		if line_count==1000:
			break
	output.close()
	input.close()


	







if __name__ == '__main__':
	pipe_delimition('import')
	pipe_delimition('export')	