import psycopg2
import psycopg2.extras
from collections import namedtuple
from config import *

class PostgresDB(object):
    def __init__(self):
        self.params = parseConfig('PostgreSQL')
        self._db_connection = psycopg2.connect(**self.params)
        self._db_cur = self._db_connection.cursor()

    def query(self, query):
        return self._db_cur.execute(query, self.params)

    def test(self):
        self._db_cur.execute('Select version()')
        print(self._db_cur.fetchone())

    def createTacDataRawIfNotExists(self):
        try:
            self._db_cur.execute("""
                create table if not exists tac_data_raw(
                    startdate date,
                    enddate date,
                    needle varchar(100),
                    val varchar(100)
                )
            """)
            self._db_connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def bulkinsert(self, data):
        insert_query =  """INSERT INTO TAC_data_raw(startdate, enddate, needle, val)
            VALUES(%s)
        """

        try:
            with self._db_cur as cursor:
                cursor.copy_from(data, 'TAC_data_raw', columns = ('startdate', 'enddate', 'needle', 'val'))
                psycopg2.extras.execute_values(cursor, insert_query, data, template=None, page_size=1000)
            
            self._db_connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert(self, startdate, enddate, needle, val):
        try:
            self._db_cur.execute("""
                INSERT INTO TAC_data_raw(startdate, enddate, needle, val)
                VALUES(%s, %s, %s, %s)
            """, (startdate, enddate, needle, val)
            )
            self._db_connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def __del__(self):
        self._db_cur.close()
        self._db_connection.close()

if __name__ == '__main__':
    PostgresDB().test()