"""
database - stuff for handling a database
"""
from pathlib import Path
import sqlite3


class DatabaseError(RuntimeError):
    pass


class Database(object):
    """
    wrapper class around sqlite3 to allow neat Python code
    """

    database_path = None
    connection = None

    def __init__(self, database_path: Path | str, must_exist: bool = True):
        """
        define a sqlite3 database
        :param database_path: path to the database file
        :param must_exist: whether the database must already exist
        """
        database_path = Path(database_path)
        if must_exist and not database_path.is_file():
            raise DatabaseError(f"database {database_path!r} does not exist")
        
        super().__init__()
        self.database_path = database_path

    def connect(self):
        """
        connect to the database
        """
        if self.connection is not None:
            raise DatabaseError(f"already connected to {self.database_path!r}")

        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row

    def cursor(self):
        """
        create a cursor on the database
        :return: database cursor
        """
        if self.connection is None:
            raise DatabaseError(f"not connected to {self.database_path!r}")

        return self.connection.cursor()

    def execute(self, command, *args, **kwargs):
        """
        execute a command on the database
        :param command: command text
        :param args: arguments to the command
        :param kwargs: keyword arguments to the command
        :return: command result
        """
        if self.connection is None:
            raise DatabaseError(f"not connected to {self.database_path!r}")

        return self.connection.execute(command, *args, **kwargs)

    def executemany(self, command, args):
        """
        execute a command on the database
        :param command: command text
        :param args: arguments to the command
        :return: command result
        """
        if self.connection is None:
            raise DatabaseError(f"not connected to {self.database_path!r}")

        return self.connection.executemany(command, args)

    def executescript(self, script):
        """
        execute a command on the database
        :param script: command text
        :return: command result
        """
        if self.connection is None:
            raise DatabaseError(f"not connected to {self.database_path!r}")

        return self.connection.executescript(script)

    def disconnect(self, success: bool = True):
        """
        disconnect from the database
        :param success: whether processing was successful and should be persisted
        :return:
        """
        if self.connection is None:
            raise DatabaseError(f"not connected to {self.database_path!r}")

        if success:
            self.connection.commit()
        else:
            self.connection.rollback()

        self.connection.close()
        self.connection = None

    # --- context manager interface ---

    def __enter__(self):
        """
        create a database context
        :return: a database context - this object
        """
        self.connect()

        # will handle the database context ourselves
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        terminate a database context - the arguments tell whether the termination is regular or by exception
        :param exc_type: exception type or None
        :param exc_val: exception value or None
        :param exc_tb: exception traceback or None
        :return: whether the exception (if any) was handled
        """
        success = exc_type is None
        self.disconnect(success)

        # database context terminated, but exception not handled
        return False
