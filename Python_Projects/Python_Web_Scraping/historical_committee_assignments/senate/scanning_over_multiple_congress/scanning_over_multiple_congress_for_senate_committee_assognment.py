import json
import re
import urllib2
from bs4 import BeautifulSoup

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


def _get_soup(url):
    # returns a beautiful soup object for further operations
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url, timeout=6)
    return BeautifulSoup(response.read(), 'lxml')


def _get_url(year, month, day):
    # The web pages for each of the senate committee assignment follows
    # a certain pattern, where the parameters include congress, year, month and day
    # the congress can be reversely calculated from the year
    congress_number = str(_get_congress_number(year))
    year = str(year)
    month = str(month).zfill(2)
    day = str(day).zfill(2)
    url = 'https://www.gpo.gov/fdsys/pkg/CCAL-{c}scal-{y}-{m}-{d}/html/CCAL-{c}scal-{y}-{m}-{d}-pt2.htm' \
        .format(c=congress_number, y=year, m=month, d=day)
    return url


def _get_years(congress_number):
    # linear algebra that maps a congress_number into the two years it covers
    return [2 * congress_number + 1787, 2 * congress_number + 1788]


def _get_congress_number(year):
    # this function is intended to calculate the congress_number
    # from a year that it represents. This is basically the reverse
    # function of _get_years, where the only minor attention needed
    # is to determine whether the year is an even or odd number
    if year % 2 == 1:
        return (year - 1787) / 2
    else:
        return (year - 1788) / 2


def _is_valid_page(soup):
    # this function is intended to check whether the url from which the soup
    # was generated was a valid url that displays senate committee assignments.
    # if an invalid url was used, either the _get_soup function raise an HTTPError
    # or we reach a page where "Error Detected - The page you requested cannot be found."
    # is displayed. This function here is therefore not mandatory required but instead
    # recommended just in case we miss anything
    text = soup.text
    if re.search('Error Detected - The page you requested cannot be found.', text):
        return False
    else:
        return True


def _get_date_from_url(url):
    # this function is needed in order to extract the date when the committee assignment
    # web page was published. the date can be directly inferred from the url
    base_index = url.find('scal-')
    # year = url[base_index+5:base_index+9]
    # month = url[base_index+10:base_index+12]
    # day = url[base_index+13:base_index+15]
    return url[base_index + 5:base_index + 15]


def _create_identifier(display_name, state):
    return '{0}, {1}'.format(display_name, state)


def _get_committee_assignments(soup):
    # this function is intended to parse the HTML of a web page that displays the senate
    # committee assignment, and return it as a dictionary where the display_name of a
    # member is used as the key. The contents included in each member include state (full state name),
    # and a list of committee assignments, where within the committee assignments regular and chairman
    # memberships are treated separately
    text = soup.find('pre').text
    lines = text.split('\n')

    results = {}
    current_committee_assignment = ''
    for line in lines:
        # we only look at lines that displays either a committee assignment or a member
        if _is_meaningful_line(line):
            line_type = _get_line_type(line)
            if line_type == 'member':
                display_name = _get_display_name(line)
                state = _get_state(line)
                identifier = _create_identifier(display_name, state)
                # role = _get_role(line)
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
    line = line.replace('_', '').replace('-', '').strip()

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
        # this is just for debugging.....
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


