import json
import urllib2
from bs4 import BeautifulSoup
import lxml
import numpy as np
import pandas as pd
import xmldict
import re
import requests

# This constant is for checking if the website has changed
# If changed, we may need to modify our scraping strategy
WEB_STRUCTURE_FINGER_PRINT = ''


# leading underscore for "internal use only" functions, cannot call such functions from outside
def _get_senate_roll_call_vote_url(congress_number, session_number, vote_number):
    # an example of URL looks like:
    # http://www.senate.gov/legislative/LIS/roll_call_votes/vote1141/vote_114_1_00276.xml
    url = ''
    # components of desired url
    url_pieces = [
        'http://www.senate.gov/legislative/LIS/roll_call_votes/vote',
        str(congress_number),
        str(session_number),
        '/vote_',
        str(congress_number),
        '_',
        str(session_number),
        '_',
        str(vote_number).zfill(5),
        '.xml']
    for url_piece in url_pieces:
        url += url_piece
    return url


def _check_web_structure(url, finger_print):
    # TODO do something to check whether web structure has changed and our scraping strategy needs modification
    return False


def get_senate_roll_call_vote(congress_number):
    # compare
    web_structure_has_changed = _check_web_structure(_get_senate_roll_call_vote_url(congress_number, 1, 1),
                                                     WEB_STRUCTURE_FINGER_PRINT)
    if web_structure_has_changed:
        print 'the web structure has changed, we need to modify our code to adapt to the changes'
        return [None, None]
    # the function is meant to return the senate vote data as an array of dictionaries
    # The index of a specific vote data is vote_number - 1 due to zero based indexing system
    dicts = []
    # this opener adds a header to the HTTP requests, and mimic the behavior of a browser
    # in order to avoid 503 service not available error
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    # each congress has no more than 2 sessions
    session_number = 1
    while session_number < 3:
        # re-basing the vote number
        vote_number = 1
        while True:
            try:           
                url = _get_senate_roll_call_vote_url(congress_number, session_number, vote_number)
                # print url
                # dict=xmldict.xml_to_dict(requests.get(url).content)
                response = opener.open(url)
                dict = xmldict.xml_to_dict(response.read())
                internal_ids = _get_internal_ids(dict)
                dict['ndp_specs'] = {'internal_id': internal_ids[0], 'amendment_to_id': internal_ids[1]}
                vote_number += 1
                dicts.append(dict)
                print url
            except urllib2.HTTPError:
                # either the vote number has incremented high enough, or some unknown url error occurred
                print 'HTTPError occurred at '+ url
                break
        session_number += 1
    return dicts


def _get_internal_ids(dict):
    try:
        if dict['roll_call_vote']['amendment']['amendment_number']:
            # this is an amendment, if it is an amendment, it does not matter if it is a senate/house resoltion or bill
            return _get_amendment_ids(dict)
        elif re.search('Res.', dict['roll_call_vote']['document']['document_name']):
            # this is a senate or House resolution
            return [_get_resolution_internal_id(dict), None]
        elif re.search('[S.,H.R.]', dict['roll_call_vote']['document']['document_name']):
            # this is a senate or House bill
            return [_get_bill_internal_id(dict), None]
        else:
            # this is the fall back for PN# and errors if the structure of the XML has changed.
            return [None, None]
    except KeyError, TypeError:
        # dict = {'a':1,'b':2,'c':{'d':4,'e':5}}
        # dict['x'] returns KeyError, dict['a']['d'] returns TypeError
        # If they changed the XML structure, the Errors above may occur
        print 'Cannot get the internal id. The XML structure may have changed'
        return [None, None]


def _get_amendment_ids(dict):
    try:
        internal_id = ''
        # append the initial congress number (don't forget the dot)
        internal_id += dict['roll_call_vote']['document']['document_congress']
        internal_id += '.'
        # append the 'H.' or 'S.'
        internal_id += dict['roll_call_vote']['amendment']['amendment_number'][0:2]
        # append the 'A.' for resolution
        internal_id += 'A.'
        # append the resolution number
        # in this case we have to extract the amendment number from the amendment_number, which is a string (e.g. 'S.Amdt. 1')
        internal_id += re.search('[0-9]+', dict['roll_call_vote']['amendment']['amendment_number']).group()
        amendment_to_id = dict['roll_call_vote']['amendment']['amendment_to_document_number']
        return [internal_id, amendment_to_id]
    except KeyError, TypeError:
        # similar try-catch mechanism to the one in the get_internal_id function
        print 'Cannot get the internal id. The XML structure may have changed'
        return [None, None]


def _get_resolution_internal_id(dict):
    try:
        internal_id = ''
        # append the initial congress number (don't forget the dot)
        internal_id += dict['roll_call_vote']['document']['document_congress']
        internal_id += '.'
        # append the 'H.' or 'S.'
        # e.g.: string = 'abcd', and string[0:2] returns 'ab', left-closed, right-opened
        internal_id += dict['roll_call_vote']['document']['document_type'][0:2]
        # append the 'R.' for resolution
        internal_id += 'R.'
        # append the resolution number
        internal_id += dict['roll_call_vote']['document']['document_number']
        return internal_id
    except TypeError, KeyError:
        # similar try-catch mechanism to the one in the get_internal_id function
        print 'Cannot get the internal id. The XML structure may have changed'
        return None


def _get_bill_internal_id(dict):
    try:
        internal_id = ''
        # append the initial congress number (don't forget the dot)
        internal_id += dict['roll_call_vote']['document']['document_congress']
        internal_id += '.'
        # append the 'H.' or 'S.'
        # string = 'abcd', and string[0:2] returns 'ab', left-closed, right-opened
        internal_id += dict['roll_call_vote']['document']['document_type'][0:2]
        # append the 'B.' for Bill
        internal_id += 'B.'
        # append the bill number
        internal_id += dict['roll_call_vote']['document']['document_number']
        return internal_id
    except TypeError, KeyError:
        # similar try-catch mechanism to the one in the get_internal_id function
        print 'Cannot get the internal id. The XML structure may have changed'
        return None


if __name__ == '__main__':
    data = get_senate_roll_call_vote(111)
    # print data
    with open('internal_ids_111.JSON', 'w') as outfile:
        json.dump(data, outfile, indent=4)
