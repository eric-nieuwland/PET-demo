"""
PET demo - third iteration

"""
from pathlib import Path

from common import contacts
from common import util
from common import database
from common import output
from common import hasher


def create_database(database_path: Path):
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
                contactid text
            );

            CREATE TABLE email(
                email text,
                contactid text
            );

            CREATE TABLE identification(
                identification integer,
                contactid text
            );
        """)


def fill_database(database_path: Path):
    """
    fill a database with sample data
    :param database_path: path to the database file
    """
    with database.Database(database_path) as db:
        for contact in contacts.CONTACTS:
            contactid = db.execute("INSERT INTO contact VALUES (?)", (contact[0],)).lastrowid
            hashed_contactid = hasher.make_id_hash(contactid)
            db.execute("INSERT INTO address VALUES (?, ?)", (contact[1], hashed_contactid))
            db.execute("INSERT INTO email VALUES (?, ?)", (contact[2], hashed_contactid))
            db.execute("INSERT INTO identification VALUES (?, ?)", (contact[3], hashed_contactid))


def read_database(database_path: Path):
    """
    read a database and produce the rows
    :param database_path: path to the database file
    """
    with database.Database(database_path) as db:
        for contact in db.execute("""
            SELECT c.rowid
            FROM contact c
        """):
            contactid = contact['rowid']
            hashed_contactid = hasher.make_id_hash(contactid)
            for row in db.execute("""
                SELECT c.name, a.address, e.email, i.identification
                FROM contact c, address a, email e, identification i
                WHERE c.rowid = ?
                AND a.contactid = ?
                AND e.contactid = ?
                AND i.contactid = ?
            """, (contactid, hashed_contactid, hashed_contactid, hashed_contactid)):
                yield row


def main():
    p: Path = util.make_database_path(__file__)
    if not p.is_file():
        create_database(p)
        fill_database(p)
    output.database_rows(read_database(p))


if __name__ == "__main__":
    main()
