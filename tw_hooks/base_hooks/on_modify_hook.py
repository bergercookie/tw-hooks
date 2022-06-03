from abc import abstractmethod
from typing import Dict, List, final

from tw_hooks.base_hooks.base_hook import BaseHook
from tw_hooks.utils import stdin_lines_to_json


class OnModifyHook(BaseHook):
    """On modify hook base class."""

    @final
    def on_modify(self, stdin_lines: List[str]):
        """Entrypoint - to be called by the Hook shim."""
        o, m = stdin_lines_to_json(stdin_lines)
        return self._on_modify(original_task=o, modified_task=m)

    @abstractmethod
    def _on_modify(self, original_task: Dict[str, str], modified_task: Dict[str, str]):
        """Implement this in your hook."""

    @classmethod
    def entrypoint(cls) -> str:
        return "on_modify"

    @classmethod
    def require_stdin(cls) -> bool:
        return True

    @classmethod
    def shim_prefix(cls) -> str:
        return "on-modify"
