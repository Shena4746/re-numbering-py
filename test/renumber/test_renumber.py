import os
import sys
from typing import Optional

import pytest

sys.path.append(os.path.join(".", "scr"))
from Re_Numbering import Re_Numbering  # type: ignore

# from scr.Re_Numbering import Re_Numbering
# from scr.Text_Lines import Paged_Text_Lines
from Text_Lines import Paged_Text_Lines  # type: ignore


@pytest.fixture
def data_get_new_numbers() -> list[tuple[list[str], list[Optional[int]]]]:
    return [
        (["1", "2->5", "3", "4->10", "5"], [1, 5, 6, 10, 11]),
        (["1", "2->5", "", "4->10", "5"], [1, 5, None, 10, 11]),
    ]


@pytest.fixture
def data_get_order_disturbing_rows_found() -> list[list[str]]:
    return [["1", "2", "1"], ["-9", "-10", "1"], ["-3", "-1", "0"]]


def test_get_new_numbers(data_get_new_numbers):
    for data, ans in data_get_new_numbers:
        ptls = Paged_Text_Lines(data)
        renumbering = Re_Numbering(ptls)
        print(ptls)
        assert renumbering._get_new_numbers() == ans


def test_get_order_disturbing_rows_found(data_get_order_disturbing_rows_found):
    renumbering = Re_Numbering(Paged_Text_Lines())
    for data in data_get_order_disturbing_rows_found:
        ptls = Paged_Text_Lines(data)
        print(ptls)
        assert renumbering._get_order_disturbing_rows(ptls) != []
