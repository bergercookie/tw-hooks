from abc import abstractmethod
from typing import Dict

from tw_hooks.base_hooks.base_hook import BaseHook


class OnAddHook(BaseHook):
    """On add hook base class."""

    @abstractmethod
    def on_add(self, added_tasks: Dict[str, str]):
        pass

    @classmethod
    def shim_prefix(cls) -> str:
        return "on-add"
