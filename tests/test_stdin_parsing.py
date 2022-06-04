from pathlib import Path
from unittest.mock import patch

import pytest

import tw_hooks.utils


@pytest.mark.parametrize(
    "stdlines",
    [f"stdlines{i}" for i in range(2)],
    indirect=True,
)
def test_stdin_to_json(stdlines):
    tasks = tw_hooks.utils.stdin_lines_to_json(stdlines)
    assert len(tasks) == 2
    for i in range(2):
        assert isinstance(tasks[i], dict)
        assert set({"description", "due", "entry"}).issubset(tasks[i].keys())


TEST_DATA = Path(__file__).absolute().parent / "test_data"


def test_parse_stdin_lines():
    """Make sure we can parse stdin lines that contain non-unicode characters."""
    f = open(TEST_DATA / "invalid_unicode_chars.txt", "r")
    with patch("tw_hooks.utils.sys.stdin.fileno", lambda: f.fileno()):
        tasks = tw_hooks.utils.parse_stdin_lines()
        assert len(tasks) == 2
        assert "Fasting" in tasks[0]
