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
            # TODO: Try to throw the exception outside
            pass

    def execute_query(self, query: str, data: tuple):
        """
        Runs a sql query

        :param query: The sql query
        :param data: The values to replace the question marks (?) in the query
        :return: Result of the sql query
        """
        with self.conn.cursor(prepared=True) as cur:
            self.conn.begin() # Start transaction
            try:
                cur.execute(query, data=data)
                self.conn.commit()
            except Exception as e:
                # TODO: Try to throw the exception outside
                print(e.args)
                self.conn.rollback()
                raise e

