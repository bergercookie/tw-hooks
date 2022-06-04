from typing import Any, List

import pytest
from pytest import fixture

from tw_hooks.types import TaskT


@fixture
def on_modify_changed_title(
    on_modify_changed_title_orig, on_modify_changed_title_mod
) -> List[str]:
    return [on_modify_changed_title_orig, on_modify_changed_title_mod]


@fixture
def on_modify_changed_title_orig(on_modify_changed_title_orig_dict) -> str:
    return f"{on_modify_changed_title_orig_dict}\n"


@fixture
def on_modify_changed_title_mod(on_modify_changed_title_mod_dict) -> str:
    return f"{on_modify_changed_title_mod_dict}\n"


@fixture
def on_modify_changed_title_orig_dict() -> TaskT:
    return {
        "description": "kalimera kalimera kalimera",
        "entry": "20220602T212503Z",
        "modified": "20220602T212709Z",
        "status": "pending",
        "uuid": "c236dff8-76bb-4a8c-a075-0657c633c018",
        "tags": ["movie"],
    }


@fixture
def on_modify_changed_title_mod_dict() -> TaskT:
    return {
        "description": "kalimera kalimera kalimera kalimera",
        "entry": "20220602T212503Z",
        "modified": "20220602T212709Z",
        "status": "pending",
        "uuid": "c236dff8-76bb-4a8c-a075-0657c633c018",
        "tags": ["movie", "wor"],
    }


@pytest.fixture()
def stdlines(request: pytest.FixtureRequest):
    """Fixture to parametrize on."""
    param = request.param  # type: ignore
    return request.getfixturevalue(param)  # type: ignore


@fixture
def stdlines0() -> List[Any]:
    return [
        '{"description":"Meditate","due":"20220528T155959Z","entry":"20220528T144107Z","mask":"XXXXX-WW","modified":"20220603T161607Z","recur":"1d","rtype":"periodic","status":"recurring","uuid":"0fbe94ed-0b8b-419b-ab49-d85acd6c8b8e","wait":"20220527T225959Z","tags":["remindme","routine"]}\n',
        '{"description":"Meditate","due":"20220528T155959Z","entry":"20220528T144107Z","mask":"XXXXXXWW","modified":"20220603T161607Z","recur":"1d","rtype":"periodic","status":"recurring","uuid":"0fbe94ed-0b8b-419b-ab49-d85acd6c8b8e","wait":"20220527T225959Z","tags":["remindme","routine"]}\n',
    ]


@fixture
def stdlines1() -> List[Any]:
    return [
        '{"description":"🍣'
        ' Food","due":"20220528T155959Z","entry":"20220528T144107Z","mask":"XXXXX-WW","modified":"20220603T161607Z","recur":"1d","rtype":"periodic","status":"recurring","uuid":"0fbe94ed-0b8b-419b-ab49-d85acd6c8b8e","wait":"20220527T225959Z","tags":["remindme","routine"]}\n',
        '{"description":"🍣🍣🍣 More'
        ' food","due":"20220528T155959Z","entry":"20220528T144107Z","mask":"XXXXXXWW","modified":"20220603T161607Z","recur":"1d","rtype":"periodic","status":"recurring","uuid":"0fbe94ed-0b8b-419b-ab49-d85acd6c8b8e","wait":"20220527T225959Z","tags":["remindme","routine"]}\n',
    ]
