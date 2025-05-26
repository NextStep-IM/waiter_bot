import sys
from typing import List, Tuple, Any
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

    def _execute_query(self, query: str, data: tuple):
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

    def _read_query(self, query: str, data: tuple=()) -> List[Tuple[Any, ...]]:
        """
        Runs DQL sql query

        :param query: The SQL query
        :type query: str
        :param data: The values to replace the question marks (?) in the query
        :type data: tuple
        :return: Result of the query
        :rtype: List[Tuple[Any, ...]]
        :raises mariadb.Error: Raises exception if execute() or fetchall() could not run properly
        """
        with self.conn.cursor(prepared=True) as cur:
            try:
                cur.execute(query, data=data)
                result = cur.fetchall()
                if not result:
                    return [(None,)]
            except mariadb.Error as e:
                print(e.args)
                raise e
        return result

    def user_exists(self, name:str) -> bool:
        query = 'SELECT name FROM users WHERE name = ?'
        data = (name,)
        try:
            result = self._read_query(query, data)[0]
        except mariadb.Error as e:
            raise e
        if not result[0]:
            return False
        return True

    def signup_user(self, name: str, password: str):
        query = 'INSERT INTO users (name, password) VALUES (?, ?)'
        data = (name, password)
        try:
            self._execute_query(query, data)
        except mariadb.Error as e:
            raise e

    def authenticate_user(self, name, password) -> bool:
        """
        Authenticates user

        :param name: Username
        :param password: Password
        :return: True if user is cleared otherwise False.
        :rtype: bool
        :raises mariadb.Error: Raises exception if an exception is caught when executing query
        """
        query = 'SELECT name, password FROM users WHERE name = ?'
        data = (name,)
        try:
            result = self._read_query(query, data)[0]
        except mariadb.Error as e:
            raise e
        if not result[0]:
            return False
        n, p = result
        if not (n == name and p == password):
            return False
        return True

    def get_user_history(self, name) -> List[Tuple[Any, ...]]:
        """
        Retrieve all the contents of the recipes the user has liked before.

        :param name: Username
        :return: Recipes' contents
        :rtype: List[Tuple[Any, ...]]
        """
        query = ''
        with open('queries/get_user_history.sql') as q:
            query = q.read()
        data = (name,)
        try:
            result = self._read_query(query, data)
        except mariadb.Error as e:
            raise e
        return result

def main():
    db = DBConnection()
    print(db.get_user_history('test_user_1'))

if __name__ == '__main__':
    main()