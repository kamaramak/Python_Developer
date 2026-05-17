from dataclasses import dataclass
from typing import Optional


class BaseCallbackFactory:
    def __init__(self, section_prefix: str):
        self.section_prefix = section_prefix

    def base_callback_pagination(self):
        return f"{self.section_prefix}:pagination:"

    def callback_pagination(self, page: int):
        return f"{self.section_prefix}:pagination:{page}"

    def base_callback_year(self):
        return f"{self.section_prefix}:year:"

    def callback_year(self, year: int, value_type: Optional[str] = None):
        if value_type is not None:
            return f"{self.section_prefix}:year:{value_type}:{year}"
        return f"{self.section_prefix}:year:{year}"

    def base_callback_all_years(self):
        return f"{self.section_prefix}:years:"

    def callback_all_years(self, decade: int):
        return f"{self.section_prefix}:years:{decade}"

    def callback_menu(self):
        return f"{self.section_prefix}:menu"

    def callback_back_to_menu(self):
        return f"{self.section_prefix}:menu"


@dataclass
class ParsedCallback:
    section: str
    subsection: str
    value: Optional[int | str] = None
    value_type: Optional[str] = None


def parse_callback(data: str) -> ParsedCallback:
    parts = data.split(":")
    if len(parts) > 3:
        return ParsedCallback(
            section=parts[0],
            subsection=parts[1],
            value_type=parts[2],
            value=parts[3],
        )
    elif len(parts) > 2:
        return ParsedCallback(
            section=parts[0],
            subsection=parts[1],
            value=parts[2],
            value_type=None,
        )
    return ParsedCallback(
        section=parts[0],
        subsection=parts[1],
        value=None,
        value_type=None,
    )