def scan_on_a_congress_number(congress_number):
    years = _get_years(congress_number)
    months = range(1, 13)
    days = range(1, 32)

    urls = []
    for year in years:
        for month in months:
            for day in days:
                url = _get_url(year, month, day)
                urls.append(url)

    print '****** Finished creating all urls for congress ' + str(congress_number)

    soups = []
    valid_dates = []
    for url in urls:
        print 'trying to fetch html from ' + url
        while True:
            try:
                soup = _get_soup(url)
                soups.append(soup)
                date = _get_date_from_url(url)
                valid_dates.append(date)
                print 'successfully fetched html from ' + url
                break
            except urllib2.HTTPError:
                print '404 occurred at ' + url
                break
            except:
                print 'failed to fetch html from ' + url
                # time.sleep(10)
                continue



            # try:
            # 	soup = _get_soup(url)
            # 	soups.append(soup)
            # 	date = _get_date_from_url(url)
            # 	valid_dates.append(date)
            # except urllib2.HTTPError:
            # 	continue
            # 	# print 'HTTPError occurred at ' + url
            # except urllib2.URLError:
            # 	continue
            # 	# print 'URLError occurred at ' + url
            # except socket.error:
            # 	while True:
            # 		try:
            # 			print '****** trying to access again ' + url
            # 			time.sleep(5)
            # 			soup = _get_soup(url)
            # 			soups.append(soup)
            # 			date = _get_date_from_url(url)
            # 			valid_dates.append(date)
            # 			print '****** re-accessing succeeded'
            # 			break
            # 		except:
            # 			print '***** re-accessing failed, will try again'
            # 			continue
            # except:
            # 	print '**** An unexpect error occurred at ' + url
            # 	raise
            # 	continue

    print '****** Finshied downloading all htmls for congress' + str(congress_number)

    all_committee_assignment_data = []

    for soup in soups:
        committee_assignment_data = _get_committee_assignments(soup)
        all_committee_assignment_data.append(committee_assignment_data)

    print '****** Finished fetching all committee assignment data for congress ' + str(congress_number)
    # with open('scan_on_112_congress_local_data.JSON','w') as outfile:
    # 	json.dump(all_committee_assignment_data, outfile, indent=4)

    # with open('valid_dates.JSON','w') as outfile:
    # 	json.dump(valid_dates, outfile, indent=4)

    result = {}
    for index in range(0, len(all_committee_assignment_data)):
        members = all_committee_assignment_data[index]
        # keys are basically all the display_name of the members in the members json data
        keys = members.keys()
        for key in keys:
            # we need to scan over all keys within an element from the all_committee_assignment_data dictionary
            if result.has_key(key):
                # if a key is already in the result dictionary, it means that this member appearred in previous
                # all_committee_assignment_data element, what we need to do here is to update the 'last_seen_date'
                # which is within the committee_assignments field
                for committee_assignment_name in members[key]['committee_assignments']:
                    # when updating the 'last_seen_date', we need to the consider two situations
                    # (1) when the member is continuing servicing the same committee assignment
                    # (2) when the member has received a new committee assignment, where we need to create an entry for this
                    # new committee assignment before we update the 'last_seen_date' (like an initialization)
                    if result[key]['committee_assignments'].has_key(committee_assignment_name):
                        result[key]['committee_assignments'][committee_assignment_name]['last_seen_date'] = valid_dates[
                            index]
                    else:
                        result[key]['committee_assignments'][committee_assignment_name] = {}
                        result[key]['committee_assignments'][committee_assignment_name]['start_date'] = valid_dates[
                            index]
                        result[key]['committee_assignments'][committee_assignment_name]['last_seen_date'] = valid_dates[
                            index]
            else:
                # if a member has not been added to the result yet, we create an element for him/her
                # this is basically an initialization
                result[key] = {}
                result[key]['state'] = members[key]['state']
                result[key]['display_name'] = members[key]['display_name']
                result[key]['committee_assignments'] = {}
                for committee_assignment_name in members[key]['committee_assignments']:
                    result[key]['committee_assignments'][committee_assignment_name] = {}
                    result[key]['committee_assignments'][committee_assignment_name]['start_date'] = valid_dates[index]
                    result[key]['committee_assignments'][committee_assignment_name]['last_seen_date'] = valid_dates[index]
    # print 'finished parsing all data'
    return result


def scan_on_multiple_congress_number(starting_congress, ending_congress):
    # this function is intended to fetch and parse senate committee assignment data
    # over certain congresses, and keep track of the service time frame of the committee assignment
    # of each senate member. This approach is not perfect in that it only keeps track of the first
    # and last seen date of a commitee assignment for a member, and therefore if a member leaves a
    # committee for a period of time and then returned, what we saw would be 'he was in the committee'
    # for the whole time', which is not exactly true
    result = {}
    for congress_number in range(starting_congress, ending_congress + 1):
        data = scan_on_a_congress_number(congress_number)
        for key in data.keys():
            if result.has_key(key):
                for committee_assignment_name in data[key]['committee_assignments']:
                    if result[key]['committee_assignments'].has_key(committee_assignment_name):
                        result[key]['committee_assignments'][committee_assignment_name]['last_seen_date'] = \
                            data[key]['committee_assignments'][committee_assignment_name]['last_seen_date']
                    else:
                        # this one liner basically does what it does with the three lines that were commented out
                        result[key]['committee_assignments'][committee_assignment_name] = \
                        data[key]['committee_assignments'][committee_assignment_name]
                    # result[key]['committee_assignments'][committee_assignment_name] = {}
                    # result[key]['committee_assignments'][committee_assignment_name]['start_date'] = data[key]['committee_assignments'][committee_assignment_name]['start_date']
                    # result[key]['committee_assignments'][committee_assignment_name]['last_seen_date'] = data[key]['committee_assignments'][committee_assignment_name]['last_seen_date']
            else:
                result[key] = data[key]
    return result


if __name__ == '__main__':
    data = scan_on_multiple_congress_number(109, 114)
    with open('scan_on_109_to_114_congress_new.JSON', 'w') as outfile:
        json.dump(data, outfile, indent=4)

    # data = scan_on_a_congress_number(112)
    # with open('scan_on_112_congress.JSON','w') as outfile:
    # 	json.dump(data, outfile, indent=4)
