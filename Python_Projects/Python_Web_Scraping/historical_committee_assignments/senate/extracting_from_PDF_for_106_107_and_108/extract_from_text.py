import json
import re


def _get_state_abbreviation(state):
    state = state.strip()
    dictionary = {
        'Mississippi': 'MS',
        'Trust Territory of the Pacific Islands': 'TT',
        'Palau': 'PW',
        'Northern Mariana Islands': 'CM',
        'Oklahoma': 'OK',
        'Delaware': 'DE',
        'Minnesota': 'MN',
        'Illinois': 'IL',
        'Arkansas': 'AR',
        'New Mexico': 'NM',
        'Indiana': 'IN',
        'Maryland': 'MD',
        'Louisiana': 'LA',
        'Idaho': 'ID',
        'Wyoming': 'WY',
        'Federated States of Micronesia': 'FM',
        'Tennessee': 'TN',
        'Arizona': 'AZ',
        'Iowa': 'IA',
        'Michigan': 'MI',
        'Kansas': 'KS',
        'Utah': 'UT',
        'Virginia': 'VA',
        'Oregon': 'OR',
        'Connecticut': 'CT',
        'Montana': 'MT',
        'California': 'CA',
        'Massachusetts': 'MA',
        'West Virginia': 'WV',
        'South Carolina': 'SC',
        'New Hampshire': 'NH',
        'Philippine Islands': 'PI',
        'Wisconsin': 'WI',
        'Panama Canal Zone': 'CZ',
        'Europe': 'AE',
        'Vermont': 'VT',
        'Georgia': 'GA',
        'North Dakota': 'ND',
        'Pennsylvania': 'PA',
        'U.S. Armed Forces': 'AA',
        'Puerto Rico': 'PR',
        'Florida': 'FL',
        'Alaska': 'AK',
        'Kentucky': 'KY',
        'Hawaii': 'HI',
        'Marshall Islands': 'MH',
        'Nebraska': 'NB',
        'Missouri': 'MO',
        'Ohio': 'OH',
        'Alabama': 'AL',
        'New York': 'NY',
        'American Samoa': 'AS',
        'Virgin Islands': 'VI',
        'South Dakota': 'SD',
        'Colorado': 'CO',
        'New Jersey': 'NJ',
        'Guam': 'GU',
        'Washington': 'WA',
        'North Carolina': 'NC',
        'District of Columbia': 'DC',
        'Texas': 'TX',
        'Nevada': 'NV',
        'Pacific': 'AP',
        'Maine': 'ME',
        'Rhode Island': 'RI'
    }

    if state in dictionary.values():
        return state
    elif dictionary.has_key(state):
        return dictionary[state]
    else:
        print 'the full name of the state ' + state + ' does not exist in our library'
        return None


def _create_identifier(display_name, state):
    return '{0}, {1}'.format(display_name, state)


def extract_from_text(congress_number):
    file = open(str(congress_number) + '.txt', 'r')
    lines = []
    for line in file:
        line = line.replace('\n', '').strip()
        lines.append(line)
    file.close()

    results = {}
    member = ''
    current_committee_assignment = ''
    for line in lines:
        # we only look at lines that displays either a committee assignment or a member
        if _is_meaningful_line(line):
            line_type = _get_line_type(line)
            if line_type == 'member':
                display_name = _get_display_name(line)
                state = _get_state(line)
                identifier = _create_identifier(display_name, state)
                if results.has_key(identifier):
                    if _get_role(line) != 'member':
                        results[identifier]['committee_assignments'].append(
                            current_committee_assignment + ', ' + _get_role(line))
                    else:
                        results[identifier]['committee_assignments'].append(current_committee_assignment)
                else:
                    results[identifier] = {}
                    results[identifier]['state'] = state
                    results[identifier]['display_name'] = display_name
                    results[identifier]['committee_assignments'] = []
                    if _get_role(line) != 'member':
                        results[identifier]['committee_assignments'].append(
                            current_committee_assignment + ', ' + _get_role(line))
                    else:
                        results[identifier]['committee_assignments'].append(current_committee_assignment)
            elif line_type == 'assignment':
                current_committee_assignment = line.strip().title().replace('And', 'and')
            # print 'here is a new committee ' + current_committee_assignment
            else:
                print 'this line is neither a committe nor a member'
                print line
                print '\n'
    return results


