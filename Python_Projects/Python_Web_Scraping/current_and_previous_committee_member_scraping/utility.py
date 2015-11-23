def get_state_abbreviation(state_full):
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
    if dictionary[state_full]:
        return dictionary[state_full]
    else:
        print 'the full name of the state ' + state_full + ' does not exist in our library'
        return None


# def get_party_abbreviation(party_full):
#     if party_full == 'Republican' or 'republican' or 'R' or 'r':
#         return 'R'
#     elif party_full == 'Democratics'
