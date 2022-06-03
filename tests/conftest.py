from typing import List
from pytest import fixture

from tw_hooks.types import SerTask


@fixture
def on_modify_changed_title(on_modify_changed_title_orig, on_modify_changed_title_mod) -> List[str]:
    return [on_modify_changed_title_orig, on_modify_changed_title_mod]


@fixture
def on_modify_changed_title_orig(on_modify_changed_title_orig_dict) -> str:
    return f"{on_modify_changed_title_orig_dict}\n"


@fixture
def on_modify_changed_title_mod(on_modify_changed_title_mod_dict) -> str:
    return f"{on_modify_changed_title_mod_dict}\n"


@fixture
def on_modify_changed_title_orig_dict() -> SerTask:
    return {
        "description": "kalimera kalimera kalimera",
        "entry": "20220602T212503Z",
        "modified": "20220602T212709Z",
        "status": "pending",
        "uuid": "c236dff8-76bb-4a8c-a075-0657c633c018",
        "tags": ["movie"],
    }


@fixture
def on_modify_changed_title_mod_dict() -> SerTask:
    return {
        "description": "kalimera kalimera kalimera kalimera",
        "entry": "20220602T212503Z",
        "modified": "20220602T212709Z",
        "status": "pending",
        "uuid": "c236dff8-76bb-4a8c-a075-0657c633c018",
        "tags": ["movie", "wor"],
    }
