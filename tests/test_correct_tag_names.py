from typing import Any, Dict, List

from pytest import fixture

from tw_hooks.base_hooks.on_modify_hook import OnModifyHook
from tw_hooks.hooks.correct_tag_names import CorrectTagNames
from tw_hooks.utils import _use_json


@fixture
def hook0() -> OnModifyHook:
    tag_mappings = {"this": "that", "something": "else"}
    c = CorrectTagNames(tag_mappings=tag_mappings)
    return c


@fixture
def hook1() -> OnModifyHook:
    tag_mappings = {"movie": "movies"}
    c = CorrectTagNames(tag_mappings=tag_mappings)
    return c


@fixture
def hook2() -> OnModifyHook:
    tag_mappings = {"movie": "movies", "wor": "work"}
    c = CorrectTagNames(tag_mappings=tag_mappings)
    return c


def test_nop(
    on_modify_changed_title: List[str],
    on_modify_changed_title_mod_dict: Dict[str, Any],
    capsys,
    hook0: OnModifyHook,
):
    """If the tags are irrelevant then this hook should do nothing."""
    hook0.on_modify(on_modify_changed_title)
    captured = capsys.readouterr()
    assert _use_json(captured.out.strip()) == on_modify_changed_title_mod_dict
    assert captured.err == ""


def test_change_one_tag(
    on_modify_changed_title: List[str],
    on_modify_changed_title_mod_dict: Dict[str, Any],
    capsys,
    hook1: OnModifyHook,
):
    """If one tag was identified, change that, leave the rest unchanged."""
    hook1.on_modify(on_modify_changed_title)
    captured = capsys.readouterr()
    on_modify_changed_title_mod_dict["tags"] = ["movies", "wor"]
    assert _use_json(captured.out.strip()) == on_modify_changed_title_mod_dict
    assert captured.err == ""


def test_change_multiple_tag(
    on_modify_changed_title: List[str],
    on_modify_changed_title_mod_dict: Dict[str, Any],
    capsys,
    hook2: OnModifyHook,
):
    """
    If multiple tags were identified, make sure all were changed correctly to the right values.
    """
    hook2.on_modify(on_modify_changed_title)
    captured = capsys.readouterr()
    on_modify_changed_title_mod_dict["tags"] = ["movies", "work"]
    assert _use_json(captured.out.strip()) == on_modify_changed_title_mod_dict
    assert captured.err == ""
