# ref: http://stackoverflow.com/questions/5687718/how-can-i-insert-data-into-a-mysql-database

import MySQLdb
import json
import time
from datetime import date

def process_string_value(input):
    output = '\'' + input.replace('\'', '\'\'').replace('\"', '\"\"') + '\''
    return output

def get_sql_statements():
    with open('current_and_previous_committee_member_scraping_with_web_url_and_state_abbreviation.JSON') as data:
        members = json.load(data)
    output = open('members_sql_satement.sql','w')
    for member in members:
        # This is the unique identifier we discussed that comes from the congress.gov source.
        legislator_id = process_string_value(member['id'])

        # This is a code value that will be used to identify a particular
        # legislature.  At this time all of the ones are from the US Congress.
        # Therefore all rows for now will have the same value.  The value that
        # should be used is '1016-1'.  In the future we may do state legislatures,
        # and each one will have a different value here ('1016-2', '1016-3', ... etc).
        type_cd = process_string_value('1016-1')

        first_name = process_string_value(member['first_name'])
        last_name = process_string_value(member['last_name'])
        display_name = process_string_value(member['display_name'])
        # TODO: need better web_url than just the href in the Conrgess.gov
        if member['web_url']:
            web_url = process_string_value(member['web_url'])
        else:
            web_url = 'NULL'

        # This is a date value that will represent when the data in
        # the row became valid. For now, you can just use the current date/time.
        today = date.today()
        valid_from_dt = process_string_value('{2}-{0}-{1}'.format(today.month, today.day, today.year))

        # This is a date value that represents when the data in the
        # row is superseded by new data. For your purposes, this value will always
        # be null.  It will be used in the future when data will be updated.
        valid_to_dt = 'NULL'

        # this is the current date/time
        today = date.today()
        insert_dt = process_string_value('{2}-{0}-{1}'.format(today.month, today.day, today.year))

        # this should be null.  It will be populated when the data is
        # updated in the future
        update_dt = 'NULL'

        # this should be null
        update_by = 'NULL'

        insert_query = """
        INSERT INTO `lr_v1`.`lrt_legislator`(`legislator_id`,`type_cd`,`first_name`,`last_name`,`display_name`,`web_url`,`valid_from_dt`,`valid_to_dt`,`insert_dt`,`update_dt`,`update_by`)
        VALUES ({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10});""".format(
            legislator_id,
            type_cd,
            first_name,
            last_name,
            display_name,
            web_url,
            valid_from_dt,
            valid_to_dt,
            insert_dt,
            update_dt,
            update_by)
        output.write(insert_query)
    output.close()


if __name__ == "__main__":
    get_sql_statements()