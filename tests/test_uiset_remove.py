import functools
from uiset import UISet, Interval
from test_uiset import do_bulk_tests


do_bulk_remove_tests = functools.partial(do_bulk_tests, fn=UISet.remove, mode='pieces')


# REMOVE SCALAR

def test_remove_scalar_from_empty_uiset():

    tests = [
        ([], 1, []),
    ]
    do_bulk_remove_tests(tests)


def test_remove_scalar_from_scalars_only():

    tests = [
        ([1], 0, [1]),
        ([1], 1, []),
        ([1], 2, [1]),

        ([1, 3], 0, [1, 3]),
        ([1, 3], 1, [3]),
        ([1, 3], 2, [1, 3]),
        ([1, 3], 3, [1]),
        ([1, 3], 4, [1, 3]),

        ([1, 3, 5], 0, [1, 3, 5]),
        ([1, 3, 5], 1, [3, 5]),
        ([1, 3, 5], 2, [1, 3, 5]),
        ([1, 3, 5], 3, [1, 5]),
        ([1, 3, 5], 4, [1, 3, 5]),
        ([1, 3, 5], 5, [1, 3]),
    ]

    do_bulk_remove_tests(tests)


def test_remove_scalar_from_interval():

    i1 = Interval('(1, 3)')
    i2 = Interval('[1, 3)')
    i3 = Interval('(1, 3]')
    i4 = Interval('[1, 3]')

    tests = [
        ([i1], 0, [i1]),
        ([i1], 1, [i1]),
        ([i1], 2, [Interval('(1, 2)'), Interval('(2, 3)')]),
        ([i1], 3, [i1]),
        ([i1], 4, [i1]),

        ([i2], 0, [i2]),
        ([i2], 1, [i1]),
        ([i2], 2, [Interval('[1, 2)'), Interval('(2, 3)')]),
        ([i2], 3, [i2]),
        ([i2], 4, [i2]),

        ([i3], 0, [i3]),
        ([i3], 1, [i3]),
        ([i3], 2, [Interval('(1, 2)'), Interval('(2, 3]')]),
        ([i3], 3, [i1]),
        ([i3], 4, [i3]),

        ([i4], 0, [i4]),
        ([i4], 1, [i3]),
        ([i4], 2, [Interval('[1, 2)'), Interval('(2, 3]')]),
        ([i4], 3, [i2]),
        ([i4], 4, [i4]),
    ]

    do_bulk_remove_tests(tests)

    assert i1 == Interval('(1, 3)')
    assert i2 == Interval('[1, 3)')
    assert i3 == Interval('(1, 3]')
    assert i4 == Interval('[1, 3]')


def test_remove_scalar_from_two_close_intervals():

    i1 = Interval('(1, 3)')
    i2 = Interval('[1, 3)')
    i3 = Interval('(3, 5)')
    i4 = Interval('(3, 5]')
    s = UISet([i2, i4])

    tests = [
        (s, 0, [i2, i4]),
        (s, 1, [i1, i4]),
        (s, 2, [Interval('[1, 2)'), Interval('(2, 3)'), i4]),
        (s, 3, [i2, i4]),
        (s, 4, [i2, Interval('(3, 4)'), Interval('(4, 5]')]),
        (s, 5, [i2, i3]),
        (s, 6, [i2, i4]),
    ]

    do_bulk_remove_tests(tests)

    assert i2 == Interval('[1, 3)')
    assert i4 == Interval('(3, 5]')


def test_remove_scalar_from_interval_and_scalar():

    i = Interval('[1, 3]')

    tests = [
        ([i, 5], 0, [i, 5]),
        ([i, 5], 1, [Interval('(1, 3]'), 5]),
        ([i, 5], 2, [Interval('[1, 2)'), Interval('(2, 3]'), 5]),
        ([i, 5], 3, [Interval('[1, 3)'), 5]),
        ([i, 5], 4, [i, 5]),
        ([i, 5], 5, [i]),
        ([i, 5], 6, [i, 5]),
    ]

    do_bulk_remove_tests(tests)

    assert i == Interval('[1, 3]')


