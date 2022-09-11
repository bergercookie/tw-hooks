#!/usr/bin/env python3

"""Delegate function to call all the hooks of a particular type."""

import importlib
import os
from enum import Enum, auto
from functools import cached_property
from types import ModuleType
from typing import List, Mapping, Sequence, Type

from bubop import logger

from tw_hooks.base_hooks import OnAddHook, OnExitHook, OnLaunchHook, OnModifyHook
from tw_hooks.base_hooks.base_hook import BaseHook
from tw_hooks.utils import parse_stdin_lines


class HookProps(Enum):
    Add = auto()
    Exit = auto()
    Launch = auto()
    Modify = auto()

    @cached_property
    def suffix(self) -> str:
        return _hook_prop_to_suffix[self]

    @cached_property
    def envvar(self) -> str:
        return _hook_prop_to_envvar[self]

    def hook_base_class(self) -> Type[BaseHook]:
        return _hook_prop_to_base_class[self]

    @staticmethod
    def from_suffix(suffix: str) -> "HookProps":
        if suffix not in _suffix_to_hook_prop:
            logger.error(
                f"Invalid suffix provided -> {suffix}. Suffix has to be one of the following:"
                f" {list(_suffix_to_hook_prop.keys())}"
            )

        return _suffix_to_hook_prop[suffix]

    @classmethod
    def from_hook_name(cls, hook_name: str) -> "HookProps":
        """
        Given a hook name, extract  the suffix and then infer the HookProps for that suffix.
        """

        parts = hook_name.split("-")
        if len(parts) < 2:
            logger.error(f"Can't detect hook type from name -> {hook_name}")

        suffix = "-".join(parts[:2])
        return cls.from_suffix(suffix)


_hook_prop_to_base_class: Mapping[HookProps, Type[BaseHook]] = {
    HookProps.Launch: OnLaunchHook,
    HookProps.Exit: OnExitHook,
    HookProps.Add: OnAddHook,
    HookProps.Modify: OnModifyHook,
}

_hook_prop_to_envvar: Mapping[HookProps, str] = {
    HookProps.Launch: "TW_ON_LAUNCH_PLUGINS",
    HookProps.Exit: "TW_ON_EXIT_PLUGINS",
    HookProps.Add: "TW_ON_ADD_PLUGINS",
    HookProps.Modify: "TW_ON_MODIFY_PLUGINS",
}

_hook_prop_to_suffix: Mapping[HookProps, str] = {
    HookProps.Launch: "on-launch",
    HookProps.Exit: "on-exit",
    HookProps.Add: "on-add",
    HookProps.Modify: "on-modify",
}

_suffix_to_hook_prop: Mapping[str, HookProps] = {
    item[1]: item[0] for item in _hook_prop_to_suffix.items()
}


def fetch_hooks_to_call(envvar: str) -> Sequence[str]:
    """Fetch all the hooks - in their string form - from the specified environment variable."""
    if envvar not in os.environ:
        logger.debug(f"Variable {envvar} is not set - Failed to fetch hooks...")
        return []

    all_hooks = os.environ[envvar].split()
    if not all_hooks:
        logger.info(
            f"Variable {envvar} is set but doesn't contain any hook modules. "
            "Remember this has to be a space-separated list, e.g., "
            '"tw_hooks.hooks.warn_on_task_congestion tw_hooks.hooks.correct_tag_name"'
        )

    return all_hooks


def hook_module_to_hook_name(mod_str: str) -> str:
    """
    Extract the hook name from the module path

    For example for module "a.b.hook_name" contains a hook named "HookName".

    >>> hook_module_to_hook_name("kalimera.kalinuxta.kalispera")
    'Kalispera'
    >>> hook_module_to_hook_name("kalimera.kalinuxta.kalispera_kalispera")
    'KalisperaKalispera'
    >>> hook_module_to_hook_name("kalimera.kalinuxta.kalispera_kalispera_kalispera")
    'KalisperaKalisperaKalispera'
    """

    hook_name = mod_str.rsplit(".")[-1]
    return "".join([p.capitalize() for p in hook_name.split("_")])


def handle_no_hooks_case(hp: HookProps, stdin_lines: List[str]) -> None:
    """Copied and repurposed from hook_delegate.py."""
    if hp == HookProps.Add:
        added_task = "\n".join(stdin_lines)
        print(added_task)
    elif hp == HookProps.Modify:
        modified_task = stdin_lines[-1]
        print(modified_task)
    else:
        pass


def run(hook_name: str):
    """Fetch, instantiate and call the hooks based on the hook name provided

    The given filename has to have a suffix that matches one of the Taskwarrior supported file
    suffixes (e.g., on-launch).
    """

    hp = HookProps.from_hook_name(hook_name)
    hook_strs = fetch_hooks_to_call(hp.envvar)

    # convert from strings to concrete hook instances
    hooks: List[BaseHook] = []
    for hook_path_str in hook_strs:
        # import hook module ------------------------------------------------------------------
        mod: ModuleType
        try:
            mod = importlib.import_module(hook_path_str)
        except ModuleNotFoundError:
            logger.error(f"Could not import hook {hook_path_str} - programmatic error?...")
            continue

        # import hook class -------------------------------------------------------------------
        hook_class: Type[BaseHook]
        # assumption: module "a.b.hook_name" contains a hoo named "HookName"
        hook_name = hook_module_to_hook_name(hook_path_str)

        try:
            hook_class = getattr(mod, hook_name)
        except AttributeError:
            logger.error(f"Couldn't find hook by the name of {hook_name} in {hook_path_str}")
            continue

        hooks.append(hook_class())

    base_class = hp.hook_base_class()
    stdin_lines = parse_stdin_lines()
    for hook in hooks:
        # call parent method on hook

        entrypoint_str = base_class.entrypoint()
        entrypoint = getattr(base_class, entrypoint_str)
        logger.debug(f"-------------- Calling {hook}.{entrypoint_str}...")
        if base_class.require_stdin():
            output = entrypoint(hook, stdin_lines=stdin_lines)
        else:
            output = entrypoint(hook)

        # chain the output of one with the input of the next if the current hook does produce
        # output (e.g., on-add)
        if base_class.produce_stdout():
            stdin_lines = output

    else:
        handle_no_hooks_case(hp, stdin_lines)
