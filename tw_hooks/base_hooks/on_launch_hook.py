from abc import abstractmethod
from typing import final

from tw_hooks.base_hooks.base_hook import BaseHook


class OnLaunchHook(BaseHook):
    """On launch hook base class."""

    @final
    def on_launch(self):
        """Entrypoint - to be called by the Hook shim."""
        return self._on_launch()

    @abstractmethod
    def _on_launch(self):
        """Implement this in your hook."""

    @classmethod
    def entrypoint(cls) -> str:
        return "on_launch"

    @classmethod
    def require_stdin(cls) -> bool:
        return False

    @classmethod
    def shim_prefix(cls) -> str:
        return "on-launch"
