import json
import re
import urllib2
import utility

from bs4 import BeautifulSoup


def _get_url(page_number):
    # the number of results on each page can also be specified in the url
    # by listing a large number of results on each page may result in 
    # less number of queries, but larger traffic in each query,
    # which may or may not improve the performance of this program
    URL_HEAD = 'https://www.congress.gov/members?page='
    return URL_HEAD + str(page_number)


def _last_page_reached(soup):
    # when "page_number" has exceeded the number of maximum pages
    # the website basically stick at the last available page
    # and does not change even if you increase the page number in the url
    # example url as described above: https://www.congress.gov/members?page=89
    # as of Nov. 18 2015, only 88 pages available, inputing 89 or even 100 only
    # shows still the last page (88)
    # The indicator for this case is the 'next' button at the bottom of the page
    # if the next button (an anchor tag actually) has a class of 'next off'
    # that means the next page is not available

    # ADDITIONALLY:
    # when "page_number" is super large, this website shows a page saying
    # "this content is currently not available" rather than throwing an HTTP error
    # example url as described above: https://www.congress.gov/members?page=10000000000000000000000000
    # if the page contains committee member information
    # there will be a <div> with id 'main'
    # this <div> is not displayed if the page contains no result (as described above)
    # and therefore used as a indicator
    if not soup.find(id='main'):
        # cannot find div with id 'main', the second case mentioned above
        return True
    elif soup.find(id='main').find('div', class_='nav-pag-top').find('div', class_='pagination').find_all('a',
                                                                                                          recursive=False)[
        -1]['class'][-1] == 'off':
        return True
    else:
        return False


def _website_structure_has_changed():
    # determine whether the website structure being scraped has changed
    WEBSITE_FINGER_PRINT = 'some hash code'
    SEED_URL = 'https://www.congress.gov/members?page=1'
    # TODO: do something to determine whether the website has changed
    # if not we can continue, otherwise we may need to re-design some of the functions
    return False


def _get_soup(url):
    # returns a beautiful soup object for further operations
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)
    return BeautifulSoup(response.read(), 'lxml')


def _parse_display_name(display_name):
    name_pieces = {}
    # further parse the display_name
    # typical name display scenarios:
    # last, first
    # last, first MI.
    # last, first MI., suffix.
    # last, first MI. "nick name"
    # last, first "nick name"
    # last, first (nick name)
    # last, first, suffix.
    partials = display_name.split(', ')

    # get the last name
    last_name = partials[0]
    name_pieces['last_name'] = last_name

    # get the first name
    if len(partials[1].split(' ')) == 1:
        # case of last, first and last, first, suffix
        first_name = partials[1]
    else:
        # all other three cases
        first_name = partials[1].split(' ')[0]
    name_pieces['first_name'] = first_name

    # get the middle name
    if len(partials[1].split(' ')) == 1:
        # case of last, first and last, first, suffix
        middle_name = None
    elif len(partials[1].split(' ')) == 2 and re.match('["]\w+["]', partials[1].split(' ')[1]):
        # case of last, first "nick name"
        middle_name = None
    else:
        # all other cases
        middle_name = partials[1].split(' ')[1]
    name_pieces['middle_name'] = middle_name

    # get the suffix
    if len(partials) == 3:
        suffix = partials[2]
    else:
        suffix = None
    name_pieces['suffix'] = suffix

    # get the nick name
    if re.search('["][a-zA-Z]+["]', display_name):
        nick_name = re.search('["][a-zA-Z]+["]', display_name).group()[1:-1]
    elif re.search('[(][a-zA-Z]+[)]', display_name):
        nick_name = re.search('[(][a-zA-Z]+[)]', display_name).group()[1:-1]
    else:
        nick_name = None
    name_pieces['nick_name'] = nick_name

    return name_pieces


