#!/usr/bin/env python3
"""Detect Taskwarrior hooks and register an executable shim for each one of them."""
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from importlib import import_module
from pathlib import Path
from typing import Dict, Sequence, Set, Type

from bubop.classes import all_subclasses
from bubop.fs import valid_path
from bubop.logging import logger
from bubop.string import format_dict, format_list

from tw_hooks.base_hooks import BaseHook, OnAddHook, OnExitHook, OnLaunchHook, OnModifyHook
from tw_hooks.hooks import import_concrete_hooks

# By default this will find all the implementations in this package. If the user wants to
# include their own hook classes, they'll have to specify the module paths in the
# TW_ADDITIONAL_HOOKS environment variable


HOOK_TEMPLATE = """
#!/usr/bin/env python3

import sys
from pathlib import Path
# Make this robust in case e.g., the user is running inside a virtualenv and tw_hooks is not
# installed in there.
try:
    from {import_from} import {class_name}
except ModuleNotFoundError:
    print("Can't import {class_name} hook")

    # We have to return some JSON that's compatible with the hooks API
    # https://taskwarrior.org/docs/hooks/
    name = Path(__file__).name
    hook_type = "-".join(name.split("-")[:2])

    stdin = sys.stdin.read().strip()

    if hook_type == "on-add":
        added_task = stdin
        print(added_task)
    elif hook_type == "on-modify":
        modified_task = stdin.splitlines()[-1]
        print(modified_task)
    else:
        pass

    sys.exit(0)

obj = {class_name}()
{invoke_instructions}
"""

INVOKE_WITH_STDIN_TEMPLATE = """
from tw_hooks.utils import parse_stdin_lines
sys.exit(obj.{class_entrypoint}(parse_stdin_lines()))
"""

INVOKE_WITH_NO_ARGS_TEMPLATE = """
sys.exit(obj.{class_entrypoint}())
"""


def _build_shim(base_hook: Type[BaseHook], hook: Type[BaseHook]) -> str:
    invoke_instructions = (
        INVOKE_WITH_STDIN_TEMPLATE
        if base_hook.require_stdin()
        else INVOKE_WITH_NO_ARGS_TEMPLATE
    )
    invoke_instructions = invoke_instructions.format(class_entrypoint=base_hook.entrypoint())
    return HOOK_TEMPLATE.format(
        import_from=hook.__module__,
        class_name=hook.name(),
        invoke_instructions=invoke_instructions,
    ).strip()


