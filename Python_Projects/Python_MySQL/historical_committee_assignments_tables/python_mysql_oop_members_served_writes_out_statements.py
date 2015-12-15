import json
import time
from datetime import date


def process_string_value(input):
    output = '\'' + input.replace('\'', '\'\'').replace('\"', '\"\"') + '\''
    return output

def get_sql_statement(input,output):
    # this input file HAS to be the historical data rather than the
    # list of all committee members becasue you need to create an
    # insert query for each committee assignment of a member!

    with open(input) as data:
        members = json.load(data)

    file = open(output,'w')
    
    for member in members:
        committee_assignments = member['committee_assignments']
        for committee_assignment in committee_assignments:
            # This is the unique identifier we discussed that comes from the congress.gov source.
            # this id is not included in the input file, but rather in the complete list of committee
            # members from the congress.gov, therefore you need a function to do the dirty work
            # you need to member information to generate an intermediate id, which later maps to 
            # the complete list of committee members to fetch the legislator id we are interested in
            # the "intermediate id" will be explained in the _get_id function
            id = _get_id(member)
            legislator_id = process_string_value(id)            


            # this is a code that indicates senate or house.  The values are:
            # '1018-1' is for a Senate, and '1018-2' is for a member of the house of
            # representatives.
            where = served_term['where']
            if where=='Senate':
                branch_cd = process_string_value('1018-1')
            elif where == 'House':
                branch_cd = process_string_value('1018-2')
            else:
                print 'member ' + member['display_name'] + ' has a branch_cd of null'
                print 'served_term = ' + served_term
                branch_cd = 'NULL'

            state_cd = process_string_value(member['state'])

            # this should be an integer that represents the district
            # number. If it is a senator, you can use 0.  If the member is "at large"
            # you can use 1.
            district_raw = member['district']
            if district_raw == 'At Large':
                district_cd = process_string_value('1')
            elif district_raw == None:
                district_cd = process_string_value('0')
            else:
                district_cd = process_string_value(district_raw)

            # this is a code value that represents the political party.  The
            # values are: '1019-1' for Democrat, '1019-2' for Republican, '1019-3' for
            # Independent.  If you find other parties and need additional codes, let me
            # know.
            party_raw = member['party']
            if party_raw == 'Democratic':
                party_cd = process_string_value('1019-1')
            elif party_raw == 'Republican':
                party_cd = process_string_value('1019-2')
            elif party_raw == 'Independent':
                party_cd = process_string_value('1019-3')
            elif party_raw == 'Independent Democrat':
                party_cd = process_string_value('1019-1')
            else:
                print 'the party data of ' + member['display_name'] + ': ' + party_raw + ' needs attention'
                party_cd = 'NULL'

            # this is the date when their term started.
            served_from_dt = process_string_value(served_term['start_date'] + '-01-01')

            # this is the date when their service ended.  It will end if
            # they resign, retire, if they are defeated, or if any of the other values
            # above change.  In other words, if they change party, then the served_to_dt
            # will have a value indication when their membership in the old party ended,
            # and their will be another row indicating when the new party took affect.
            # For the initial population of current members, the served_to_dt will be
            # null. This value will be important for the historic data. We can discuss
            # this, I will need to make sure you understand what I mean for this.
            served_to_dt_raw = served_term['end_date']
            if served_to_dt_raw == None:
                served_to_dt = 'NULL'
            else:
                served_to_dt = process_string_value(served_to_dt_raw + '-12-31')

            # this is the current date/time
            # use the NOW function of SQL
            insert_dt = 'NOW()'

            # this should be null.  It will be populated when the data is
            # updated in the future
            update_dt = 'NULL'

            # this should be null
            update_by = 'NULL'

            insert_query = """INSERT INTO `lr_v1`.`lrt_legislator_served`(`legislator_id`,`branch_cd`,`state_cd`,`district_cd`,`party_cd`,`served_from_dt`,`served_to_dt`,`insert_dt`,`update_dt`,`update_by`)
VALUES ({0},{1},{2},{3},{4},{5},{6},{7},{8},{9});\n""".format(
                legislator_id,
                branch_cd,
                state_cd,
                district_cd,
                party_cd,
                served_from_dt,
                served_to_dt,
                insert_dt,
                update_dt,
                update_by)

            file.write(insert_query)
    file.close()

if __name__ == "__main__":
    input = 'current_and_previous_committee_member_scraping_with_web_url_and_state_abbreviation.JSON'
    output = 'legislator_served.sql'
    get_sql_statement(input,output)