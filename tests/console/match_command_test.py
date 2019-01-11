import io
import os

from cleo import Application
from cleo import CommandTester
import pytest

from pyrex.console.match_command import MatchCommand


def cleo_tester(command_class, command_name):
    app = Application()
    app.add(command_class())
    cmd = app.find(command_name)
    tester = CommandTester(cmd)
    return tester


class TestMatch(object):
    def setup(self):
        self.tester = cleo_tester(MatchCommand, "match")
        print(self.tester)

    def test_source_is_a_string(self):
        self.tester.execute(""" '\\w+' 'asdf qwer' --separator ',' """)
        assert self.tester.io.fetch_output() == "asdf,qwer" + os.linesep
        assert self.tester.status_code == 0

    def test_source_is_stdin(self, monkeypatch):
        monkeypatch.setattr("sys.stdin", io.StringIO("asdf qwer"))
        self.tester.execute(""" '\\w+' --separator ',' """)
        assert self.tester.io.fetch_output() == "asdf,qwer" + os.linesep
        assert self.tester.status_code == 0

    def test_source_is_file(self, tmp_path):
        tmp = tmp_path / "test.txt"
        tmp.write_text("asdf qwer")
        self.tester.execute(f""" '\\w+' {tmp} --separator=',' """)
        assert self.tester.io.fetch_output() == "asdf,qwer" + os.linesep
        assert self.tester.status_code == 0

    @pytest.mark.parametrize(
        "sep,expected",
        [
            (",", "98,23" + os.linesep),
            (" ", "98 23" + os.linesep),
            ("-", "98-23" + os.linesep),
            ("/", "98/23" + os.linesep),
            # XXX Not currently working. Need to check
            # ("\\", r"98\\23" + os.linesep),
            ("\n", "98\n23" + os.linesep),
            ("\t", "98\t23" + os.linesep),
        ],
    )
    def test_use_different_separators(self, sep, expected):
        self.tester.execute(f""" '\\d+' 'asdf 98 qwer 23' --separator='{sep}' """)
        print(self.tester.io.fetch_output())
        assert self.tester.io.fetch_output() == expected
        assert self.tester.status_code == 0
