from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import re
import pprint
import json

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

doc = _convert_pdf_to_txt('112.pdf')
print doc
string_list = doc.split('\n')
# print string_list

current_member = ''
result = {}
for string in string_list:
    if len(string.strip())!=0:
        print string
        # exclude blank lines
        if re.search('([0-9]+(d|st|th)|At Large|[(]Delegate[)]|[(]Resident Commissioner[)]) [A-Z][A-Z]',string):
            # this is the starting row for a new member
            # each line that contains a memeber has a part stating
            # number of congressional district, space, and then state abbreviation
            unprocessed_current_member = re.search('.+, ([0-9]|At Large|[(])',string).group()
            if re.search('At Large',unprocessed_current_member):
                current_member = unprocessed_current_member[:-10]
            else:
                current_member = unprocessed_current_member[:-3]
            committee_assignments = [re.findall('[\' 0-9a-zA-Z,]+',string)[-1].strip()]
            result[current_member] = committee_assignments
        elif re.search('([(]Delegate[)]|[(]Resident Commissioner[)])',string):
            del result[current_member]
            extra = re.search('([(]Delegate[)]|[(]Resident Commissioner[)])',string).group().strip()
            current_member += extra
            result[current_member] = committee_assignments
        elif re.search('[0-9 ()]+',string):
            continue
        else:
            if len(current_member)>0:
                committee_assignment_list = re.findall('[\' 0-9a-zA-Z,]+',string)
                for committee_assignment in committee_assignment_list:
                    result[current_member].append(committee_assignment)

with open('pdf_data.JSON', 'w') as outfile:
    json.dump(result, outfile, indent=4)
