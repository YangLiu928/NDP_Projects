# import re

def _read_and_write(raw_file_route, pipe_file_route, pairs):
    raw_file = open(raw_file_route, 'r')
    sql_file = open(pipe_file_route, 'w')
    file_name = _extract_file_name(raw_file_route)

    if 'exp' in file_name.lower():
        exp_or_imp = 'exp'
    else:
        exp_or_imp = 'imp'


    line_count = 0
    for line in raw_file:
        line_count = line_count + 1
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
        if line_count == 1000:
            break
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









def process_concord(data_folder, output_folder):
    concord_raw_route = data_folder + 'CONCORD.TXT'
    concord_pipe_route = output_folder + 'CONCORD.SQL'
    pairs = [
        [1, 10],
        [11, 160],
        [161, 210],
        [211, 213],
        [214, 216],
        [217, 221],
        [222, 226],
        [227, 232],
        [233, 233],
        [234, 235]
    ]
    _read_and_write(concord_raw_route, concord_pipe_route, pairs)


def process_country(data_folder, output_folder):
    country_raw_route = data_folder + 'COUNTRY.TXT'
    country_pipe_route = output_folder + 'COUNTRY.SQL'
    pairs = [
        [1, 4],
        [5, 11],
        [12, 60]
    ]
    _read_and_write(country_raw_route, country_pipe_route, pairs)


def process_district(data_folder, output_folder):
    district_raw_route = data_folder + 'DISTRICT.TXT'
    district_pipe_route = output_folder + 'DISTRICT.SQL'
    pairs = [
        [1, 2],
        [3, 9],
        [10, 59]
    ]
    _read_and_write(district_raw_route, district_pipe_route, pairs)


def process_enduse(data_folder, output_folder):
    enduse_raw_route = data_folder + 'ENDUSE.TXT'
    enduse_pipe_route = output_folder + 'ENDUSE.SQL'
    pairs = [
        [1, 5],
        [6, 105]
    ]
    _read_and_write(enduse_raw_route, enduse_pipe_route, pairs)


def process_exp_comm(data_folder, output_folder):
    exp_comm_raw_route = data_folder + 'EXP_COMM.TXT'
    exp_comm_pipe_route = output_folder + 'EXP_COMM.SQL'
    pairs = [
        [1, 1],
        [2, 11],
        [12, 61],
        [62, 64],
        [65, 67],
        [68, 71],
        [72, 73],
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
        [359, 373]
    ]
    _read_and_write(exp_comm_raw_route, exp_comm_pipe_route, pairs)


def process_exp_cty(data_folder, output_folder):
    exp_cty_raw_route = data_folder + 'EXP_CTY.TXT'
    exp_cty_pipe_route = output_folder + 'EXP_CTY.SQL'
    pairs = [
        [1, 4],
        [5, 34],
        [35, 38],
        [39, 40],
        [41, 55],
        [56, 70],
        [71, 85],
        [86, 100],
        [101, 115],
        [116, 130],
        [131, 145],
        [146, 160],
        [161, 175],
        [176, 190],
        [191, 205],
        [206, 220],
        [221, 235],
        [236, 250],
        [251, 265],
        [266, 280]
    ]
    _read_and_write(exp_cty_raw_route, exp_cty_pipe_route, pairs)


def process_exp_detl(data_folder, output_folder):
    exp_detl_raw_route = data_folder + 'EXP_DETL.TXT'
    exp_detl_pipe_route = output_folder + 'EXP_DETL.SQL'
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
    _read_and_write(exp_detl_raw_route, exp_detl_pipe_route, pairs)


def process_exp_dist(data_folder, output_folder):
    exp_dist_raw_route = data_folder + 'EXP_DIST.TXT'
    exp_dist_pipe_route = output_folder + 'EXP_DIST.SQL'
    pairs = [
        [1, 2],
        [3, 32],
        [33, 36],
        [37, 38],
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
        [264, 278]
    ]
    _read_and_write(exp_dist_raw_route, exp_dist_pipe_route, pairs)


def process_hitech(data_folder, output_folder):
    hitech_raw_route = data_folder + 'HITECH.TXT'
    hitech_pipe_route = output_folder + 'HITECH.SQL'
    pairs = [
        [1, 2],
        [3, 32]
    ]
    _read_and_write(hitech_raw_route, hitech_pipe_route, pairs)


def process_hsdesc(data_folder, output_folder):
    hsdesc_raw_route = data_folder + 'HSDESC.TXT'
    hsdesc_pipe_route = output_folder + 'HSDESC.SQL'
    pairs = [
        [1, 6],
        [7, 156],
        [157, 206]
    ]
    _read_and_write(hsdesc_raw_route, hsdesc_pipe_route, pairs)


