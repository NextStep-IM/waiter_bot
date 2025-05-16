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

