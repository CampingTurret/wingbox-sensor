import datetime


def format_data(line: str) -> str:
    """
    Formats the line variable.

    Parameters
    ----------
    line: str
        The line variable to format.

    Returns
    -------
    str
        Formatted line string.

    """

    timestamp = datetime.datetime.now()
    milliseconds = int(float(timestamp.strftime("%f")) / 1000)
    ms_str = str(milliseconds).zfill(3)
    split_line = line.split(' ')
    load_cell, time_of_flight = split_line[1], split_line[3]
    log_data = f'[{timestamp.strftime("%H:%M:%S")}.{ms_str}]: {load_cell},{time_of_flight}\n'

    return log_data
