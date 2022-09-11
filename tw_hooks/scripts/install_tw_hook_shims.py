#!/usr/bin/env python3
"""
Install 4 shims - one per Taskwarrior event (on-add, on-launch, on-modify, on-exit).

Delegate to hook_shim:run in all cases
"""


from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
from typing import Iterator, Tuple

import pkg_resources
from bubop import logger, loguru_set_verbosity, valid_path


def write_shim_to(path: Path):
    hook_delegate_path: Path = Path(
        pkg_resources.resource_filename("tw_hooks", "hook_delegate.py")
    )
    shim_contents = hook_delegate_path.read_bytes()
    path.write_bytes(shim_contents)
    path.chmod(mode=0o764)


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
        "-u",
        "--uninstall",
        help="Uninstall all tw-hooks previously installed via this executable",
        action="store_true",
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")

    args = vars(parser.parse_args())
    hooks_dir: Path = args["task_dir"] / "hooks"

    loguru_set_verbosity(args["verbose"])

    def hook_path_gen() -> Iterator[Tuple[str, Path]]:
        for event in ["add", "exit", "modify", "launch"]:
            shim_path = hooks_dir / f"on-{event}-tw-hooks-delegate.py"
            yield event, shim_path

    # uninstall all installed shims -----------------------------------------------------------
    if args["uninstall"]:
        logger.info("Uninstalling previously installed delegate hokos")
        for ev, hook_path in hook_path_gen():
            logger.debug(f"Removing shim for {ev} event")
            hook_path.unlink(missing_ok=True)

        return

    # install a shim under the hooks directory for each hook type -----------------------------
    logger.info(f"Installing shims under {hooks_dir}")
    for ev, hook_path in hook_path_gen():
        logger.debug(f"Creating shim for {ev} event -> {hook_path}")
        write_shim_to(hook_path)


if __name__ == "__main__":
    main()