def main():
    """Main."""
    # parse CLI arguments ---------------------------------------------------------------------
    task_dir_default = Path.home() / ".task"

    parser = ArgumentParser(
        __doc__,
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-t",
        "--task-dir",
        type=valid_path,
        help="Path to the taskwarrior main directory",
        default=task_dir_default,
    )
    parser.add_argument(
        "-a",
        "--all-hooks",
        help="Install shims for all the hooks",
        action="store_true",
    )
    parser.add_argument(
        "-l",
        "--list-hooks",
        help="List the available hooks and exit",
        action="store_true",
    )
    parser.add_argument("-r", "--register-additional", nargs="+", default=[])

    executable = Path(sys.argv[0]).stem
    usecases = {
        "Install only the WarnOnTaskCongestion hook (assuming you've installed tw_hooks with e.g., pip3)": (
            "-r tw_hooks.hooks.warn_on_task_congestion"
        ),
        "Install all the available hooks from this repo (assuming you've installed tw_hooks with e.g., pip3)": (
            "--all-hooks"
        ),
        'Install a custom hook defined in .../dir/mod/hook_name.py. "dir" should be in your PYTHONPATH': (
            "-r mod.hook_name"
        ),
        "List all the available hooks and exit": "--list-hooks",
    }
    parser.epilog = f'Usage examples:\n{"=" * 15}\n\n' + "\n".join(
        (f"- {k}\n  {executable} {v}\n" for k, v in usecases.items())
    )

    args = vars(parser.parse_args())
    additional_hook_modules: Sequence[str] = args["register_additional"]
    install_all_hooks: bool = args["all_hooks"]
    list_hooks: bool = args["list_hooks"]
    hooks_dir: Path = args["task_dir"] / "hooks"

    if (not install_all_hooks and not additional_hook_modules) and not list_hooks:
        raise RuntimeError(
            'You have to specify at least one of the "--all-hooks", "--register-additional"'
            " options otherwise no hooks are going to be installed.\n"
            "Alternatively use --list-hooks to see the hooks that can be installed"
        )

    if list_hooks:
        install_all_hooks = True

    # print CLI configuration -----------------------------------------------------------------
    print(
        format_dict(
            header="CLI Configuration",
            items={
                "Hooks directory": (hooks_dir),
                "Install all available hooks": install_all_hooks,
                "List hooks and exit": list_hooks,
                "Register hooks from modules": additional_hook_modules,
            },
            align_items=True,
        )
    )

    if install_all_hooks:
        logger.info("Installing all available hooks...")
        import_concrete_hooks()

    # iterate over additional_hook_modules, try to find a (partial) match on ------------------
    # any importable module and import it
    for ad_hook in additional_hook_modules:
        try:
            import_module(ad_hook)
        except ModuleNotFoundError:
            logger.error(
                f"Couldn't find module {ad_hook} in your path. Make sure this module is"
                " accessible, e.g., by adding its location in $PYTHONPATH"
            )

    # initialize hooks directory --------------------------------------------------------------
    if hooks_dir.exists():
        if not hooks_dir.is_dir():
            raise RuntimeError(f"{hooks_dir} exists and is not a directory, can't proceed.")

    else:
        logger.info("Hooks directory not present, creating it...")
        hooks_dir.mkdir(parents=True, exist_ok=False)

    # fetch all the hook implemenattions and group them per base hook -------------------------
    hook_bases: Sequence[Type[BaseHook]] = [OnExitHook, OnLaunchHook, OnAddHook, OnModifyHook]
    hooks_to_install: Dict[Type[BaseHook], Set[Type[BaseHook]]] = {}

    # gather all the hooks --------------------------------------------------------------------
    hook_with_descriptions: Dict[str, Sequence[str]] = {}  # only for reporting to the user...
    for SomeBaseHook in hook_bases:
        subclasses: Set[Type[BaseHook]] = all_subclasses(SomeBaseHook)  # type: ignore # TODO?
        hooks_to_install[SomeBaseHook] = subclasses
        hook_with_descriptions[SomeBaseHook.name()] = [
            f"{Subclass.name()}: {Subclass.description()}" for Subclass in subclasses
        ]

    # report all the hook implementations found -----------------------------------------------
    logger.info("Available hooks")
    for hook_name, descriptions in hook_with_descriptions.items():
        print(format_list(descriptions, header=hook_name, indent=2))
    if list_hooks:
        logger.info("Skipping installation of hooks...")
        return

    # make sure there are shims to install otherwise exit
    for _, subclasses in hooks_to_install.items():
        if subclasses:
            break
    else:
        logger.warning("No shims to install.")
        return

    # install a shim under the hooks directory for each hook implementation -------------------
    logger.info(f"Installing shim executables under {hooks_dir}")
    for SomeBaseHook, subclasses in hooks_to_install.items():
        for SomeHook in subclasses:
            logger.debug(f"Creating shim for {SomeHook.name()}.{SomeBaseHook.entrypoint()}")
            shim_contents = _build_shim(SomeBaseHook, SomeHook)
            shim_path = hooks_dir / f"{SomeBaseHook.shim_prefix()}-{SomeHook.dashed_name()}.py"
            shim_path.write_text(shim_contents)
            shim_path.chmod(mode=0o764)

    return


if __name__ == "__main__":
    main()
