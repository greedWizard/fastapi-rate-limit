from dataclasses import dataclass


@dataclass(frozen=True)
class BadDataException(Exception):
    errors: dict[str, list[str]]