def _is_meaningful_line(line):
    # we want to do the replace because lines line the following is usually seen
    # __________ , ________________
    # _____________________________
    # where there is essentially no information within the line
    line = line.replace('_', '').strip()
    line = line.replace('\n', '').strip()

    # this black list is basically the lines we already know that are not effective information
    # but at the same time difficult to distinguish from a committee name which is also usually
    # displayed as a string in all caps. the comma is basically the line of "_____ , ____" with
    # underscore replaced with an empty string
    black_list = ['COMMITTEE ASSIGNMENTS', 'STANDING COMMITTEES', ',']

    # total five conditions where the line contains no effective information:
    # (1) lines that contains brackets [], because they are typically strings representing page numbers (e.g. "[[Page (6)]]")
    # (2) lines that are basically an empty string after the strip() function, meaning the line was just a bunch of white space
    # (3) lines that are in the black list we pre-defined
    # (4) lines where the word "Room" appears. This is to exclude the titles under each committe assignments that states where and
    # when a certain meeting will be held. This actually not needed because the function _get_line_type should return this as a None
    # type line, but, again, this is just for completeness and ruling out anything that we already know we do not need
    # (5) lines where, after replacing underscore with empty string and stripping, only one or multiple '\n' were left
    # This is added because we still see some empty lines printed out from the _get_line_type function
    if (re.search('[\[\]]', line) != None) or (line == '') or (line in black_list):
        return False
    else:
        # print line + ' is meaningful'
        return True


def _get_line_type(line):
    # this function is intended to return whether the current line we are working with is a line
    # that contains committee assignment information or a specific member's identify
    line = line.strip()

    # .upper() changes everything within a string to its upper-case counterpart
    # if line.upper() == line, the entire line must originally be all in caps, which
    # indicates this is a line that represents the committee assignment name of a new block
    if line.upper() == line:
        # this is just for degugging.....
        # print line + ' is an assignment'
        return 'assignment'
    elif re.search(', of ', line):
        # name, of state_full_name(, Chairman) <== optional
        return 'member'
    else:
        # The following lines prints out the lines that are not recognized as either a name or an assignment
        # this is mainly for debugging purpose to make sure no important information was overlooked
        print 'the following line was not recognized as either assignment or member'
        print line
        print '\n'
        return None


def _get_display_name(member_line):
    # Barbara A. Mikulski, of Maryland, Chairman
    return member_line.split(', of ')[0]


def _get_state(member_line):
    # Barbara A. Mikulski, of Maryland, Chairman
    state_raw = member_line.split(', of ')[1].split(', ')[0]
    state_abbrev = _get_state_abbreviation(state_raw)
    return state_abbrev


def _get_role(member_line):
    # Barbara A. Mikulski, of Maryland, Chairman
    if len(member_line.split(', of ')[1].split(', ')) == 2:
        return member_line.split(', of ')[1].split(', ')[1]
    elif len(member_line.split(', of ')[1].split(', ')) == 1:
        return 'member'
    else:
        # this prints out the lines where members' role in the committee was not recognized
        # This is mainly for making sure we do not overlook any line that contains important
        # information
        print 'cannot extract role from the follow line'
        print member_line
        print '\n'


if __name__ == '__main__':
    congress_number = 108
    data = extract_from_text(congress_number)
    with open('output_{0}.json'.format(str(congress_number)), 'w') as outfile:
        json.dump(data, outfile, indent=4)
