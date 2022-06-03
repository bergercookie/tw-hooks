import json
import os
from typing import List, Union

from tw_hooks.types import ListOfTagsList, MapOfTags, SerTask


def use_json(json_str: str):
    if json_str == "":
        return {}
    else:
        return json.loads(json_str)


def stdin_lines_to_json(stdin_lines: List[str]) -> List[SerTask]:
    out: List[SerTask] = []
    for line in stdin_lines:
        out.append(use_json(line.strip()))

    return out


def get_map_from_environ(envvar: str) -> Union[MapOfTags, ListOfTagsList]:
    val = os.environ.get(envvar)
    if val is None:
        return {}
    else:
        val = json.loads(val.replace("'", '"'))
        return val