def test_remove_scalar_from_three_intervals_and_2_scalars():

    i1 = Interval('(-inf, 0)')
    i2 = Interval('(0, 1)')
    i3 = Interval('[10, inf)')
    pieces = [i1, i2, 5, 7, i3]

    tests = [
        (pieces, float('-inf'), [i1, i2, 5, 7, i3]),
        (pieces, -5, [Interval('(-inf, -5)'), Interval('(-5, 0)'), i2, 5, 7, i3]),
        (pieces, 0, [i1, i2, 5, 7, i3]),
        (pieces, 1, [i1, i2, 5, 7, i3]),
        (pieces, 3, [i1, i2, 5, 7, i3]),
        (pieces, 5, [i1, i2, 7, i3]),
        (pieces, 6, [i1, i2, 5, 7, i3]),
        (pieces, 7, [i1, i2, 5, i3]),
        (pieces, 8, [i1, i2, 5, 7, i3]),
        (pieces, 10, [i1, i2, 5, 7, Interval('(10, inf)')]),
        (pieces, 11, [i1, i2, 5, 7, Interval('[10, 11)'), Interval('(11, inf)')]),
        (pieces, float('inf'), [i1, i2, 5, 7, i3]),
    ]

    do_bulk_remove_tests(tests)

    assert i1 == Interval('(-inf, 0)')
    assert i2 == Interval('(0, 1)')
    assert i3 == Interval('[10, inf)')


# REMOVE INTERVAL


def test_remove_interval_from_empty_uiset():

    tests = [
        (UISet(), Interval('(4, 5)'), []),
    ]
    do_bulk_remove_tests(tests)


def test_remove_interval_from_scalar():

    i1 = Interval('(2, 4)')
    i2 = Interval('[2, 4)')
    i3 = Interval('(2, 4]')
    i4 = Interval('[2, 4]')

    tests = [
        ([1], i1, [1]),
        ([1], i2, [1]),
        ([1], i3, [1]),
        ([1], i4, [1]),
        ([2], i1, [2]),
        ([2], i2, []),
        ([2], i3, [2]),
        ([2], i4, []),
        ([3], i1, []),
        ([3], i2, []),
        ([3], i3, []),
        ([3], i4, []),
        ([4], i1, [4]),
        ([4], i2, [4]),
        ([4], i3, []),
        ([4], i4, []),
        ([5], i1, [5]),
        ([5], i2, [5]),
        ([5], i3, [5]),
        ([5], i4, [5]),
    ]

    do_bulk_remove_tests(tests)


def test_remove_interval_from_two_scalars():

    i1 = Interval('(2, 4)')
    i2 = Interval('[2, 4)')
    i3 = Interval('(2, 4]')
    i4 = Interval('[2, 4]')

    tests = [
        ([0, 1], i1, [0, 1]),
        ([1, 2], i1, [1, 2]),
        ([1, 2], i2, [1]),
        ([1, 2], i3, [1, 2]),
        ([1, 2], i4, [1]),
        ([1, 3], i1, [1]),
        ([1, 4], i1, [1, 4]),
        ([1, 4], i2, [1, 4]),
        ([1, 4], i3, [1]),
        ([1, 4], i1, [1, 4]),
        ([1, 5], i4, [1, 5]),
        ([2, 3], i1, [2]),
        ([2, 4], i1, [2, 4]),
        ([2, 4], i2, [4]),
        ([2, 4], i3, [2]),
        ([2, 4], i4, []),
        ([2, 5], i3, [2, 5]),
        ([2, 5], i4, [5]),
        ([3, 4], i1, [4]),
        ([3, 4], i2, [4]),
        ([3, 4], i3, []),
        ([3, 4], i4, []),
        ([4, 5], i1, [4, 5]),
        ([4, 5], i2, [4, 5]),
        ([4, 5], i3, [5]),
        ([4, 5], i4, [5]),
        ([5, 6], i4, [5, 6]),
    ]

    do_bulk_remove_tests(tests)


