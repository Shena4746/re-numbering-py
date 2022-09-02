from __future__ import annotations

from typing import Iterable, Optional

import click

from Text_Line import Paged_Text_Line
from Text_Lines import Paged_Text_Lines


class Re_Numbering:
    def __init__(self, lines: Paged_Text_Lines) -> None:
        self.lines: Paged_Text_Lines = lines

    def _update_numbering(self, new_numbers: list[Optional[int]]) -> Paged_Text_Lines:
        """get new texts with new page number of self.lines overwritten by input numbers."""
        if len(new_numbers) != len(self.lines):
            raise ValueError(f"inconsistent number of rows. new_numbers={len(new_numbers)}, original={self.lines}")
        return Paged_Text_Lines(
            [
                Paged_Text_Line(
                    text=self.lines[i].text,
                    page_number=number,
                    roman_page_number=self.lines[i].roman_page_number,
                    sep=self.lines[i].sep,
                )
                for i, number in enumerate(new_numbers)
            ]
        )

    def _get_order_disturbing_rows(self, lines: Paged_Text_Lines) -> list[Paged_Text_Line]:
        """get rows at which page numbers are not increasing or blank."""
        bad_rows: list[Paged_Text_Line] = []
        last: int = -(10**5)  # init value small enough
        for line in lines:
            if line.page_number is not None:
                if line.page_number < last:
                    bad_rows.append(line)
                last = line.page_number
        return bad_rows

    def _ask_continue(self, msg: Optional[str] = None, with_displaying: Optional[str] = None) -> bool:
        """ask user whether to continue, and abort if the answer is no. this method is intended to be called when some problematic rows are found in the preceding process."""
        if with_displaying is not None:
            print(with_displaying)
        _msg: str = "Some pages seem badly numbered. continue?" if msg is None else msg
        return click.confirm(text=_msg)

    def _get_contents_of_rows(self, non_numbered: Iterable[Paged_Text_Line]) -> str:
        return "\n".join([line.to_text() for line in non_numbered])

    def _get_new_numbers(self) -> list[Optional[int]]:
        """analyze self rows and return new numbers by which existing numbers should be overwritten. this method also record blank-numbered pages."""
        slide: int = 0
        new_numbers: list[Optional[int]] = []
        for line in self.lines:
            if line.page_order.set:
                new_numbers.append(line.page_order.after)
                slide = line.page_order.after - line.page_order.before
            elif line.page_number is not None:
                new_numbers.append(line.page_number + slide)
            else:
                new_numbers.append(None)
        return new_numbers

    def _ensure_no_unintended_order_disturber(self, lines: Paged_Text_Lines) -> None:
        """check rows are properly ordered. if not, ask user whether to continue."""
        bad_rows: list[Paged_Text_Line] = self._get_order_disturbing_rows(lines)
        if bad_rows != [] and not self._ask_continue(with_displaying=self._get_contents_of_rows(bad_rows)):
            raise click.Abort()

    def re_numbering(self) -> Paged_Text_Lines:
        """get re-numbered rows. if some problem are found during the process, then it interactively ask user whether to continue. if user chooses to stop, no change will be made to the original text."""
        new_numbers: list[Optional[int]] = self._get_new_numbers()
        updated = self._update_numbering(new_numbers=new_numbers)
        self._ensure_no_unintended_order_disturber(updated)
        return updated
