import process_data

data_folder = '../data/merchandise_trade_exports/cdromtxt/'
output_folder = '../output/merchandise_trade_exports/'

# process_data.process_concord(data_folder, output_folder)
# process_data.process_country(data_folder, output_folder)
# process_data.process_district(data_folder, output_folder)
# process_data.process_enduse(data_folder, output_folder)
# process_data.process_exp_comm(data_folder, output_folder)
# process_data.process_exp_cty(data_folder, output_folder)
# process_data.process_exp_detl(data_folder, output_folder)
# process_data.process_exp_dist(data_folder, output_folder)
# process_data.process_hitech(data_folder, output_folder)
process_data.process_hsdesc(data_folder, output_folder)
# process_data.process_naics(data_folder, output_folder)
# process_data.process_sitc(data_folder, output_folder)

print 'work completed'
