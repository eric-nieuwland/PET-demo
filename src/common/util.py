"""
util - various common utilities
"""
from pathlib import Path


def make_database_path(path: str | Path) -> Path:
    """
    turn a file path into a database path
    :param path: file path
    :return: database path
    """
    if not isinstance(path, str):
        raise TypeError(f"path should be str, not {path.__class__.__name__}")
    if path == "":
        raise ValueError("path should be a non-empty string")

    path = Path(path).resolve()  # make sure we have the whole thing
    project_directory = path.parent.parent

    database_directory = project_directory / "database"
    if not database_directory.exists():
        database_directory.mkdir(parents=True, exist_ok=True)
    elif not database_directory.is_dir():
        raise NotADirectoryError(f"{database_directory}")

    db_ext = ".db"
    database_path = database_directory / f"{path.stem}{db_ext}"

    return database_path