def process_naics(data_folder, output_folder):
    naics_raw_route = data_folder + 'NAICS.TXT'
    naics_pipe_route = output_folder + 'NAICS.SQL'
    pairs = [
        [1, 6],
        [7, 56]
    ]
    _read_and_write(naics_raw_route, naics_pipe_route, pairs)


def process_sitc(data_folder, output_folder):
    sitc_raw_route = data_folder + 'SITC.TXT'
    sitc_pipe_route = output_folder + 'SITC.SQL'
    pairs = [
        [1, 5],
        [6, 155],
        [156, 205]
    ]
    _read_and_write(sitc_raw_route, sitc_pipe_route, pairs)


def process_imp_comm(data_folder, output_folder):
    imp_comm_raw_route = data_folder + 'IMP_COMM.TXT'
    imp_comm_pipe_route = output_folder + 'IMP_COMM.SQL'
    pairs = [
        [1, 10],
        [11, 60],
        [61, 63],
        [64, 66],
        [67, 70],
        [71, 72],
        [73, 87],
        [88, 102],
        [103, 117],
        [118, 132],
        [133, 147],
        [148, 162],
        [163, 177],
        [178, 192],
        [193, 207],
        [208, 222],
        [223, 237],
        [238, 252],
        [253, 267],
        [268, 282],
        [283, 297],
        [298, 312],
        [313, 327],
        [328, 342],
        [343, 357],
        [358, 372],
        [373, 387],
        [388, 402],
        [403, 417],
        [418, 432],
        [433, 447],
        [448, 462],
        [463, 477],
        [478, 492],
        [493, 507],
        [508, 522],
        [523, 537],
        [538, 552],
        [553, 567],
        [568, 582],
        [583, 597],
        [598, 612],
        [613, 627],
        [628, 642],
        [643, 657],
        [658, 672],
        [673, 687],
        [688, 702],
        [703, 717],
        [718, 732]
    ]
    _read_and_write(imp_comm_raw_route, imp_comm_pipe_route, pairs)


def process_imp_cty(data_folder, output_folder):
    imp_cty_raw_route = data_folder + 'IMP_CTY.TXT'
    imp_cty_pipe_route = output_folder + 'IMP_CTY.SQL'
    pairs = [
        [1, 4],
        [5, 34],
        [35, 38],
        [39, 40],
        [41, 55],
        [56, 70],
        [71, 85],
        [86, 100],
        [101, 115],
        [116, 130],
        [131, 145],
        [146, 160],
        [161, 175],
        [176, 190],
        [191, 205],
        [206, 220],
        [221, 235],
        [236, 250],
        [251, 265],
        [266, 280],
        [281, 295],
        [296, 310],
        [311, 325],
        [326, 340],
        [341, 355],
        [356, 370],
        [371, 385],
        [386, 400],
        [401, 415],
        [416, 430],
        [431, 445],
        [446, 460],
        [461, 475],
        [476, 490],
        [491, 505],
        [506, 520],
        [521, 535],
        [536, 550],
        [551, 565],
        [566, 580]
    ]
    _read_and_write(imp_cty_raw_route, imp_cty_pipe_route, pairs)

def process_imp_de(data_folder, output_folder):
    imp_de_raw_route = data_folder + 'IMP_DE.TXT'
    imp_de_pipe_route = output_folder + 'IMP_DE.SQL'
    pairs = [
        [1, 2],
        [3, 32],
        [33, 36],
        [37, 38],
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
        [309, 323],
        [324, 338],
        [339, 353],
        [354, 368],
        [369, 383],
        [384, 398],
        [399, 413],
        [414, 428],
        [429, 443],
        [444, 458],
        [459, 473],
        [474, 488],
        [489, 503],
        [504, 518],
        [519, 533],
        [534, 548],
        [549, 563],
        [564, 578]
    ]
    _read_and_write(imp_de_raw_route, imp_de_pipe_route, pairs)


def process_imp_du(data_folder, output_folder):
    imp_du_raw_route = data_folder + 'IMP_DU.TXT'
    imp_du_pipe_route = output_folder + 'IMP_DU.SQL'
    pairs = [
        [1, 2],
        [3, 32],
        [33, 36],
        [37, 38],
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
        [309, 323],
        [324, 338],
        [339, 353],
        [354, 368],
        [369, 383],
        [384, 398],
        [399, 413],
        [414, 428],
        [429, 443],
        [444, 458],
        [459, 473],
        [474, 488],
        [489, 503],
        [504, 518],
        [519, 533],
        [534, 548],
        [549, 563],
        [564, 578]
    ]
    _read_and_write(imp_du_raw_route, imp_du_pipe_route, pairs)


def process_imp_detl(data_folder, output_folder):
    imp_detl_raw_route = data_folder + 'IMP_DETL.TXT'
    imp_detl_pipe_route = output_folder + 'IMP_DETL.SQL'
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
    _read_and_write(imp_detl_raw_route, imp_detl_pipe_route, pairs)


