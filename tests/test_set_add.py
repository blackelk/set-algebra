import functools
import pytest

from set_algebra import Set, Interval
from test_set import do_bulk_tests


do_bulk_add_tests = functools.partial(do_bulk_tests, fn=Set.add, mode='pieces')


# ADD SCALAR

def test_add_scalar_to_empty_set():

    tests = [
        ([], 1, [1]),
    ]
    do_bulk_add_tests(tests)


def test_add_scalar_to_scalars_only():

    tests = [
        ([1], 0, [0, 1]),
        ([1], 1, [1]),
        ([1], 2, [1, 2]),

        ([1, 3], 0, [0, 1, 3]),
        ([1, 3], 1, [1, 3]),
        ([1, 3], 2, [1, 2, 3]),
        ([1, 3], 3, [1, 3]),
        ([1, 3], 4, [1, 3, 4]),

        ([1, 3, 5], 0, [0, 1, 3, 5]),
        ([1, 3, 5], 1, [1, 3, 5]),
        ([1, 3, 5], 2, [1, 2, 3, 5]),
        ([1, 3, 5], 3, [1, 3, 5]),
        ([1, 3, 5], 4, [1, 3, 4, 5]),
        ([1, 3, 5], 5, [1, 3, 5]),
    ]

    do_bulk_add_tests(tests)


def test_add_scalar_to_interval():

    i1 = Interval('(1, 3)')
    i2 = Interval('[1, 3)')
    i3 = Interval('(1, 3]')
    i4 = Interval('[1, 3]')

    tests = [
        ([i1], 0, [0, i1]),
        ([i1], 1, [i2]),
        ([i1], 2, [i1]),
        ([i1], 3, [i3]),
        ([i1], 4, [i1, 4]),

        ([i2], 0, [0, i2]),
        ([i2], 1, [i2]),
        ([i2], 2, [i2]),
        ([i2], 3, [i4]),
        ([i2], 4, [i2, 4]),

        ([i3], 0, [0, i3]),
        ([i3], 1, [i4]),
        ([i3], 2, [i3]),
        ([i3], 3, [i3]),
        ([i3], 4, [i3, 4]),

        ([i4], 0, [0, i4]),
        ([i4], 1, [i4]),
        ([i4], 2, [i4]),
        ([i4], 3, [i4]),
        ([i4], 4, [i4, 4]),
    ]

    do_bulk_add_tests(tests)

    assert i1 == Interval('(1, 3)')
    assert i2 == Interval('[1, 3)')
    assert i3 == Interval('(1, 3]')
    assert i4 == Interval('[1, 3]')


def test_add_scalar_to_two_intervals():

    i1 = Interval('(1, 3)')
    i2 = Interval('[1, 3)')
    i3 = Interval('(1, 3]')
    i4 = Interval('[1, 3]')
    i5 = Interval('(5, 7)')
    i6 = Interval('[5, 7)')
    i7 = Interval('(5, 7]')
    i8 = Interval('[5, 7]')

    tests = [
        ([i1, i5], 0, [0, i1, i5]),
        ([i1, i5], 1, [i2, i5]),
        ([i1, i5], 2, [i1, i5]),
        ([i1, i5], 3, [i3, i5]),
        ([i1, i5], 4, [i1, 4, i5]),
        ([i1, i5], 5, [i1, i6]),
        ([i1, i5], 6, [i1, i5]),
        ([i1, i5], 7, [i1, i7]),
        ([i1, i5], 8, [i1, i5, 8]),

        ([i2, i5], 0, [0, i2, i5]),
        ([i2, i5], 1, [i2, i5]),
        ([i2, i5], 2, [i2, i5]),
        ([i2, i5], 3, [i4, i5]),
        ([i2, i5], 4, [i2, 4, i5]),
        ([i2, i5], 5, [i2, i6]),
        ([i2, i5], 6, [i2, i5]),
        ([i2, i5], 7, [i2, i7]),
        ([i2, i5], 8, [i2, i5, 8]),

        ([i2, i6], 0, [0, i2, i6]),
        ([i2, i6], 1, [i2, i6]),
        ([i2, i6], 2, [i2, i6]),
        ([i2, i6], 3, [i4, i6]),
        ([i2, i6], 4, [i2, 4, i6]),
        ([i2, i6], 5, [i2, i6]),
        ([i2, i6], 6, [i2, i6]),
        ([i2, i6], 7, [i2, i8]),
        ([i2, i6], 8, [i2, i6, 8]),
    ]

    do_bulk_add_tests(tests)

    assert i1 == Interval('(1, 3)')
    assert i2 == Interval('[1, 3)')
    assert i3 == Interval('(1, 3]')
    assert i4 == Interval('[1, 3]')
    assert i5 == Interval('(5, 7)')
    assert i6 == Interval('[5, 7)')
    assert i7 == Interval('(5, 7]')
    assert i8 == Interval('[5, 7]')


