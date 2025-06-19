from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Optional


class CommandType(StrEnum):
    CUT = auto()
    TEXT = auto()


@dataclass
class PrinterCommand:
    type: CommandType
    text: Optional[str] = None
