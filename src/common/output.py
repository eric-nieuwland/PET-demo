"""
output - output table rows
"""


def _collect_database_rows(rows):
    """
    collect rows into a table with a header
    :param rows: source for database rows - a row is a dict
    :return: table - a list of lists
    """
    table = []
    for row in rows:
        if len(table) == 0:  # no header in table yet
            table.append([col for col in row.keys()])
        table.append([row[col] for col in row.keys()])
    return table


def _compute_column_widths(table):
    """
    compute the width of each column in a table
    :param table: a list of lists
    :return: list of widths
    """
    widths = [0] * len(table[0])
    for row in table:
        for idx, col in enumerate(row):
            widths[idx] = max(widths[idx], len(str(col)))
    return widths


def _make_row_format(widths, sample_row):
    """
    create a format string for the widths
    :param widths: sequence of numbers
    :param sample_row: a sample of data
    :return: format string
    """
    parts = [""]
    for idx, width in enumerate(widths):
        if isinstance(sample_row[idx], str):
            conversion = ""
            align = ""
            kind = "s"
        elif isinstance(sample_row[idx], int):
            conversion = ""
            align = ""
            kind = "d"
        else:
            conversion = "!r"
            align = "^"
            kind = "s"
        parts.append(f" {{{idx}{conversion}:{align}{width}{kind}}} ")
    parts.append("")
    return "|".join(parts)


def _make_separator(header_format):
    """
    create a separator string
    :param header_format: header format used as a template
    :return:
    """
    ncols = header_format.count("|") - 1
    empty_row = [""]*ncols
    return header_format.format(*empty_row).replace(" ", "-").replace("|", "+")


def database_rows(rows):
    """
    print rows from a database
    :param rows: source for database rows
    """
    table = _collect_database_rows(rows)
    nrows = len(table)-1  # table includes header
    if nrows < 1:
        print("no rows")
        return

    column_widths = _compute_column_widths(table)
    header_format = _make_row_format(column_widths, table[0])
    row_format = _make_row_format(column_widths, table[1])
    separator = _make_separator(header_format)

    for rownr, row in enumerate(table):
        if rownr == 0:  # header
            print(separator)
            print(header_format.format(*row))
            print(separator)
        else:
            print(row_format.format(*row))

    print(separator)
