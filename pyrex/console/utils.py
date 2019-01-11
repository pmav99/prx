import pathlib
import sys


def read_source(source):
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
