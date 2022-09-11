#!/usr/bin/env python3

import os
import sys
import traceback
from pathlib import Path

from bubop import loguru_set_verbosity

name = Path(__file__).name


def handle_errors() -> None:
    """Print the right strings even in the case where the hooks module is not found.

    This is so  that we abide to the TW Hooks output specifications.
    """
    stdin = sys.stdin.read().strip()

    hook_type = "-".join(name.split("-")[:2])

    if hook_type == "on-add":
        added_task = stdin
        print(added_task)
    elif hook_type == "on-modify":
        modified_task = stdin.splitlines()[-1]
        print(modified_task)
    else:
        pass


try:
    from tw_hooks.hook_shim import run
except ModuleNotFoundError:
    print(
        "Can't import tw_hooks.hook_shim. Make sure that the tw_hooks module is correctly"
        " installed and available in your PYTHONPATH"
    )

    handle_errors()

else:
    try:
        if "TW_HOOKS_VERBOSE" in os.environ:
            print("[hook_delegate.py:45] DEBUGGING STRING ==> ", 1)
            loguru_set_verbosity(2)
        else:
            loguru_set_verbosity(0)
        sys.exit(run(name))
    except Exception as e:
        print(traceback.format_exc())