def process_STHS6(data_folder, output_folder, date):
    STHS6_raw_route = data_folder + 'STHS6' + 'M' + date + '.TXT'
    STHS6_pipe_route = output_folder + 'STHS6' + 'M' + date + '.SQL'
    pairs = [
        [1, 6],
        [7, 10],
        [11, 12],
        [13, 16],
        [17, 18],
        [19, 33],
        [34, 48],
        [49, 63],
        [64, 78],
        [79, 93],
        [94, 108],
        [109, 123],
        [124, 138],
        [139, 153],
        [154, 168],
        [169, 183],
        [184, 198],
        [199, 213],
        [214, 228]
    ]
    _read_and_write(STHS6_raw_route, STHS6_pipe_route, pairs)


def process_STNAICS(data_folder, output_folder, date):
    STNAICS_raw_route = data_folder + 'STNAICS' + date + '.txt'
    STNAICS_pipe_route = output_folder + 'STNAICS' + date + '.SQL'
    pairs = [
        [1, 4],
        [5, 8],
        [9, 10],
        [11, 14],
        [15, 16],
        [17, 31],
        [32, 46],
        [47, 61],
        [62, 76],
        [77, 91],
        [92, 106],
        [107, 121],
        [122, 136],
        [137, 151],
        [152, 166],
        [167, 181],
        [182, 196],
        [197, 211],
        [212, 226]
    ]
    _read_and_write(STNAICS_raw_route, STNAICS_pipe_route, pairs)

def process_ISTHS6(data_folder, output_folder, date):
    ISTHS6_raw_route = data_folder + 'ISTHS' + 'M' + date + '.txt'
    ISTHS6_pipe_route = output_folder + 'ISTHS' + 'M' + date + '.SQL'
    pairs = [
        [1, 6],
        [7, 10],
        [11, 12],
        [13, 16],
        [17, 18],
        [19, 33],
        [34, 48],
        [49, 63],
        [64, 78],
        [79, 93],
        [94, 108],
        [109, 123],
        [124, 138],
        [139, 153],
        [154, 168],
        [169, 183],
        [184, 198],
        [199, 213],
        [214, 228],
        [229, 243],
        [244, 258]
    ]
    _read_and_write(ISTHS6_raw_route, ISTHS6_pipe_route, pairs)

def process_ISTNAICS(data_folder, output_folder, date):
    ISTNAICS_raw_route = data_folder + 'ISNAICS' + date + '.TXT'
    ISTNAICS_pipe_route = output_folder + 'ISNAICS' + date + '.SQL'
    pairs = [
        [1, 4],
        [5, 8],
        [9, 10],
        [11, 14],
        [15, 16],
        [17, 31],
        [32, 46],
        [47, 61],
        [62, 76],
        [77, 91],
        [92, 106],
        [107, 121],
        [122, 136],
        [137, 151],
        [152, 166],
        [167, 181],
        [182, 196],
        [197, 211],
        [212, 226],
        [227, 241],
        [242, 256]
    ]
    _read_and_write(ISTNAICS_raw_route, ISTNAICS_pipe_route, pairs)


def process_DPORTHS6E(data_folder, output_folder, date):
    DPORTHS6E_raw_route = data_folder + 'PORTHS6XM' + date + '.TXT'
    DPORTHS6E_pipe_route = output_folder + 'PORTHS6XM' + date + '.SQL'
    pairs = [
        [1, 6],
        [7, 10],
        [11, 14],
        [15, 18],
        [19, 20],
        [21, 35],
        [36, 50],
        [51, 65],
        [66, 80],
        [81, 95],
        [96, 110],
        [111, 125],
        [126, 140],
        [141, 155],
        [156, 170],
        [171, 185],
        [186, 200],
        [201, 215],
        [216, 230]
    ]
    _read_and_write(DPORTHS6E_raw_route, DPORTHS6E_pipe_route, pairs)


def process_DPORTHS6I(data_folder, output_folder, date):
    DPORTHS6I_raw_route = data_folder + 'PORTHS6MM' + date + '.TXT'
    DPORTHS6I_pipe_route = output_folder + 'PORTHS6MM' + date + '.SQL'
    pairs = [
        [1, 6],
        [7, 10],
        [11, 14],
        [15, 18],
        [19, 20],
        [21, 35],
        [36, 50],
        [51, 65],
        [66, 80],
        [81, 95],
        [96, 110],
        [111, 125],
        [126, 140],
        [141, 155],
        [156, 170],
        [171, 185],
        [186, 200],
        [201, 215],
        [216, 230]
    ]
    _read_and_write(DPORTHS6I_raw_route, DPORTHS6I_pipe_route, pairs)

