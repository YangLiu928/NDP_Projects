# import re
from zipfile import ZipFile
from os import listdir, mkdir
from os.path import isfile, join, isdir
from time import time

def _read_and_write(raw_file_route, pipe_file_route, pairs):
    raw_file = open(raw_file_route, 'r')
    sql_file = open(pipe_file_route, 'w')
    file_name = _extract_file_name(raw_file_route)

    if 'exp' in file_name.lower():
        exp_or_imp = 'exp'
    else:
        exp_or_imp = 'imp'


    # line_count = 0
    for line in raw_file:
        # line_count = line_count + 1
        line = line.strip()
        length = len(pairs)
        sql = 'call cap_data_goods_' + exp_or_imp + '_detl_update ('
        for index in range(0, length - 1):
            pair = pairs[index]
            word = line[pair[0] - 1:pair[1]].strip()
            sql = sql + '\'' + word.replace('\'','\'\'').replace('\"','\"\"').strip() + '\', '
        last_word = line[pairs[-1][0] - 1:pairs[-1][1]].strip()
        sql = sql + '\'' + last_word.replace('\'','\'\'').replace('\"','\"\"').strip() + '\');\r\n'        
        sql_file.write(sql)
        # if line_count == 1000:
            # break
    raw_file.close()
    sql_file.close()





def _extract_file_name(raw_file_route):
    return raw_file_route.split('/')[-1][:-4]

def _is_number(string):
    number_pattern = re.compile('[0-9]+')
    if number_pattern.match(string.strip()):
        return True
    else:
        return False



def process_exp_detl(year):
    start_time = time()
    main_output_folder = 'output'
    # check if the main output folder exists, and create one if not
    if not isdir(main_output_folder):
        mkdir(main_output_folder)
    # check if the year folder exists in the output folder
    output_year_folder = join(main_output_folder,str(year))
    if not isdir(output_year_folder):
        mkdir(output_year_folder)

    output_folder = join(output_year_folder,'export')
    if not isdir(output_folder):
        mkdir(output_folder)

    main_data_folder = 'downloaded_census_data'
    if (not isdir(main_data_folder)) or (not isdir(join(main_data_folder,str(year)))):
        print 'there is no source data folder for year ' + str(year)
    input_year_folder = join(main_data_folder,str(year))
    folder_list = [folder for folder in listdir(input_year_folder) if isdir(join(input_year_folder,folder))]
    input_file_name = 'EXP_DETL.TXT'
    # exp_detl_pipe_route = output_folder + 'EXP_DETL.SQL'
    pairs = [
        [1, 1],
        [2, 11],
        [12, 15],
        [16, 17],
        [18, 21],
        [22, 23],
        [24, 38],
        [39, 53],
        [54, 68],
        [69, 83],
        [84, 98],
        [99, 113],
        [114, 128],
        [129, 143],
        [144, 158],
        [159, 173],
        [174, 188],
        [189, 203],
        [204, 218],
        [219, 233],
        [234, 248],
        [249, 263],
        [264, 278],
        [279, 293],
        [294, 308],
        [309, 323]
    ]
    for folder in folder_list:
        if folder[:2].lower() == 'im':
            continue
        time_stamp = folder[-4:]
        input_file_path = join(join(input_year_folder,folder),input_file_name)
        output_file_path = join(output_folder,'EXP_DETL_{0}.sql'.format(time_stamp))
        _read_and_write(input_file_path, output_file_path, pairs)

    print 'generation of sql statements for export data for year ' + str(year) + ' took ' + str(time()-start_time) + ' seconds'


def process_imp_detl(year):
    start_time = time()
    main_output_folder = 'output'
    # check if the main output folder exists, and create one if not
    if not isdir(main_output_folder):
        mkdir(main_output_folder)
    # check if the year folder exists in the output folder
    output_year_folder = join(main_output_folder,str(year))
    if not isdir(output_year_folder):
        mkdir(output_year_folder)

    output_folder = join(output_year_folder,'import')
    if not isdir(output_folder):
        mkdir(output_folder)

    main_data_folder = 'downloaded_census_data'
    if (not isdir(main_data_folder)) or (not isdir(join(main_data_folder,str(year)))):
        print 'there is no source data folder for year ' + str(year)
    input_year_folder = join(main_data_folder,str(year))
    folder_list = [folder for folder in listdir(input_year_folder) if isdir(join(input_year_folder,folder))]
    input_file_name = 'IMP_DETL.TXT'
    pairs = [
        [1, 10],
        [11, 14],
        [15, 16],
        [17, 18],
        [19, 20],
        [21, 22],
        [23, 26],
        [27, 28],
        [29, 43],
        [44, 58],
        [59, 73],
        [74, 88],
        [89, 103],
        [104, 118],
        [119, 133],
        [134, 148],
        [149, 163],
        [164, 178],
        [179, 193],
        [194, 208],
        [209, 223],
        [224, 238],
        [239, 253],
        [254, 268],
        [269, 283],
        [284, 298],
        [299, 313],
        [314, 328],
        [329, 343],
        [344, 358],
        [359, 373],
        [374, 388],
        [389, 403],
        [404, 418],
        [419, 433],
        [434, 448],
        [449, 463],
        [464, 478],
        [479, 493],
        [494, 508],
        [509, 523],
        [524, 538],
        [539, 553],
        [554, 568],
        [569, 583],
        [584, 598],
        [599, 613],
        [614, 628],
        [629, 643],
        [644, 658],
        [659, 673],
        [674, 688]
    ]
    for folder in folder_list:
        if folder[:2].lower() == 'ex':
            continue
        time_stamp = folder[-4:]
        input_file_path = join(join(input_year_folder,folder),input_file_name)
        output_file_path = join(output_folder,'IMP_DETL_{0}.sql'.format(time_stamp))
        _read_and_write(input_file_path, output_file_path, pairs)

    print 'generation of sql statements for import data for year ' + str(year) + ' took ' + str(time()-start_time) + ' seconds'
