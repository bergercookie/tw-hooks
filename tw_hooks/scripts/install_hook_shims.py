#!/usr/bin/env python3

from argparse import ArgumentParser
from typing import Dict, Sequence, Set, Type
from bubop.fs import valid_path
from bubop.logging import logger
from pathlib import Path
from bubop import valid_path
from bubop.string import format_list


from tw_hooks.base_hooks import BaseHook, OnExitHook, OnLaunchHook, OnAddHook, OnModifyHook
from tw_hooks.hooks import *

# By default this will find all the implementations in this package. If the user wants to
# include their own hook classes, they'll have to specify the module paths in the
# TW_ADDITIONAL_HOOKS environment variable


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)]
    )


# TODO Change the path to the module that holds the hook
HOOK_TEMPLATE = """#!/usr/bin/env python3

import sys
from tw_hooks.hooks import {class_name}

obj = {class_name}()
sys.exit(obj.{class_entrypoint}({args}))
"""


def build_shim(base_hook: Type[BaseHook], hook: Type[BaseHook]) -> str:
    return HOOK_TEMPLATE.format(
        class_name=hook.name(),
        class_entrypoint=base_hook.entrypoint(),
        args="sys.stdin.readline()" if base_hook.require_stdin() else "",
    )


def main():
    # parse CLI arguments ---------------------------------------------------------------------
    task_dir_default = Path.home() / ".task"

    parser = ArgumentParser("Install executable shims for all the registered hooks.")
    parser.add_argument(
        "-t",
        "--task-dir",
        type=valid_path,
        help="Path to the taskwarrior main directory",
        default=task_dir_default,
    )

    args = vars(parser.parse_args())

    # TODO Import additional modules specified by the suer

    # initialize hooks directory --------------------------------------------------------------
    hooks_dir: Path = args["task_dir"] / "hooks"
    if hooks_dir.exists():
        if not hooks_dir.is_dir():
            raise RuntimeError(f"{hooks_dir} exists and is not a directory, can't proceed.")

    else:
        logger.info("Hooks directory not present, creating it...")
        hooks_dir.mkdir(parents=True, exist_ok=False)

    # fetch all the hook implemenattions and group them per base hook -------------------------
    logger.info("Looking for Taskwarrior hooks...")

    hook_bases: Sequence[Type[BaseHook]] = [OnExitHook, OnLaunchHook, OnAddHook, OnModifyHook]
    hooks_dict: Dict[Type[BaseHook], Set[Type[BaseHook]]] = {}
    hook_with_descriptions: Dict[str, Sequence[str]] = {}  # only for reporting to the user...
    for SomeBaseHook in hook_bases:
        subclasses: Set[Type[BaseHook]] = all_subclasses(SomeBaseHook)
        hooks_dict[SomeBaseHook] = subclasses
        hook_with_descriptions[SomeBaseHook.name()] = [
            f"{Subclass.name()}: {Subclass.description()}" for Subclass in subclasses
        ]

    # report all the hook implementations found
    for hook_name, descriptions in hook_with_descriptions.items():
        print(format_list(descriptions, header=hook_name))

    # install a shim under the "~/.task/hooks" directory for each hook implementation ---------
    # found
    logger.info(f"Installing shim executables under {hooks_dir}")
    for SomeBaseHook, subclasses in hooks_dict.items():
        for SomeHook in subclasses:
            logger.debug(f"Creating shim for {SomeHook.name()}.{SomeBaseHook.entrypoint()}")
            shim_contents = build_shim(SomeBaseHook, SomeHook)
            shim_path = hooks_dir / f"{SomeBaseHook.shim_prefix()}-{SomeHook.dashed_name()}.py"
            shim_path.write_text(shim_contents)
            shim_path.chmod(mode=0o764)

if __name__ == "__main__":
    main()
