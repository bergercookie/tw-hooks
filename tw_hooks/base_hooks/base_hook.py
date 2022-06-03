from abc import ABC, abstractmethod

from bubop.string import camel_case_to_dashed


class BaseHook(ABC):
    """Base class for all the Taskwarrior hooks."""

    @classmethod
    @abstractmethod
    def shim_prefix(cls) -> str:
        """Return the prefix that is to be used when creating shims for this type of hooks.

        Implement in the direct children only.
        """

    @classmethod
    @abstractmethod
    def entrypoint(cls) -> str:
        """Name of the method that is meant to be the entrypoint for this hook."""

    @classmethod
    @abstractmethod
    def require_stdin(cls) -> bool:
        """True if this Hook requires access to the standard input."""

    @classmethod
    def _get_subclass_name(cls) -> str:
        return cls.__name__

    @classmethod
    def description(cls) -> str:
        """Get a description of this class based on the first line of its docstring."""
        doc = cls.__doc__
        if not doc:
            doc = "No description"
        else:
            doc = doc.strip("\n ").split("\n")[0]

        return doc

    @classmethod
    def name(cls) -> str:
        """Return the name of the child class."""
        return cls._get_subclass_name()

    @classmethod
    def dashed_name(cls) -> str:
        """Return the name of the child class in dashed format - instead of camel-case."""
        name = cls.name()
        return camel_case_to_dashed(name)

    def __str__(self) -> str:
        """Return in string form."""
        return self.name()

    def log(self, s: str):
        """Helper method for the child classes to log and prefix it with their name."""
        print(f"[{self.name()}] {s}")