def _get_member_data(member):
    print re.search(' .+', str(member.a.string)).group()[1:] + '\'s data has been fetched'
    # function takes in a member information as beautiful soup object
    # and returns a dictionary with information parsed
    result = {}

    # get the display name
    display_name = re.search(' .+', str(member.a.string)).group()[1:]
    result['display_name'] = display_name

    # get the name parsed and extract parsed pieces
    name_pieces = _parse_display_name(display_name)
    result['last_name'] = name_pieces['last_name']
    result['first_name'] = name_pieces['first_name']
    result['suffix'] = name_pieces['suffix']
    result['middle_name'] = name_pieces['middle_name']
    result['nick_name'] = name_pieces['nick_name']


    # get the membership
    if re.search('Representative', member.a.string):
        membership = 'Representative'
    elif re.search('Senator', member.a.string):
        membership = 'Senator'
    else:
        membership = None
    result['membership'] = membership

    # get the id
    # always last 7 digits in the href of the anchor tag
    id = member.a['href'][-7:]
    result['id'] = id

    # TODO: we can get more detailed information about the member using the url in the anchor tag
    anchor_href = member.find('h2').find('a')['href']
    
    # counter counts how many times the url has been accessed
    # we try at most three times, and if the connection fails 
    # continuously, we still fail

    counter = 1
    while True:
        try:
            member_detail_page_soup = _get_soup(anchor_href)
            break
        except:
            counter+=1
            print '************************* we failed to connect to '+ anchor_href +" for the "+str(counter) + " time ************************"
            continue

    member_profile = member_detail_page_soup.find('div',class_='member_profile').find_all('table')[1]
    if member_profile.find('a'):
        web_url = member_profile.find('a')['href']
    else:
        web_url = None
    result['web_url'] = web_url

    # this member_profile is an array of <tr> tags with state/party/district/term information
    member_profile = member.find('div', class_='memberProfile').find_all('tr')

    # get the state
    # the mapping from full state name to abbreviation can also be done
    state_full = member_profile[0].td.string
    state_abbrev = utility.get_state_abbreviation(state_full)
    result['state'] = state_abbrev

    # get the party
    party = member_profile[-2].td.string
    result['party'] = party

    # get the served terms
    # served_terms is an array of dictionaries or JSON objects
    served_terms = []
    terms = member_profile[-1].td.find_all('li')
    for term in terms:
        where = re.findall('[a-zA-Z]+',term.string)[0] 
        # possible formats:
        # 'House: 1990-1999'
        # 'Senate: 2011-present'
        # 'House: 1990-1998, 1999-2002'
        # the start date is definitely a number
        # the end date might be the word 'present'
        # needs appropriate handling for all these cases
        dates = re.findall('[0-9]+',term.string)
        if len(dates) % 2 == 1:
            # there are odd numbers of year in the string
            # append an None at the end of the string
            # this None served as a replacement of the 'present' string
            # from the original string
            dates.append(None)
            # otherwise there are even numbers of year in the string
            # every two years is a pair, no action needed
        for i in range (0, len(dates), 2):
            start_date = dates[i]
            end_date = dates[i + 1]
            term_object = {}
            term_object['where'] = where
            term_object['start_date'] = start_date
            term_object['end_date'] = end_date
            served_terms.append(term_object)
    result['served_terms'] = served_terms

    # get whether the member is a former or current member
    # present the value to 'former'
    # examine all the elements in served terms
    # if any one of those ends with a None (representing 'present')
    # the value will be set to 'current'
    current_or_former = 'former'
    for served_term in served_terms:
        if not served_term['end_date']:
            current_or_former = 'current'
    result['current_or_former'] = current_or_former

    # get the district
    if member_profile[1].th.string == 'District:':
        district = member_profile[1].td.string
    else:
        # this None conventional may need to be re-considered
        # in the scraping for current list of committee at large and 
        # Delegate/resident commissioner are handled differently
        district = None
    result['district'] = district

    # return the results
    return result


def _get_state_abbreviation(state_full):
    # TODO: get the mapping from a reliable source
    return


def get_committee_data():
    if _website_structure_has_changed():
        print 'the website structure at https://www.congress.gov/members?page=1 has changed'
        print 'the program needs to be re-adjusted for the new structure'
    else:
        results = []
        page_number = 1
        while True:
            url = _get_url(page_number)
            soup = _get_soup(url)
            if _last_page_reached(soup):
                # if reached, we get rid of the loop
                break
            else:
                # Note: recursive = False means only detect <li> tag that is one level down
                # otherwise you get all the <li> elements, including the nested ones
                members = soup.find(id='main').find('ol').find_all('li', recursive=False)
                for member in members:
                    results.append(_get_member_data(member))
            page_number += 1
    return results


if __name__ == '__main__':
    data = get_committee_data()
    with open('current_and_previous_committee_member_scraping_with_web_url_and_state_abbreviation.JSON', 'w') as outfile:
        json.dump(data, outfile, indent=4)
