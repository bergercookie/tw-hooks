import json
import os
import subprocess

from tw_hooks import OnModifyHook
from tw_hooks.types import Retcode, TaskT

envvar = "TW_I3STATUS_RS_DBUS_NAME"


class PostLatestSTartToI3Status(OnModifyHook):
    """When a task is started, send the title of the task to i3status-rs via DBus.

    This is in order to update a custom DBus block in the toolbar.

    To specify the name with which to communicate with i3status-rs over DBus, set the following
    environment variable in your shell RC file:

        TW_I3STATUS_RS_DBUS_NAME=ActiveTaskwarriorTask
    """

    def __init__(self, dbus_name=os.environ.get(envvar)):
        self._dbus_name: str = dbus_name if dbus_name else ""

    def _detect_start_of_task(self, task: TaskT) -> bool:
        """Return True if task is marked as started, false otherwise

        I don't care whether the task was alredy started or not.
        """
        return "start" in task.keys()

    def _post_to_dbus(self, task) -> Retcode:
        task_desc = f'{task["uuid"][:8]} | {task["description"]}'
        if "annotations" in task:
            annotations = " | ".join(
                annotation_dict["description"][:50] for annotation_dict in task["annotations"]
            )
            task_desc += f" | {annotations}"

        # upper limit on the length of the string I'll be sending
        task_desc = task_desc[:200]

        proc = subprocess.run(
            [
                "busctl",
                "--user",
                "call",
                "i3.status.rs",
                "/ActiveTaskwarriorTask",
                "i3.status.rs",
                "SetStatus",
                "sss",
                task_desc,
                "tasks",
                "Good",
            ],
            check=False,
        )

        if proc.returncode != 0:
            # Don't fail this execution. Updating the i3status is not that important.
            if proc.stdout:
                out = proc.stdout.decode("utf-8")
            else:
                out = ""
            if proc.stderr:
                err = proc.stderr.decode("utf-8")
            else:
                err = ""
            self.log(f"Failed to send started task.\n\nstdout: {out}\n\nstderr: {err}")

        return 0

    def _on_modify(self, original_task: TaskT, modified_task: TaskT):
        del original_task
        ret = 0
        if self._detect_start_of_task(modified_task):
            ret = self._post_to_dbus(modified_task)

        print(json.dumps(modified_task))
        return ret
