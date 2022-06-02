from abc import abstractmethod
from typing import Dict

from tw_hooks.base_hooks.base_hook import BaseHook


class OnExitHook(BaseHook):
    """On exit hook base class."""

    @abstractmethod
    def on_exit(self, added_modified_tasks: Dict[str, str]):
        pass

    @classmethod
    def entrypoint(cls) -> str:
        """Name of the method that is meant to be the entrypoint for this hook."""
        return "on_exit"


    @classmethod
    def require_stdin(cls) -> bool:
        """True if this Hook requires access to the standard input."""
        return True

    @classmethod
    def shim_prefix(cls) -> str:
        return "on-exit"
