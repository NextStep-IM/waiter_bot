import sys
import mariadb


class DBConnection:
    def __init__(self):
        try:
            self.conn = mariadb.connect(
                user="mysql",
                password="dustrunner41", # TODO: Find a way to hide this
                host="localhost",
                port=3306,
                database="waiter_bot_db",
                autocommit=False,
                reconnect=True # if connection died due to timeout or other errors.
            )
        except mariadb.Error as e:
            sys.exit(1)

    def execute_query(self, query: str, data: tuple):
        """
        Runs DDL or DML sql query

        :param query: The sql query
        :type query: str
        :param data: The values to replace the question marks (?) in the query
        :type data: tuple
        """
        with self.conn.cursor(prepared=True) as cur:
            self.conn.begin() # Start transaction
            try:
                cur.execute(query, data=data)
                self.conn.commit()
            except mariadb.Error as e:
                print(e.args)
                self.conn.rollback()
                raise e

    def read_query(self, query: str, data: tuple=()):
        """
        Runs DQL sql query

        :param query:
        :return:
        """
        with self.conn.cursor(prepared=True) as cur:
            # TODO: Make a custom exception
            try:
                cur.execute(query, data=data)
                result = cur.fetchall()
                if not result:
                    return [None]
                return result
            except Exception as e:
                print(e.args)
                raise e

def test_db():
    #query = 'INSERT INTO users(name, password) VALUES (?, ?)'
    #data = ('test_user_1', 'test_pass_1')
    query = 'SELECT name, password FROM users'
    db = DBConnection()
    # db.execute_query(query, data)
    print(db.read_query(query))

if __name__ == '__main__':
    test_db()