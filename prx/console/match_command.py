import re

from schema import And, Optional, Or, Schema, Use

from .command import Command
from .utils import read_source

_MATCH_HELP = """\
The <info>match</> command returns matches of the <c1><regex></> pattern found in
<c1><source></>. The <c1><source></> can be either a string, or a path to a file. If
<c1><source></> is not specified, the new a command tries to read from <u>STDIN</>.
The found matches are printed to <u>STDOUT</> separated by the <c1>(--separator)</>.
"""


class MatchCommand(Command):

    # TODO make nth accept a multiple values (e.g. 1,2,3,7-10)
    # TODO figure out how to handle not finding matches
    # TODO add support for printing one per line

    """
    Find matches of pattern in source

    match
        {regex : The regex pattern which we want to match}
        {source? : The source of the text on which we want to find matches}
        {--nth=0 : Return the Nth match. If <c1>nth</> < 1, we return all matches}
        {--s|separator=, : The separator to use for the matches. Defaults to a single string ' '}
    """

    help = " ".join(_MATCH_HELP.splitlines()).strip()

    schema = Schema(
        {
            "regex": And(str, len),
            Optional("source"): Or(None, str),
            Optional("nth"): And(Use(int), lambda n: n >= 0),
            Optional("separator"): And(str, Use(str.lower)),
        }
    )

    def handle(self):
        # We can't set the default value of the separator on the signature until
        # https://github.com/sdispater/cleo/issues/64 is resolved
        params = self.parse_parameters()
        text = read_source(params.source)
        matches = re.findall(params.regex, text)
        if params.nth:
            self.line(matches[params.nth - 1])
        else:
            self.line(params.separator.join(matches))
