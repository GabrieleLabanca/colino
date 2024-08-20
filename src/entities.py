from dataclasses import dataclass
from typing import Optional


@dataclass
class Article:
    title: str
    subtitle: str
    body: str
    has_image: Optional[bool] = None
    position_in_page: Optional[int] = None
    font_style: Optional[str] = None
