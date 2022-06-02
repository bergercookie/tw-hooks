from abc import abstractmethod

from tw_hooks.base_hooks.base_hook import BaseHook


class OnLaunchHook(BaseHook):
    """On launch hook base class."""

    @abstractmethod
    def on_launch(self):
        pass

    @classmethod
    def shim_prefix(cls) -> str:
        return "on-launch"
