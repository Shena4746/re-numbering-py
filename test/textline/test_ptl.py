import os
import re
import sys
from re import Match, Pattern

import pytest

sys.path.append(os.path.join(".", "scr"))
# from scr.Text_Line import Paged_Text_Line
from Text_Line import Paged_Text_Line, Text_Line  # type: ignore


@pytest.fixture
def text_with_arabic_page() -> list[tuple[str, str, int | None]]:
    return [
        ("text1 15", "text1", 15),
        ("text2 203 204", "text2 203", 204),
        ("text3 303 303", "text3 303", 303),
        ("text40", "text", 40),
        ("text", "text", None),
    ]


@pytest.fixture
def text_with_roman_page() -> list[tuple[str, str, str | None]]:
    return [
        ("text1 xi", "text1", "xi"),
        ("text2 203 v", "text2 203", "v"),
        ("text3 303 iii", "text3 303", "iii"),
        ("text4v", "text4v", None),
        ("text", "text", None),
        ("test6 i", "test6", "i"),
    ]


@pytest.fixture
def data_test_roman_pattern() -> list[tuple[Pattern, str, int | None, bool]]:
    # term1	    term2	term3
    # roman	    roman	all
    # roman	    arabic	second
    # roman	    roman	first
    # arabic    arabic	all
    # arabic	roman	second
    # arabic	arabic	first
    pat = re.compile("(?=\\s|^)\\s?(?P<key>[ixv]+|[IXV]+)$")
    return [
        (pat, "ix iv", None, True),
        (pat, "ix 4 4", 1, False),
        (pat, "ix iv", 0, True),
        (pat, "1 4", None, False),
        (pat, "2 v v", 1, True),
        (pat, "6 4", 0, False),
    ]


@pytest.fixture
def data_apply_roman_pattern() -> list[tuple[Pattern, str, int | None, str | list[Match]]]:
    # term1	    term2	term3
    # roman	    roman	all
    # roman	    arabic	second
    # roman	    roman	first
    # arabic    arabic	all
    # arabic	roman	second
    # arabic	arabic	first
    pat = re.compile("(?=\\s|^)\\s?(?P<key>[ixv]+|[IXV]+)$")
    return [
        (pat, "ix iv iv", None, "iv"),
        (pat, "ix 4 4", 1, []),
        (pat, "iii xxi xxi", 0, "iii"),
        (pat, "1 4 4", None, []),
        (pat, "2 v v", 1, "v"),
        (pat, "6 4 4", 0, []),
    ]


@pytest.fixture
def text_page_order_ok() -> list[tuple[str, int, int]]:
    return [
        ("text1 1->5", 1, 5),
        ("text1 1 ->5", 1, 5),
        ("text1 1-> 5", 1, 5),
        ("text1 1 -> 5", 1, 5),
        ("text1 10 -> 5", 10, 5),
        ("text1 10  ->  5", 10, 5),
    ]


@pytest.fixture
def text_page_order_ng() -> list[str]:
    return [
        ("text1 1->"),
        ("text1 ->1"),
        ("text1 ->"),
        ("text1"),
        ("text1 1->>2"),
        ("text1 1>>2"),
        ("text1 1-->2"),
    ]


@pytest.fixture
def text_get_text_without_page() -> list[tuple[str, str]]:
    return [("text1 1->5", "text1"), ("text1 1", "text1")]


def test_ptl_separates_arabic_pages(text_with_arabic_page):
    for text, res_text, res_page in text_with_arabic_page:
        ptl = Paged_Text_Line(idx=-1, text=text)
        print(ptl)
        assert ptl.text == res_text
        assert ptl.page_number == res_page


def test_ptl_separates_roman_pages(text_with_roman_page):
    for text, res_text, res_page in text_with_roman_page:
        ptl = Paged_Text_Line(idx=-1, text=text)
        print(ptl)
        assert ptl.text == res_text
        assert ptl.roman_page_number == res_page


def test_page_order_ok(text_page_order_ok):
    for text, x, y in text_page_order_ok:
        ptl = Paged_Text_Line(text=text)
        assert ptl.page_order.before == x and ptl.page_order.after == y


def test_page_order_ng(text_page_order_ng):
    for text in text_page_order_ng:
        ptl = Paged_Text_Line(text=text)
        print(ptl)
        assert not ptl.page_order.set


def test_get_text_without_page(text_get_text_without_page):
    for text, ans in text_get_text_without_page:
        ptl = Paged_Text_Line(text=text)
        print(ptl)
        assert ptl.text == ans
