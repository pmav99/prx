import pathlib
import sys


def read_source(source=None):
    """ Read the data from `source` and return the input as string.  """
    if source is None:
        text = sys.stdin.read()
    else:
        path = pathlib.Path(source)
        if path.exists():
            text = path.read_text()
        else:
            text = source
    return text


VALID_NTHS = set("0123456789+-")


def convert_nth_element_to_slice(elem):
    # validate input
    if not set(elem).issubset(VALID_NTHS):
        raise ValueError("Couldn't parse: <%r>" % elem)
    elif "+" in elem:
        start, end = elem.split("+")
        if end != "" or not start.isdigit():
            raise ValueError("Couldn't parse: <%r>" % elem)
        elem = int(elem)
        sl = slice(elem - 1, None)
    elif "-" in elem:
        start, stop = elem.split("-")
        if not (start.isdigit() and end.isdigit()):
            raise ValueError("Couldn't parse: <%r>" % elem)
        sl = slice(int(start) - 1, int(stop) + 1)
    else:
        if not elem.isdigit():
            raise ValueError("Couldn't parse: <%r>" % elem)
        sl = slice(int(elem) - 1, elem)
    return sl


def parse_nths(string):
    """
    Return a list of integers

    Should be able to handle:

        1+
        40+
        10-20
        1,2,3,40+
        1,2,3,10-20
        1,2,3,10-20,40+

    Note: It can't handle negative numbers!
    """
    numbers = []
    for part in (part.strip() for part in string.split(",")):
        if "+" in part:
            start, end = part.split("+")
            if end != "":
                raise ValueError("Couldn't parse: <%r>" % part)
            numbers.extend(list(range(int(start), MAX_QUARTER_ID + 1)))
        elif "-" in part:
            start, end = part.split("-")
            numbers.extend(list(range(int(start), int(end) + 1)))
        else:
            numbers.append(int(part))
    return numbers
