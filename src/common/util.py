"""
util - various common utilities
"""
import os


def make_database_path(path):
    """
    turn a file path into a database path
    :param path: file path
    :return: database path
    """
    if not isinstance(path, str):
        raise TypeError(f"path should be str, not {path.__class__.__name__}")
    if path == "":
        raise ValueError("path should be a non-empty string")

    path = os.path.abspath(path)  # make sure we have the whole thing
    directory, file_name = os.path.split(path)
    parent_directory = os.path.dirname(directory)

    database_directory = os.path.join(parent_directory, "database")
    if not os.path.exists(database_directory):
        os.mkdir(database_directory)
    elif not os.path.isdir(database_directory):
        raise NotADirectoryError(f"{database_directory}")

    file_base = os.path.splitext(file_name)[0]
    db_ext = ".db"
    database_path = os.path.join(database_directory, f"{file_base}{db_ext}")

    return database_path