def test_add_scalar_to_two_close_intervals():

    i1 = Interval('(1, 3)')
    i2 = Interval('(3, 5)')
    s = Set([i1, i2])

    tests = [
        (s, 0, [0, i1, i2]),
        (s, 1, [Interval('[1, 3)'), i2]),
        (s, 2, [i1, i2]),
        (s, 3, [Interval('(1, 5)')]),
        (s, 4, [i1, i2]),
        (s, 5, [i1, Interval('(3, 5]')]),
        (s, 6, [i1, i2, 6]),
    ]

    do_bulk_add_tests(tests)

    assert i1 == Interval('(1, 3)')
    assert i2 == Interval('(3, 5)')


def test_add_scalar_to_interval_and_scalar():

    i1 = Interval('(1, 3)')
    i2 = Interval('[1, 3)')
    i3 = Interval('(1, 3]')

    tests = [
        ([i1, 5], 0, [0, i1, 5]),
        ([i1, 5], 1, [i2, 5]),
        ([i1, 5], 2, [i1, 5]),
        ([i1, 5], 3, [i3, 5]),
        ([i1, 5], 4, [i1, 4, 5]),
        ([i1, 5], 5, [i1, 5]),
        ([i1, 5], 6, [i1, 5, 6]),
    ]

    do_bulk_add_tests(tests)

    assert i1 == Interval('(1, 3)')
    assert i2 == Interval('[1, 3)')
    assert i3 == Interval('(1, 3]')


def test_add_scalar_to_three_intervals_and_2_scalars():

    i1 = Interval('(-inf, 0)')
    i2 = Interval('(0, 1)')
    i3 = Interval('[10, inf)')
    pieces = [i1, i2, 5, 7, i3]

    tests = [
        (pieces, -5, [i1, i2, 5, 7, i3]),
        (pieces, 0, [Interval('(-inf, 1)'), 5, 7, i3]),
        (pieces, 1, [i1, Interval('(0, 1]'), 5, 7, i3]),
        (pieces, 3, [i1, i2, 3, 5, 7, i3]),
        (pieces, 5, [i1, i2, 5, 7, i3]),
        (pieces, 6, [i1, i2, 5, 6, 7, i3]),
        (pieces, 7, [i1, i2, 5, 7, i3]),
        (pieces, 8, [i1, i2, 5, 7, 8, i3]),
        (pieces, 10, [i1, i2, 5, 7, i3]),
        (pieces, 11, [i1, i2, 5, 7, i3]),
    ]

    do_bulk_add_tests(tests)

    assert i1 == Interval('(-inf, 0)')
    assert i2 == Interval('(0, 1)')
    assert i3 == Interval('[10, inf)')


def test_add_infinity_raises():

    s = Set('(1, 3)')
    with pytest.raises(ValueError):
        s.add(float('inf'))


# ADD INTERVAL


