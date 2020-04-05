import psycopg2
import psycopg2.extras


class PostgresReader:
    def __init__(self, hostname, username, password, database='cd4ml'):
        self.conn = psycopg2.connect(dbname=database, user=username, password=password, host=hostname)

    def read_all_data_from_table(self, table_name="raw_data"):
        sql_query = "SELECT * FROM {0}".format(table_name)
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql_query)

        while True:
            results = cursor.fetchmany(10000)
            if not results:
                break

            for result in results:
                yield result

        cursor.close()

    def read_data(self):
        return self.read_all_data_from_table()

    def close(self):
        self.conn.close()
