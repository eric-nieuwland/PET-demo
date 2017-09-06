"""
PET demo - first step

This script is the starting point.
It defines a simple database with one table to hold the contact info.
Adding rows of data is straight forward, as is retrieving data.
"""
import os

from common import contacts
from common import util
from common import database
from common import output


def create_database(database_path):
    """
    create a fresh database
    :param database_path: path to the database file
    """
    with database.Database(database_path, False) as db:
        db.executescript("""
            CREATE TABLE
            contact(
                name text,
                address text,
                email text,
                identification integer
            );
        """)


def fill_database(database_path):
    """
    fill a database with sample data
    :param database_path: path to the database file
    """
    with database.Database(database_path) as db:
        db.executemany("INSERT INTO contact VALUES (?, ?, ?, ?)", contacts.CONTACTS)


def read_database(database_path):
    """
    read a database and produce the rows
    :param database_path: path to the database file
    """
    with database.Database(database_path) as db:
        for row in db.execute("SELECT * FROM contact"):
            yield row


def main():
    p = util.make_database_path(__file__)
    if not os.path.isfile(p):
        create_database(p)
        fill_database(p)
    output.database_rows(read_database(p))


if __name__ == "__main__":
    main()