def test_add_interval_to_empty_set():

    i = Interval('(1, 2)')
    tests = [
        ([], i, [i]),
    ]

    do_bulk_add_tests(tests)


def test_add_interval_to_scalar():

    i1 = Interval('(3, 5)')
    i2 = Interval('[3, 5)')
    i3 = Interval('(3, 5]')
    i4 = Interval('[3, 5]')

    tests = [
        ([0], i1, [0, i1]),
        ([3], i1, [i2]),
        ([4], i1, [i1]),
        ([5], i1, [i3]),
        ([6], i1, [i1, 6]),

        ([0], i2, [0, i2]),
        ([3], i2, [i2]),
        ([4], i2, [i2]),
        ([5], i2, [i4]),
        ([6], i2, [i2, 6]),

        ([0], i3, [0, i3]),
        ([3], i3, [i4]),
        ([4], i3, [i3]),
        ([5], i3, [i3]),
        ([6], i3, [i3, 6]),

        ([0], i4, [0, i4]),
        ([3], i4, [i4]),
        ([4], i4, [i4]),
        ([5], i4, [i4]),
        ([6], i4, [i4, 6]),
    ]

    do_bulk_add_tests(tests)

    assert i1 == Interval('(3, 5)')
    assert i2 == Interval('[3, 5)')
    assert i3 == Interval('(3, 5]')
    assert i4 == Interval('[3, 5]')


def test_add_interval_to_two_scalars():

    i1 = Interval('(3, 5)')
    i2 = Interval('[3, 5)')
    i3 = Interval('(3, 5]')
    i4 = Interval('[3, 5]')

    tests = [
        ([0, 1], i1, [0, 1, i1]),
        ([0, 3], i1, [0, i2]),
        ([0, 4], i1, [0, i1]),
        ([0, 5], i1, [0, i3]),
        ([0, 6], i1, [0, i1, 6]),
        ([1, 3], i1, [1, i2]),
        ([1, 4], i1, [1, i1]),
        ([1, 5], i1, [1, i3]),
        ([3, 4], i1, [i2]),
        ([3, 5], i1, [i4]),
        ([3, 6], i1, [i2, 6]),
        ([4, 5], i1, [i3]),
        ([4, 6], i1, [i1, 6]),
        ([5, 6], i1, [i3, 6]),
        ([6, 7], i1, [i1, 6, 7]),
    ]

    do_bulk_add_tests(tests)

    assert i1 == Interval('(3, 5)')


