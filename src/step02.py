"""
PET demo - second iteration

"""

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
            CREATE TABLE contact(
                name text
            );

            CREATE TABLE address(
                address text,
                contactid integer,
                FOREIGN KEY(contactid) REFERENCES contact(rowid)
            );

            CREATE TABLE email(
                email text,
                contactid integer,
                FOREIGN KEY(contactid) REFERENCES contact(rowid)
            );

            CREATE TABLE identification(
                identification integer,
                contactid integer,
                FOREIGN KEY(contactid) REFERENCES contact(rowid)
            );
        """)


def fill_database(database_path):
    """
    fill a database with sample data
    :param database_path: path to the database file
    """
    with database.Database(database_path) as db:
        for contact in contacts.CONTACTS:
            contactid = db.execute("INSERT INTO contact VALUES (?)", (contact[0],)).lastrowid
            db.execute("INSERT INTO address VALUES (?, ?)", (contact[1], contactid))
            db.execute("INSERT INTO email VALUES (?, ?)", (contact[2], contactid))
            db.execute("INSERT INTO identification VALUES (?, ?)", (contact[3], contactid))


def read_database(database_path):
    """
    read a database and produce the rows
    :param database_path: path to the database file
    """
    with database.Database(database_path) as db:
        for row in db.execute("""
            SELECT c.name, a.address, e.email, i.identification
            FROM contact c, address a, email e, identification i
            WHERE a.contactid = c.rowid
            AND e.contactid = c.rowid
            AND i.contactid = c.rowid
        """):
            yield row


def main():
    p = util.make_database_path(__file__)
    if not p.is_file():
        create_database(p)
        fill_database(p)
    output.database_rows(read_database(p))


if __name__ == "__main__":
    main()
