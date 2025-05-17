import pytest
from unittest.mock import MagicMock, patch
from backend.database import DBConnection
import mariadb

# Sample queries
SAMPLE_INSERT_QUERY = "INSERT INTO users (username, password) VALUES (?, ?)"
SAMPLE_SELECT_QUERY = "SELECT * FROM users WHERE username = ?"
SAMPLE_DATA = ("admin", "123")

@patch("backend.database.mariadb.connect")
def test_execute_query_success(mock_connect):
    # Mock the DB connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    db = DBConnection()
    db.execute_query(SAMPLE_INSERT_QUERY, SAMPLE_DATA)

    mock_conn.begin.assert_called_once()
    mock_cursor.execute.assert_called_once_with(SAMPLE_INSERT_QUERY, data=SAMPLE_DATA)
    mock_conn.commit.assert_called_once()

@patch("backend.database.mariadb.connect")
def test_execute_query_failure(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    # Simulate a DB error
    mock_cursor.execute.side_effect = mariadb.Error("Query failed")

    db = DBConnection()

    with pytest.raises(mariadb.Error):
        db.execute_query(SAMPLE_INSERT_QUERY, SAMPLE_DATA)

    mock_conn.rollback.assert_called_once()

@patch("backend.database.mariadb.connect")
def test_read_query_success(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [("admin", "123")]

    db = DBConnection()
    result = db.read_query(SAMPLE_SELECT_QUERY, ("admin",))

    mock_cursor.execute.assert_called_once_with(SAMPLE_SELECT_QUERY, data=("admin",))
    assert result == [("admin", "123")]

@patch("backend.database.mariadb.connect")
def test_read_query_no_results(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchall.return_value = []

    db = DBConnection()
    result = db.read_query(SAMPLE_SELECT_QUERY, ("ghost",))

    assert result == [(None,)]

@patch("backend.database.mariadb.connect")
def test_read_query_failure(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.execute.side_effect = mariadb.Error("DB error")

    db = DBConnection()
    with pytest.raises(mariadb.Error):
        db.read_query(SAMPLE_SELECT_QUERY, ("admin",))
