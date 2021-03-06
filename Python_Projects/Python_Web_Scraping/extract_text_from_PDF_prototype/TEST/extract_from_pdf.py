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


if __name__ == '__main__':
    doc = _convert_pdf_to_txt('102.pdf')
    # print doc

    member_queue = deque()
    assignments_queue = deque()

    blocks = _get_blocks(doc)
    for block in blocks:
        block_type = _get_block_type(block)
        if block_type == 'member':
            member_queue.append(block)
        elif block_type == 'assignments':
            assignments_queue.append(block)
        else:
            print 'the following block has a unknown blcok type'
            # print block
    min_length = min(len(assignments_queue),len(member_queue))
    # for member in member_queue:
    #     print member
    # for assignments in assignments_queue:
    #     print assignments
    print len(member_queue)
    print len(assignments_queue)

# list = doc.split('\n')
# for line in list:
#     print line
#     # _get_line_type(line)
    # member_queue = list(member_queue)[6:]

    fake_result = []
    for index in range(0,min_length):
        fake_result.append(member_queue[index] + '\t\t' + assignments_queue[index])
with open('fake.JSON', 'w') as outfile:
    json.dump(fake_result, outfile, indent=4)