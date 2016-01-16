import process_data

data_folder = '../data/port_data_imports/'
output_folder = '../output/port_data_imports/'
date = '0902'

process_data.process_DPORTHS6I(data_folder, output_folder, date)

print 'task completed'