def test_add_interval_to_interval():

    i1 = Interval('(3, 6)')
    i2 = Interval('[3, 6)')
    i3 = Interval('(3, 6]')
    i4 = Interval('[3, 6]')

    i5 = Interval('(1, 2)')
    i6 = Interval('(1, 3)')
    i7 = Interval('(1, 3]')
    i8 = Interval('(1, 4]')
    i9 = Interval('(1, 6)')
    i10 = Interval('(1, 6]')
    i11 = Interval('(1, 7)')
    i12 = Interval('(3, 4)')
    i13 = Interval('[3, 4)')
    i14 = Interval('(3, 7)')
    i15 = Interval('[3, 7)')
    i16 = Interval('(4, 6)')
    i17 = Interval('(4, 6]')
    i18 = Interval('(4, 7)')
    i19 = Interval('(6, 7)')
    i20 = Interval('[6, 7)')

    tests = [
        ([i1], i1, [i1]),
        ([i1], i2, [i2]),
        ([i1], i3, [i3]),
        ([i1], i4, [i4]),
        ([i1], i5, [i5, i1]),
        ([i1], i6, [i6, i1]),
        ([i1], i7, [i9]),
        ([i1], i8, [i9]),
        ([i1], i9, [i9]),
        ([i1], i10, [i10]),
        ([i1], i11, [i11]),
        ([i1], i12, [i1]),
        ([i1], i13, [i2]),
        ([i1], i14, [i14]),
        ([i1], i15, [i15]),
        ([i1], i16, [i1]),
        ([i1], i17, [i3]),
        ([i1], i18, [i14]),
        ([i1], i19, [i1, i19]),
        ([i1], i20, [i14]),

        ([i2], i1, [i2]),
        ([i2], i2, [i2]),
        ([i2], i3, [i4]),
        ([i2], i4, [i4]),
        ([i2], i5, [i5, i2]),
        ([i2], i6, [i9]),
        ([i2], i7, [i9]),
        ([i2], i8, [i9]),
        ([i2], i12, [i2]),
        ([i2], i13, [i2]),
        ([i2], i14, [i15]),
        ([i2], i15, [i15]),
        ([i2], i16, [i2]),
        ([i2], i17, [i4]),
        ([i2], i18, [i15]),
        ([i2], i19, [i2, i19]),
        ([i2], i20, [i15]),
        ([i3], i19, [i14])
    ]

    do_bulk_add_tests(tests)

    assert i1 == Interval('(3, 6)')
    assert i2 == Interval('[3, 6)')
    assert i3 == Interval('(3, 6]')
    assert i4 == Interval('[3, 6]')
    assert i5 == Interval('(1, 2)')
    assert i6 == Interval('(1, 3)')
    assert i7 == Interval('(1, 3]')
    assert i8 == Interval('(1, 4]')
    assert i9 == Interval('(1, 6)')
    assert i10 == Interval('(1, 6]')
    assert i11 == Interval('(1, 7)')
    assert i12 == Interval('(3, 4)')
    assert i13 == Interval('[3, 4)')
    assert i14 == Interval('(3, 7)')
    assert i15 == Interval('[3, 7)')
    assert i16 == Interval('(4, 6)')
    assert i17 == Interval('(4, 6]')
    assert i18 == Interval('(4, 7)')
    assert i19 == Interval('(6, 7)')
    assert i20 == Interval('[6, 7)')


def test_add_interval_to_three_intervals_and_two_scalars():

    i1 = Interval('(-inf, 0)')
    i2 = Interval('(0, 1)')
    i3 = Interval('[10, inf)')
    i4 = Interval('(-inf, 0)')
    i5 = Interval('(-inf, 0]')
    i6 = Interval('[0, 1]')
    i7 = Interval('(0, 1]')
    i8 = Interval('(-1, 5)')
    i9 = Interval('(5, 7)')
    i10 = Interval('(1, 7)')
    i11 = Interval('[0, 10]')
    i12 = Interval('(-inf, inf)')
    pieces = [i1, i2, 5, 7, i3]

    tests = [
        (pieces, i4, [i1, i2, 5, 7, i3]),
        (pieces, i5, [Interval('(-inf, 1)'), 5, 7, i3]),
        (pieces, i6, [Interval('(-inf, 1]'), 5, 7, i3]),
        (pieces, i7, [i1, i7, 5, 7, i3]),
        (pieces, i8, [Interval('(-inf, 5]'), 7, i3]),
        (pieces, i9, [i1, i2, Interval('[5, 7]'), i3]),
        (pieces, i10, [i1, i2, Interval('(1, 7]'), i3]),
        (pieces, i11, [i12]),
        (pieces, i12, [i12]),
    ]

    do_bulk_add_tests(tests)

    assert i1 == Interval('(-inf, 0)')
    assert i2 == Interval('(0, 1)')
    assert i3 == Interval('[10, inf)')
    assert i4 == Interval('(-inf, 0)')
    assert i5 == Interval('(-inf, 0]')
    assert i6 == Interval('[0, 1]')
    assert i7 == Interval('(0, 1]')
    assert i8 == Interval('(-1, 5)')
    assert i9 == Interval('(5, 7)')
    assert i10 == Interval('(1, 7)')
    assert i11 == Interval('[0, 10]')
    assert i12 == Interval('(-inf, inf)')

