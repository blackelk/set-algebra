import functools

from uiset import Set, Interval
from test_set import do_bulk_tests


do_bulk_search_tests = functools.partial(do_bulk_tests, fn=Set.search, mode='return')


def test_search_in_empty_set():

    assert Set().search(0) == (0, None)


def test_search_in_interval():

    i1 = Interval('(4, 7)')
    i2 = Interval('[4, 7)')
    i3 = Interval('[4, 7]')
    tests = [
        ([i1], 2, (0, None)),
        ([i1], 4, (0, None)),
        ([i1], 5, (0, i1)),
        ([i1], 7, (1, None)),
        ([i1], 9, (1, None)),
        
        ([i2], 4, (0, i2)),
        ([i2], 5, (0, i2)),
        ([i2], 7, (1, None)),
        ([i2], 8, (1, None)),

        ([i3], 5, (0, i3)),
        ([i3], 7, (0, i3)),
    ]

    do_bulk_search_tests(tests)


def test_search_in_two_intervals():

    i1 = Interval('(1, 3)')
    i2 = Interval('(5, 7)')
    s = Set([i1, i2])

    tests = [
        (s, 0, (0, None)),
        (s, 1, (0, None)),
        (s, 2, (0, i1)),
        (s, 3, (1, None)),
        (s, 4, (1, None)),
        (s, 5, (1, None)),
        (s, 6, (1, i2)),
        (s, 7, (2, None)),
    ]

    do_bulk_search_tests(tests)


def test_search_in_four_intervals():

    i1 = Interval('(-inf, 0)')
    i2 = Interval('[5, 7]')
    i3 = Interval('(9, 10)')
    i4 = Interval('(10, inf)')
    s = Set([i1, i2, i3, i4])

    tests = [
        (s, float('-inf'), (0, None)),
        (s, -2, (0, i1)),
        (s, 0, (1, None)),
        (s, 5, (1, i2)),
        (s, 6, (1, i2)),
        (s, 7, (1, i2)),
        (s, 8, (2, None)),
        (s, 9, (2, None)),
        (s, 10, (3, None)),
        (s, 1e+5, (3, i4)),
        (s, float('inf'), (4, None)),
    ]

    do_bulk_search_tests(tests)


def test_search_in_scalars():

    tests = [
        ([], 5, (0, None)),
        ([5], 4, (0, None)),
        ([5], 5, (0, 5)),
        ([5], 6, (1, None)),
        ([4, 6], 3, (0, None)),
        ([4, 6], 4, (0, 4)),
        ([4, 6], 5, (1, None)),
        ([4, 6], 6, (1, 6)),
        ([4, 6], 7, (2, None)),
        ([4, 6], float('inf'), (2, None)),
    ]

    do_bulk_search_tests(tests)


def test_search_in_interval_and_scalar():

    i1 = Interval('(4, 6)')
    i2 = Interval('[4, 6)')
    i3 = Interval('(4, 6]')
    i4 = Interval('[4, 6]')

    tests = [
        ([i1, 8], 0, (0, None)),
        ([i1, 8], 4, (0, None)),
        ([i1, 8], 5, (0, i1)),
        ([i1, 8], 6, (1, None)),
        ([i1, 8], 7, (1, None)),
        ([i1, 8], 8, (1, 8)),
        ([i1, 8], 9, (2, None)),

        ([i2, 8], 0, (0, None)),
        ([i2, 8], 4, (0, i2)),
        ([i2, 8], 5, (0, i2)),
        ([i2, 8], 6, (1, None)),
        ([i2, 8], 7, (1, None)),
        ([i2, 8], 8, (1, 8)),
        ([i2, 8], 9, (2, None)),

        ([i3, 8], 0, (0, None)),
        ([i3, 8], 4, (0, None)),
        ([i3, 8], 5, (0, i3)),
        ([i3, 8], 6, (0, i3)),
        ([i3, 8], 7, (1, None)),
        ([i3, 8], 8, (1, 8)),
        ([i3, 8], 9, (2, None)),

        ([i4, 8], 0, (0, None)),
        ([i4, 8], 4, (0, i4)),
        ([i4, 8], 5, (0, i4)),
        ([i4, 8], 6, (0, i4)),
        ([i4, 8], 7, (1, None)),
        ([i4, 8], 8, (1, 8)),
        ([i4, 8], 9, (2, None)),
    ]

    do_bulk_search_tests(tests)


def test_search_in_scalar_and_interval():

    i1 = Interval('(4, 6)')
    i2 = Interval('[4, 6)')
    i3 = Interval('(4, 6]')
    i4 = Interval('[4, 6]')

    tests = [
        ([2, i1], 1, (0, None)),
        ([2, i1], 2, (0, 2)),
        ([2, i1], 3, (1, None)),
        ([2, i1], 4, (1, None)),
        ([2, i1], 5, (1, i1)),
        ([2, i1], 6, (2, None)),
        ([2, i1], 7, (2, None)),

        ([2, i2], 1, (0, None)),
        ([2, i2], 2, (0, 2)),
        ([2, i2], 3, (1, None)),
        ([2, i2], 4, (1, i2)),
        ([2, i2], 5, (1, i2)),
        ([2, i2], 6, (2, None)),
        ([2, i2], 7, (2, None)),

        ([2, i3], 1, (0, None)),
        ([2, i3], 2, (0, 2)),
        ([2, i3], 3, (1, None)),
        ([2, i3], 4, (1, None)),
        ([2, i3], 5, (1, i3)),
        ([2, i3], 6, (1, i3)),
        ([2, i3], 7, (2, None)),

        ([2, i4], 1, (0, None)),
        ([2, i4], 2, (0, 2)),
        ([2, i4], 3, (1, None)),
        ([2, i4], 4, (1, i4)),
        ([2, i4], 5, (1, i4)),
        ([2, i4], 6, (1, i4)),
        ([2, i4], 7, (2, None)),
    ]

    do_bulk_search_tests(tests)


def test_search_in_two_scalars_and_two_intervals():

    i1 = Interval('(-inf, 0)')
    i2 = Interval('[5, 7)')
    s = Set([i1, 3, i2, 10])

    tests = [
        (s, float('-inf'), (0, None)),
        (s, -5, (0, i1)),
        (s, 0, (1, None)),
        (s, 1, (1, None)),
        (s, 3, (1, 3)),
        (s, 4, (2, None)),
        (s, 5, (2, i2)),
        (s, 6, (2, i2)),
        (s, 7, (3, None)),
        (s, 8, (3, None)),
        (s, 10, (3, 10)),
        (s, 11, (4, None)),
        (s, float('inf'), (4, None)),
    ]

    do_bulk_search_tests(tests)

