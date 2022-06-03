from abc import abstractmethod
from typing import List, final

from tw_hooks.base_hooks.base_hook import BaseHook
from tw_hooks.types import SerTask
from tw_hooks.utils import stdin_lines_to_json, use_json


class OnExitHook(BaseHook):
    """On exit hook base class."""

    @final
    def on_exit(self, stdin_lines: List[str]):
        items = stdin_lines_to_json(stdin_lines)
        return self._on_exit(items)

    @abstractmethod
    def _on_exit(self, added_modified_tasks: List[SerTask]):
        pass

    @classmethod
    def entrypoint(cls) -> str:
        return "on_exit"

    @classmethod
    def require_stdin(cls) -> bool:
        return True

    @classmethod
    def shim_prefix(cls) -> str:
        return "on-exit"
