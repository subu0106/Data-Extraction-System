import pytest
from singleton_dbconnection import test_db_connection

def test_connection():
    assert test_db_connection() is True
