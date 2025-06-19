from dataclasses import dataclass
from typing import TypeAlias


@dataclass(frozen=True)
class CutCommand:
    pass


@dataclass(frozen=True)
class PrintTextCommand:
    text: str
    cut: bool


@dataclass(frozen=True)
class PrintQRCodeCommand:
    content: str
    size: int


PrinterCommand: TypeAlias = CutCommand | PrintTextCommand | PrintQRCodeCommand
