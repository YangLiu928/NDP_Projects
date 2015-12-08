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
        CREATE TABLE `lr_v1`.`lrt_legislator` (
        `legislator_id` varchar(20) DEFAULT NULL,
        `type_cd` varchar(20) DEFAULT NULL,
        `first_name` varchar(50) DEFAULT NULL,
        `last_name` varchar(50) DEFAULT NULL,
        `display_name` varchar(100) DEFAULT NULL,
        `web_url`  varchar(300) DEFAULT NULL,
        `valid_from_dt` datetime DEFAULT NULL,
        `valid_to_dt` datetime DEFAULT NULL,
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
        valid_from_dt = 'NOW'

        # This is a date value that represents when the data in the
        # row is superseded by new data. For your purposes, this value will always
        # be null.  It will be used in the future when data will be updated.
        valid_to_dt = 'NULL'

        # this is the current date/time
        # use the SQL NOW() function
        insert_dt = 'NOW()'
        # this should be null.  It will be populated when the data is
        # updated in the future
        update_dt = 'NULL'

        # this should be null
        update_by = 'NULL'

        insert_query = """
            INSERT INTO `lr_v1`.`lrt_legislator`(`legislator_id`,`type_cd`,`first_name`,`last_name`,`display_name`,`web_url`,`valid_from_dt`,`valid_to_dt`,`insert_dt`,`update_dt`,`update_by`)
            VALUES ({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10});
        """.format(
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
        db.insert(insert_query)


def delete_table(db):
    delete_table_query = """
        DROP TABLE `lr_v1`.`lrt_legislator`;
    """

    print db.query(delete_table_query)


if __name__ == "__main__":
    db = Database()
    try:
        create_table(db)
        insert_values(db)
    except:
        print 'error occurred while populating the database'
    
    delete_table(db)
    db.close()