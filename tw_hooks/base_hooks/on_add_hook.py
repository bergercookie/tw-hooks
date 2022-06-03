from abc import abstractmethod
from typing import Dict, List, final

from tw_hooks.base_hooks.base_hook import BaseHook
from tw_hooks.types import SerTask
from tw_hooks.utils import stdin_lines_to_json, use_json


class OnAddHook(BaseHook):
    """On add hook base class."""

    @final
    def on_add(self, stdin_lines: List[str]):
        return self._on_add(stdin_lines_to_json(stdin_lines)[0])

    @abstractmethod
    def _on_add(self, added_task: SerTask):
        pass

    @classmethod
    def entrypoint(cls) -> str:
        return "on_add"

    @classmethod
    def require_stdin(cls) -> bool:
        return True

    @classmethod
    def shim_prefix(cls) -> str:
        return "on-add"
