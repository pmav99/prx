import io

import pytest

from pyrex.console.utils import read_source


def test_read_source_from_path(tmp_path):
    tmp = tmp_path / "test.txt"
    tmp.write_text("asdf")
    assert read_source(tmp.as_posix()) == "asdf"


def test_read_source_from_stdin(monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO("asdf"))
    assert read_source() == "asdf"


def test_read_source_from_string():
    assert read_source("asdf") == "asdf"
