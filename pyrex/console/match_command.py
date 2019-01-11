import pathlib
import re
import sys

from pprint import pprint as pp

import munch
from schema import Schema, And, Or, Optional, Use

from .command import Command


_MATCH_HELP = """\
The <info>match</> command returns matches of the <c1><regex></> pattern found in
<c1><source></>. The <c1><source></> can be either a string, or a path to a file. If
<c1><source></> is not specified, the new a command tries to read from <u>STDIN</>.
The found matches are printed to <u>STDOUT</> separated by the <c1>(--separator)</>.
"""


def resolve_source(source):
    """ Resolve the `source` and return the input as string.  """
    if source is None:
        text = sys.stdin.read()
    else:
        path = pathlib.Path(source)
        if path.exists():
            text = path.read_text()
        else:
            text = source
    return text


class MatchCommand(Command):
    """
    Find matches of pattern in source

    match
        {regex : The regex pattern which we want to match}
        {source? : The source of the text on which we want to find matches}
        {--nth=0 : Return the Nth match. If <c1>nth</> < 1, we return all matches}
        {--s|separator=, : The separator to use for the matches. Defaults to a single string ' '}

    """

    schema = Schema(
        {
            "regex": And(str, len),
            Optional("source"): Or(None, str),
            Optional("nth"): And(Use(int), lambda n: 0 <= n),
            Optional("separator"): And(str, Use(str.lower)),
        }
    )

    help = " ".join(_MATCH_HELP.splitlines()).strip()

    def parse_parameters(self, validate=True):
        params = {
            **{key: self.option(key) for key in self._config.options},
            **{key: self.argument(key) for key in self._config.arguments},
        }
        if isinstance(self.schema, Schema) and validate:
            params = self.schema.validate(params)
        return munch.munchify(params)

    def handle(self):
        # We can't set the default value of the separator on the signature until
        # https://github.com/sdispater/cleo/issues/64 is resolved
        params = self.parse_parameters()
        text = resolve_source(params.source)
        matches = re.findall(params.regex, text)
        if params.nth:
            self.line(matches[params.nth - 1])
        self.line(params.separator.join(matches))
