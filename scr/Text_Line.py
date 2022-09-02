from __future__ import annotations

import dataclasses
import re
from re import Match, Pattern
from typing import Final, Optional

from typing_extensions import Self


class Text_Line:
    def __init__(self, idx: int = -1, text: str = "", sep: str = " ") -> None:
        self._validate_text(text)
        self.idx: int = idx
        self._text: str = text
        self._sep: str = sep

    def __lt__(self, other: Self) -> bool:
        return self.idx < other.idx

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: idx={self.idx}, text={self.to_text()}"

    def __len__(self) -> int:
        return len(self.text)

    @property
    def sep(self) -> str:
        return self._sep

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text

    def is_empty(self) -> bool:
        return self.to_text() == ""

    def alter_sep(self, sep: str) -> None:
        self._sep = sep

    def to_text(self) -> str:
        return self.text

    def get_instance(self, idx: int, text: str, sep: str) -> Self:
        return Text_Line(idx=idx, text=text, sep=sep)

    def format_space(self) -> Self:
        return self.get_instance(
            idx=self.idx, text=" ".join([t for t in self.to_text().split(" ") if t != ""]), sep=self.sep
        )

    def _has_newline(self, text: str) -> bool:
        return len(lines := text.splitlines()) != 0 and lines[0] != text

    def _validate_text(self, text: str) -> bool:
        """text should be free of newline characters"""
        if self._has_newline(text):
            raise ValueError(f"text must admit no newline character. text={text}")
        return True


@dataclasses.dataclass
class Page_Order:
    _set: bool = False
    before: int = -1
    after: int = -1

    def __init__(self, before: Optional[int] = None, after: Optional[int] = None) -> None:
        self.before: int = -1 if before is None else before
        self.after: int = -1 if after is None else after
        self._set: bool = before is not None and after is not None

    @property
    def set(self) -> bool:
        return self._set


class Paged_Text_Line(Text_Line):

    page_key: Final[str] = "page"
    roman_page_key: Final[str] = "roman_page"
    page_key_order: list[str] = ["page_key_before", "page_key_after"]
    pat_page: Final[Pattern] = re.compile(f"(?P<{page_key}>\\s?[0-9]+)$")
    pat_roman_page: Final[Pattern] = re.compile(f"(?=\\s|^)\\s?(?P<{roman_page_key}>[ixv]+|[IXV]+)$")
    pat_page_order: Final[Pattern] = re.compile(
        f"(?P<{page_key_order[0]}>\\-?\\d+)\\s*?->\\s*?(?P<{page_key_order[1]}>\\d+)$"
    )

    def __init__(
        self,
        idx: int = -1,
        text: str = "",
        sep: str = " ",
        page_number: Optional[int] = None,
        roman_page_number: Optional[str] = None,
        text_line: Optional[Text_Line] = None,
    ) -> None:
        # about page number
        super().__init__(idx=idx, text=text, sep=sep)
        if text_line is not None:
            self.idx: int = text_line.idx
            self._text: str = text_line.text
            self._sep: str = text_line.sep
        # init page number property
        self.page_number: Optional[int] = page_number
        self.roman_page_number: Optional[str] = roman_page_number
        # automatically separate page number and text
        self.page_number = self._get_page_number() if page_number is None else page_number
        self.roman_page_number = self._get_roman_page_number() if not self.is_page_set() else roman_page_number
        self.page_order: Page_Order = self._get_page_order(text)
        self._text = self._get_text_without_page()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: idx={self.idx}, text={self.text}, page_number={self.page_number}, roman_page_number={self.roman_page_number}, page_order_before={self.page_order.before}, page_order_after={self.page_order.after}"

    def _get_page_order(self, text: str) -> Page_Order:
        match: Optional[Match] = re.search(self.pat_page_order, text)
        return (
            Page_Order()
            if match is None
            else Page_Order(
                before=int(match.group(self.page_key_order[0])), after=int(match.group(self.page_key_order[1]))
            )
        )

    def update_page_number(self, overwrite: bool = False) -> None:
        """manually update page number. might be needed if text is significantly changed."""
        if overwrite or not self.is_page_set():
            self.page_number = self._get_page_number()
            self.roman_page_number = self._get_roman_page_number()

    def get_instance(
        self,
        idx: int = -1,
        text: str = "",
        sep: str = " ",
        page_number: Optional[int] = None,
        roman_page_number: Optional[str] = None,
        text_line: Optional[Text_Line] = None,
    ) -> Self:
        return Paged_Text_Line(
            idx=idx,
            text=text,
            sep=sep,
            page_number=page_number,
            roman_page_number=roman_page_number,
            text_line=text_line,
        )

    def to_text(self, sep: str | None = None, combine: bool = True) -> str:
        """combine text and page number."""
        if not combine or not self.is_page_set():
            return self.text
        separator: str = self.sep if sep is None else sep
        page = self.page_number if self.page_number is not None else self.roman_page_number
        return separator.join([self.text, str(page)])

    def _get_page_number(self) -> int | None:
        """get arabic page number if it exists"""
        match: Optional[Match] = re.search(self.pat_page, self.text)
        return int(match.group(self.page_key)) if match else None

    def get_page_string(self) -> str:
        if self.page_number is not None:
            return str(self.page_number)
        elif self.roman_page_number is not None:
            return self.roman_page_number
        return ""

    def _get_roman_page_number(self) -> str | None:
        """get roman page number. at the time of writing, this method is designed to be called only if no arabic page number is found."""
        match: Optional[Match] = re.search(self.pat_roman_page, self.text)
        return match.group(self.roman_page_key) if match else None

    def is_page_set(self) -> bool:
        """test if page number is set in property, arabic or roman"""
        return self.page_number is not None or self.roman_page_number is not None

    def is_page_number_only(self) -> bool:
        return self.is_page_set() and self.text == ""

    def _get_text_without_page(self) -> str:
        """get text with no page number. this method is assumed to be called only for initiating self.text property in constructor, and not for other purposes."""
        pat: Pattern
        key: str
        if not self.is_page_set() and not self.page_order.set:
            return self.text
        elif self.page_order.set:
            pat = self.pat_page_order
            key = self.page_key_order[0]
        else:
            is_arabic_page: bool = self.page_number is not None
            pat = self.pat_page if is_arabic_page else self.pat_roman_page
            key = self.page_key if is_arabic_page else self.roman_page_key
        match: Optional[Match] = re.search(pat, self.text)
        # matches might be empty. it happens, for instance, when page number is directly named in constructor.
        if match is not None:
            text_end: int = match.start(key)
            return self.text[:text_end].strip()
        return self.text
