import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Union

from tw_hooks.base_hooks.on_exit_hook import OnExitHook


class WarnOnTaskCongestion(OnExitHook):
    """
    Warn the user if there are too many tasks.

    By default this class will warn if there are multiple tasks that are due:today.

    In the future the date field (due, scheduled) that will be used for this should be
    configurable.
    """

    def __init__(
        self,
        task_dir: Union[str, Path] = Path.home() / ".task",
        date_field="due",
        warn_threshold=20,
    ):
        self._task_dir = Path(task_dir)
        self._pending_data = self._task_dir / "pending.data"

        self._date_field = date_field
        self._date = "today"
        self._re_pat = rf"({self._date_field}:\"\d+).*" + "]"
        self._warn_threshold = warn_threshold

    def _on_exit(self, _):
        # I can't just invoke the taskwarrior executable. There's some sort of lock being
        # acquired so a potential subprocess.run call is blocking forever.
        # I have to manually parse pending.data
        if not self._pending_data.is_file():
            self.log(f"Can't find pending.data file -> {self._pending_data}")
            return 1

        # compute range of timestamps which corresponds to "today"
        today = datetime.today()
        today = datetime(year=today.year, month=today.month, day=today.day)
        today_start = int(today.timestamp())
        tomorrow_start = int((today + timedelta(days=1)).timestamp())

        conts = self._pending_data.read_text(errors="ignore")
        filter_ = f"{self._date_field}:{self._date}"
        re_iter = re.finditer(pattern=self._re_pat, string=conts)

        # count all the tasks whose selected date is today. If that surpasses our threshold
        # break and issue warning
        count = 0
        for g in re_iter:
            g_ = g.group(1)
            ts = int(g_.split('"')[-1])
            if today_start <= ts < tomorrow_start:
                count += 1
                if count > self._warn_threshold:
                    self.log(
                        f"Too many {filter_} tasks (threshold={self._warn_threshold})."
                        " Consider reducing them to avoid noise in your reports"
                    )
                    break
        return 0
