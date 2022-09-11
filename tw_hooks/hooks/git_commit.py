import os
import subprocess
from pathlib import Path
from typing import List

from bubop import logger

from tw_hooks.base_hooks.on_exit_hook import OnExitHook
from tw_hooks.types import TaskT

Command = List[str]


class GitCommit(OnExitHook):
    """
    On addition/modification of any task, cd into the task location (by default ~/.task` and
    issue a git add && git-commit && git push. Do this asynchronously and don't block the
    current task execution
    """

    def __init__(self):
        self._curdir = Path(".").absolute()
        self._taskdir = (
            Path(os.environ.get("TASKDATA", Path.home() / ".task")).resolve().absolute()
        )

    def _do_commit(self, msg: str):
        msg = msg.replace('"', '\\"')
        msg = f'"{msg}"'
        cmd = [f"git add -A && git commit -m {msg}"]
        self._run_cmd(cmd)

    def _run_cmd(self, cmd: Command) -> subprocess.Popen:
        try:
            os.chdir(self._taskdir)
            logger.debug(f'Recording changes in git using {" ".join(cmd)}\ncmd: {cmd}')
            p = subprocess.Popen(
                cmd,
                shell=True,
                start_new_session=True,
            )
        finally:
            os.chdir(self._curdir)
        return p

    def _on_exit(self, added_modified_tasks: List[TaskT]):
        len_ = len(added_modified_tasks)
        if len_:
            self._do_commit(msg=f"Add/modify {len_} tasks")
        else:
            logger.debug("No added/modified tasks.")
