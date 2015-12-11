from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import re
import pprint
import json
from collections import deque

def _convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def _get_block_type(block):
    # if a "state" (two capital letters) is found, we consider it as a member
    if re.search(' [A-Z][A-Z]',block.strip()):
        return 'member'
    elif re.match('([ A-Za-z0-9\',$]+[.])+',block.strip()):
        return 'assignments'
    else:
        print 'the following line is not recognized as either assignments or member'
        print block
        return 'unknown'

def _get_blocks(doc):
    
    blocks = []
    lines = doc.split('\n')
    block = ''
    black_list = ['FINAL EDITION','OFFICIAL ALPHABETICAL LIST','OF THE','HOUSE OF REPRESENTATIVES','of the UNITED STATES','Republicans in roman; Democrats in italic; Independents underlined;','Resident Commissioner and Delegates in boldface.']
    for line in lines:
        if len(line.strip())>0:
            if line.strip() in black_list or re.search('(ONE HUNDRED|Compiled by)',line.strip()):
                print 'this line seems to be not valid for a block'
                print line
            else:
                block+=(' ' + line.strip())
                if len(block.split('.')) == 5:
                    blocks.append(block)
                    print 'the following block has reached 4 committee assignments'
                    print 'skipping to the next block. This is not safe, but OK for one-time use'
                    print block
                    block = ''
        elif len(block)==0:
            continue
        else:
            blocks.append(block)
            block = ''
    return blocks

def _get_member_data(member):
    
    result = {}
    member = member.strip()

    if re.search(', Delegate ',member):
        display_name = member.split(', Delegate ')[0]
        state = member.split(', Delegate ')[1]
        congressional_district = 'Delegate'
    elif re.search(', Resident Commissioner ',member):
        display_name = member.split(', Resident Commissioner ')[0]
        state = member.split(', Resident Commissioner ')[1]
        congressional_district = 'Resident Commissioner'
    elif re.search(', At Large ',member):
        display_name = member.split(', At Large ')[0]
        state = member.split(', At Large ')[1]
        congressional_district = 'At Large'
    elif re.search(', [0-9]+(rd|th|st|nd) ',member):
        splitter = re.search(', [0-9]+(rd|th|st|nd) ',member).group()
        display_name = member.split(splitter)[0]
        state = member.split(splitter)[1]
        congressional_district = re.search('[0-9]+',splitter).group()
    else:
        print 'cannot process the following string'
        print member + '\n'

    result['display_name'] = display_name
    result['state'] = state
    result['congressional_district'] = congressional_district

    return result

def _get_committee_assignments(assignment):
    result = []
    assignment_list = assignment.split('.')
    for assignment_element in assignment_list:
        if assignment_element.strip()!='':
            result.append(assignment_element.strip())

    return result


if __name__ == '__main__':

    doc = _convert_pdf_to_txt('input/107.pdf')
    members = []
    assignments = []

    blocks = _get_blocks(doc)

    for block in blocks:
        block_type = _get_block_type(block)
        if block_type == 'member':
            members.append(block)
        elif block_type == 'assignments':
            assignments.append(block)
        else:
            print 'the following block has a unknown blcok type'
            print block


    min_length = min(len(assignments),len(members))
    print len(members)
    print len(assignments)
    # members has 438 results, and assignments has 438 results
    # the number matches exactly, but still should be careful on whether the result is accurate
    # result = []
    # for index in range (0,min_length):
    #     line = members[index] + '           ' + assignments[index]
    #     result.append(line)



    member_index = 0
    assignment_index = 0

    outputs = []
    while assignment_index < min_length:
        output = {}
        member = members[member_index]
        assignment = assignments[assignment_index]
        output.update(_get_member_data(member))
        output['committee_assignments'] = _get_committee_assignments(assignment)
        member_index += 1
        assignment_index += 1
        outputs.append(output)

    with open('output/107_raw_but_looks_fine.JSON', 'w') as outfile:
        json.dump(outputs, outfile, indent=4)