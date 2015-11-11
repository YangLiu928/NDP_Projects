import house_vote_to_JSON as house
import senate_vote_to_JSON as senate


def get_voting_data(senate_or_house, congress_number):
    if senate_or_house == 'senate':
        data = senate.get_senate_roll_call_vote(congress_number)
        # TODO: prune and format the data
        return data
    elif senate_or_house == 'house':
        data = house.get_house_roll_call_vote_data(congress_number)
        # TODO: prune and format the data
        return data
    else:
        print 'please make sure you have input a correct parameter'
        print 'the first parameter of this function should be either\'senate\' or \'house\''
