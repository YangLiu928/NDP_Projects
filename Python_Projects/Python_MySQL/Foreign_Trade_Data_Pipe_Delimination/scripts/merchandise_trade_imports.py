import process_data

data_folder = '../data/merchandise_trade_imports/cdromtxt/'
output_folder = '../output/merchandise_trade_imports/'

process_data.process_concord(data_folder, output_folder)
process_data.process_country(data_folder, output_folder)
process_data.process_district(data_folder, output_folder)
process_data.process_enduse(data_folder, output_folder)
process_data.process_hitech(data_folder, output_folder)
process_data.process_hsdesc(data_folder, output_folder)
process_data.process_imp_comm(data_folder, output_folder)
process_data.process_imp_cty(data_folder, output_folder)
process_data.process_imp_de(data_folder, output_folder)
process_data.process_imp_du(data_folder, output_folder)
process_data.process_imp_detl(data_folder, output_folder)
process_data.process_naics(data_folder, output_folder)
process_data.process_sitc(data_folder, output_folder)

print 'task completed'
