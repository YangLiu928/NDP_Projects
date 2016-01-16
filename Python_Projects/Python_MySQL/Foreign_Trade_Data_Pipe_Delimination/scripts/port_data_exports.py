import process_data

data_folder = '../data/port_data_exports/'
output_folder = '../output/port_data_exports/'
date = '0902'

process_data.process_DPORTHS6E(data_folder, output_folder, date)

print 'task completed'

