from abc import abstractmethod
from typing import Dict

from tw_hooks.base_hooks.base_hook import BaseHook


class OnModifyHook(BaseHook):
    """On modify hook base class."""

    @abstractmethod
    def on_modify(self, modified_tasks: Dict[str, str]):
        pass

    @classmethod
    def shim_prefix(cls) -> str:
        return "on-modify"