def test_remove_interval_from_interval():

    i1 = Interval('(3, 6)')
    i2 = Interval('[3, 6]')

    tests = [
        ([i1], Interval('(1, 2)'), [i1]),
        ([i1], Interval('(2, 3)'), [i1]),
        ([i1], Interval('(2, 3]'), [i1]),
        ([i1], Interval('(2, 4)'), [Interval('[4, 6)')]),
        ([i1], Interval('(2, 4]'), [Interval('(4, 6)')]),
        ([i1], Interval('(2, 6)'), []),
        ([i1], Interval('(2, 6]'), []),
        ([i1], Interval('(2, 7]'), []),
        ([i1], Interval('(3, 4)'), [Interval('[4, 6)')]),
        ([i1], Interval('(3, 4]'), [Interval('(4, 6)')]),
        ([i1], Interval('(3, 6)'), []),
        ([i1], Interval('(3, 6]'), []),
        ([i1], Interval('(3, 7]'), []),
        ([i1], Interval('(4, 5)'), [Interval('(3, 4]'), Interval('[5, 6)')]),
        ([i1], Interval('[4, 5)'), [Interval('(3, 4)'), Interval('[5, 6)')]),
        ([i1], Interval('(4, 5]'), [Interval('(3, 4]'), Interval('(5, 6)')]),
        ([i1], Interval('[4, 5]'), [Interval('(3, 4)'), Interval('(5, 6)')]),
        ([i1], Interval('(4, 6)'), [Interval('(3, 4]')]),
        ([i1], Interval('[4, 6)'), [Interval('(3, 4)')]),
        ([i1], Interval('[4, 6]'), [Interval('(3, 4)')]),
        ([i1], Interval('[4, 7]'), [Interval('(3, 4)')]),
        ([i1], Interval('(6, 7]'), [i1]),
        ([i1], Interval('[6, 7]'), [i1]),
        ([i1], Interval('[7, 8]'), [i1]),
        ([i1], Interval('(-inf, inf)'), []),

        ([i2], Interval('(1, 2)'), [i2]),
        ([i2], Interval('(2, 3)'), [i2]),
        ([i2], Interval('(2, 3]'), [Interval('(3, 6]')]),
        ([i2], Interval('(2, 4)'), [Interval('[4, 6]')]),
        ([i2], Interval('(2, 6)'), [6]),
        ([i2], Interval('(2, 6]'), []),
        ([i2], Interval('(2, 7]'), []),
        ([i2], Interval('(3, 4)'), [3, Interval('[4, 6]')]),
        ([i2], Interval('[3, 4)'), [Interval('[4, 6]')]),
        ([i2], Interval('(3, 6)'), [3, 6]),
        ([i2], Interval('[3, 6)'), [6]),
        ([i2], Interval('(3, 6]'), [3]),
        ([i2], Interval('[3, 6]'), []),
        ([i2], Interval('[4, 5)'), [Interval('[3, 4)'), Interval('[5, 6]')]),
        ([i2], Interval('(6, 7]'), [i2]),
        ([i2], Interval('[6, 7]'), [Interval('[3, 6)')]),
        ([i2], Interval('[7, 8]'), [i2]),
        ([i2], Interval('(-inf, inf)'), []),
    ]

    do_bulk_remove_tests(tests)

    assert i1 == Interval('(3, 6)')
    assert i2 == Interval('[3, 6]')


def test_remove_interval_from_interval_and_scalar():

    i = Interval('[3, 6)')

    tests = [
        ([i, 8], Interval('(1, 2)'), [i, 8]),
        ([i, 8], Interval('(2, 3)'), [i, 8]),
        ([i, 8], Interval('(2, 3]'), [Interval('(3, 6)'), 8]),
        ([i, 8], Interval('(2, 4)'), [Interval('[4, 6)'), 8]),
        ([i, 8], Interval('(2, 6)'), [8]),
        ([i, 8], Interval('(2, 8)'), [8]),
        ([i, 8], Interval('(2, 8]'), []),
        ([i, 8], Interval('(3, 5)'), [3, Interval('[5, 6)'), 8]),
        ([i, 8], Interval('(3, 6)'), [3, 8]),
        ([i, 8], Interval('[3, 6)'), [8]),
        ([i, 8], Interval('[4, 5]'), [Interval('[3, 4)'), Interval('(5, 6)'), 8]),
        ([i, 8], Interval('[4, 6)'), [Interval('[3, 4)'), 8]),
        ([i, 8], Interval('[4, 8)'), [Interval('[3, 4)'), 8]),
        ([i, 8], Interval('[4, 8]'), [Interval('[3, 4)')]),
        ([i, 8], Interval('(-inf, inf)'), []),
    ]

    do_bulk_remove_tests(tests)

    assert i == Interval('[3, 6)')


def test_remove_interval_from_three_intervals_and_two_scalars():

    i1 = Interval('(-inf, 0)')
    i2 = Interval('(0, 1)')
    i3 = Interval('[10, inf)')
    i4 = Interval('(-inf, -5)')
    i5 = Interval('[-3, 0)')
    pieces = [i1, i2, 5, 7, i3]

    tests = [
        (pieces, i4, [Interval('[-5, 0)'), i2, 5, 7, i3]),
        (pieces, Interval('[-5, -3)'), [i4, i5, i2, 5, 7, i3]),
        (pieces, Interval('[-5, 5)'), [i4, 5, 7, i3]),
        (pieces, Interval('[-5, 5]'), [i4, 7, i3]),
        (pieces, Interval('[-5, 8]'), [i4, i3]),
        (pieces, Interval('[-5, 10]'), [i4, Interval('(10, inf)')]),
        (pieces, Interval('[-5, 12]'), [i4, Interval('(12, inf)')]),
        (pieces, Interval('(-inf, inf)'), []),
    ]

    do_bulk_remove_tests(tests)

    assert i1 == Interval('(-inf, 0)')
    assert i2 == Interval('(0, 1)')
    assert i3 == Interval('[10, inf)')

