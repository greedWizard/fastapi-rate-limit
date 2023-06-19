from dataclasses import dataclass


@dataclass(frozen=True)
class BadDataException(Exception):
    errors: dict[str, list[str]]


@dataclass(frozen=True)
class SecurityException(Exception):
    errors: dict[str, list[str]]
