"""Utility methods and fucntions.

If something is generic enough, make a PR to <https://github.com/bergercookie/bubop>
"""
import json
import os
from json.decoder import JSONDecodeError
from typing import List, Union, cast

from tw_hooks.types import ListOfTagsList, MapOfTags, TaskT


def _use_json(json_str: str):
    if json_str == "":
        return {}
    else:
        try:
            out = json.loads(json_str)
        except JSONDecodeError:
            out = json.loads(json_str.replace("'", '"'))

        return out


def stdin_lines_to_json(stdin_lines: List[str]) -> List[TaskT]:
    """
    Parse all  the lines from stdin and return them as a list of strings, each one
    corresponding to a single task.
    """
    out: List[TaskT] = []
    for line in stdin_lines:
        out.append(_use_json(line.strip()))

    return out


_JsonRetValue = Union[MapOfTags, ListOfTagsList]


def get_json_from_environ(envvar: str) -> _JsonRetValue:
    """Parse an environment variable assuming it contains JSON."""
    val = os.environ.get(envvar)
    if val is None:
        return {}
    else:
        val = json.loads(val.replace("'", '"'))
        return cast(_JsonRetValue, val)
