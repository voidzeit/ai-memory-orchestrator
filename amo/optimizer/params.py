from __future__ import annotations

from dataclasses import dataclass
from typing import Any


SUPPORTED_TYPES = {"int", "float", "bool", "categorical"}


@dataclass(frozen=True)
class ParameterDefinition:
    name: str
    type: str
    default: Any
    safe_to_apply: bool
    description: str
    low: int | float | None = None
    high: int | float | None = None
    choices: tuple[Any, ...] = ()

    @classmethod
    def from_dict(cls, name: str, data: object) -> "ParameterDefinition":
        if not isinstance(data, dict):
            raise ValueError(f"{name}: definition must be a mapping")
        missing = [key for key in ("type", "default", "safe_to_apply", "description") if key not in data]
        if missing:
            raise ValueError(f"{name}: missing required fields: {', '.join(missing)}")
        if not isinstance(data["safe_to_apply"], bool):
            raise ValueError(f"{name}: safe_to_apply must be true or false")
        kind = str(data["type"])
        if kind not in SUPPORTED_TYPES:
            raise ValueError(f"{name}: unsupported type '{kind}'")
        low = data.get("low")
        high = data.get("high")
        choices = tuple(data.get("choices", ()))
        if kind in {"int", "float"}:
            if low is None or high is None:
                raise ValueError(f"{name}: numeric parameters require low and high")
            if not isinstance(low, (int, float)) or isinstance(low, bool):
                raise ValueError(f"{name}: low must be numeric")
            if not isinstance(high, (int, float)) or isinstance(high, bool):
                raise ValueError(f"{name}: high must be numeric")
            if low > high:
                raise ValueError(f"{name}: low must be less than or equal to high")
            if not low <= data["default"] <= high:
                raise ValueError(f"{name}: default must be within bounds")
        elif kind == "categorical":
            if not choices:
                raise ValueError(f"{name}: categorical parameters require choices")
            if data["default"] not in choices:
                raise ValueError(f"{name}: default must be one of choices")
        elif not isinstance(data["default"], bool):
            raise ValueError(f"{name}: bool default must be true or false")
        return cls(
            name=name,
            type=kind,
            default=data["default"],
            safe_to_apply=bool(data["safe_to_apply"]),
            description=str(data["description"]),
            low=low,
            high=high,
            choices=choices,
        )
