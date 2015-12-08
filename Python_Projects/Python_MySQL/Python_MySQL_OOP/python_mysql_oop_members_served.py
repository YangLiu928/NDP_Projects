# ref: http://stackoverflow.com/questions/5687718/how-can-i-insert-data-into-a-mysql-database

import MySQLdb
import json
import time
from datetime import date


class Database:
    host = 'localhost'
    user = 'root'
    password = '890928'
    db = 'lr_v1'

    def __init__(self):
        self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
        self.cursor = self.connection.cursor()

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            print 'exception occurred while inserting'
            self.connection.rollback()

    def query(self, query):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        return cursor.fetchall()

    def close(self):
        self.connection.close()


def process_string_value(input):
    output = '\'' + input.replace('\'', '\'\'').replace('\"', '\"\"') + '\''
    return output


def create_table(db):
    # Create the table
    create_table_query = """
        CREATE TABLE `lr_v1`.`lrt_legislator_served` (
        `legislator_id` varchar(20) DEFAULT NULL,
        `branch_cd` varchar(20) DEFAULT NULL,
        `state_cd` varchar(20) DEFAULT NULL,
        `district_cd` varchar(20) DEFAULT NULL,
        `party_cd` varchar(20) DEFAULT NULL,
        `served_from_dt` datetime DEFAULT NULL,
        `served_to_dt` datetime DEFAULT NULL,
        `insert_dt` datetime DEFAULT NULL,
        `update_dt` datetime DEFAULT NULL,
        `update_by` varchar(30) DEFAULT NULL,
        KEY `idx_legislator_id` (`legislator_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """
    db.query(create_table_query)


def insert_values(db):
    with open('current_and_previous_committee_member_scraping_with_web_url_and_state_abbreviation.JSON') as data:
        members = json.load(data)
    for member in members:
        served_terms = member['served_terms']
        for served_term in served_terms:
            # This is the unique identifier we discussed that comes from the congress.gov source.
            legislator_id = process_string_value(member['id'])            

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
                district_cd = district_raw

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
            today = date.today()
            insert_dt = 'NOW()'

            # this should be null.  It will be populated when the data is
            # updated in the future
            update_dt = 'NULL'

            # this should be null
            update_by = 'NULL'

            insert_query = """
                INSERT INTO `lr_v1`.`lrt_legislator_served`(
                    `legislator_id`,
                    `branch_cd`,
                    `state_cd`,
                    `district_cd`,
                    `party_cd`,
                    `served_from_dt`,
                    `served_to_dt`,
                    `insert_dt`,
                    `update_dt`,
                    `update_by`)
                VALUES (
                    {0},
                    {1},
                    {2},
                    {3},
                    {4},
                    {5},
                    {6},
                    {7},
                    {8},
                    {9});
            """.format(
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

            db.insert(insert_query)


def delete_table(db):
    delete_table_query = """
        DROP TABLE `lr_v1`.`lrt_legislator_served`;
    """

if __name__ == "__main__":
    try: 
        db = Database()
        create_table(db)
        insert_values(db)
        print db.query('select count(*) from lrt_legislator_served where `branch_cd`=\'1018-2\'')
    except:
        print 'error occurred while populating the database'

    delete_table(db)
    db.close()