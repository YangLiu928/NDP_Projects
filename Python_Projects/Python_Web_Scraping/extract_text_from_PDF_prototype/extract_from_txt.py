import json
import re
import pprint


# this script is intended to parse the txt file that 
# was copied and pasted from a PDF file that contains
# the committee assignments of historical committee members
# A txt file is used as data source because parsing directly from
# a PDF file will result in misplaced or missed lines from the document
# copying and pasting into a txt file will avoid such risks
# the data source is only around ~10 files, and therefore 
# manually doing the copying and pasting is still practical
# reference for the raw PDF file is here: http://history.house.gov/Congressional-Overview/Profiles/112th/
# please refer to the "committee information" section


def parse_txt(file_name):
    file = open(file_name,'r')

    # the document looks like something like this:
     
    # garbage line
    # more garbage line
    # Ackerman, Gary L., 5th NY .......................... Financial Services.
    # Foreign Affairs.
    # Adams, Sandy, 24th FL ................................ Judiciary.
    # Science, Space, and Technology.
    
    # if the member is a delegate or resident commissioner it looks like this:
    # Faleomavaega, Eni F. H., .........................
    # (Delegate) AS
    # Foreign Affairs.
    # Natural Resources.
    
    # some special attentions needed for "select commitee ..." and "chairman":
    # Mica, John L., 7th FL ................................... Transportation and Infrastructure,
    # Chairman.
    # Miller, Jeff, 1st FL ........................................ Veterans' Affairs, Chairman.
    # Armed Services.
    # Permanent Select Committee on
    # Intelligence.
    
    # the pattern of the last four lines repeats until the end of the document


    result = []
    committee_assignment_header = None
    first_member_found = False
    for line in file:
        if re.search('[.][.]+',line):
            first_member_found = True
            is_delegate = False
            current_member = {}
            result.append(current_member)
            # more than one dot that appears consecutively
            # a new member appears
            current_member_info = re.search('.+ [.][.]',line).group()[:-2]
            # print 'current_member_info is ' + current_member_info
            # get display name
            if re.search('[a-zA-Z.,"() ]+[0-9]',current_member_info):
                display_name = re.search('[a-zA-Z.,"() ]+[0-9]',current_member_info).group()[:-3]
            elif re.search('[a-zA-Z.,"() ]+At Large',current_member_info):
                display_name = re.search('[a-zA-Z.,"() ]+At Large',current_member_info).group()[:-8]
            elif re.search('[a-zA-Z.,"()]+',current_member_info):
                # case of resident commissioners and delegates
                display_name = re.search('[a-zA-Z.,"() ]+',current_member_info).group().strip()[:-3]
                is_delegate = True
            else:
                display_name = None
                print 'failed to extract display name from ' + line
                continue
            current_member['display_name'] = display_name

            # TODO: parse display name
            

            # delegate needs special attention
            if is_delegate:
                continue

            # get congressional district number
            congressional_district = re.search('(At Large|[0-9]+)',current_member_info).group()
            current_member['congressional_district'] = congressional_district

            # get state
            state = re.search(' [A-Z][A-Z] ',current_member_info).group()[1:-1]
            current_member['state'] = state

            # get committee assignments
            current_member['committee_assignments'] = []
            try:
                committee_assignments_raw = re.search('[.][.] .*',line).group().strip()[3:]
                committee_assignments = re.findall('[^.]+',committee_assignments_raw)
                for committee_assignment in committee_assignments:
                    if len(committee_assignment.strip())>0:
                        if committee_assignment.strip()=='Chairman':
                            current_member['committee_assignments'][-1] = current_member['committee_assignments'][-1] + ' Chairman'
                        # print 'new assignment =' + committee_assignment
                        else:
                            if committee_assignment_header:
                                current_member['committee_assignments'].append(committee_assignment_header + ' ' + committee_assignment.strip())
                                committee_assignment_header = None
                            else:
                                current_member['committee_assignments'].append(committee_assignment.strip())
            except:
                print 'we skipped this line for extracting committee assignments because it ends with dot dot dot'
                print line

        elif re.search('[0-9a-zA-Z, \'()]+[.]',line) and first_member_found:      
            committee_assignments = re.findall('[^.]+',line)
            for committee_assignment in committee_assignments:
                if len(committee_assignment.strip())>0:
                    if committee_assignment.strip()=='Chairman':
                        current_member['committee_assignments'][-1] = current_member['committee_assignments'][-1] + ' Chairman'
                    # print 'new assignment =' + committee_assignment
                    else:
                        if committee_assignment_header:
                            current_member['committee_assignments'].append(committee_assignment_header + ' ' + committee_assignment.strip())
                            committee_assignment_header = None
                        else:
                            current_member['committee_assignments'].append(committee_assignment.strip())

        elif re.search('Select Committee',line):
            committee_assignment_header = line.strip()
            # print 'Select Committee needs attention'
        elif re.search('[(]Delegate[)]',line):
            # print line
            current_member['congressional_district'] = 'Delegate'
            current_member['state'] = re.search(' [A-Z][A-Z]',line).group()[1:]
            current_member['committee_assignments'] = []
        elif re.search('[(]Resident Commissioner[)]',line):
            # print line
            current_member['congressional_district'] = 'Resident Commissioner'
            current_member['state'] = re.search(' [A-Z][A-Z]',line).group()[1:]
            current_member['committee_assignments'] = []
        else:
            print 'it seems the following line does not contain any useful information'
            print line
    return result


# pprint.pprint(result)

if __name__ == '__main__':
    result = parse_txt('pdf.txt')
    with open('txt_data.JSON', 'w') as outfile:
        json.dump(result, outfile, indent=4)