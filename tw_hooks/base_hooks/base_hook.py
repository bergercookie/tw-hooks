from abc import ABC, abstractmethod
from typing import List


class BaseHook(ABC):
    """Base class for all the Taskwarrior hooks."""

    @classmethod
    @abstractmethod
    def shim_prefix(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def entrypoint(cls) -> str:
        """Name of the method that is meant to be the entrypoint for this hook."""
        pass

    @classmethod
    @abstractmethod
    def require_stdin(cls) -> bool:
        """True if this Hook requires access to the standard input."""
        pass

    @classmethod
    def get_subclass_name(cls):
        return cls.__name__

    @classmethod
    def description(cls) -> str:
        doc = cls.__doc__
        if not doc:
            doc = "No description"
        else:
            doc = doc.strip("\n ").split("\n")[0]

        return doc

    @classmethod
    def name(cls) -> str:
        return cls.get_subclass_name()

    @classmethod
    def dashed_name(cls) -> str:
        name = cls.name()
        new_chars: List[str] = []
        for char in name:
            if char.isupper():
                new_chars.append("-")
                new_chars.append(char.lower())
            else:
                new_chars.append(char)
        return "".join(new_chars).lstrip("-")

    def __str__(self) -> str:
        return self.name()

    def log(self, s: str):
        print(f"[{self.name()}] {s}")
