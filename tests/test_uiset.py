from uiset import Interval, UISet


def test_uiset_init():

    s = UISet()
    assert s.intervals == []

    s = UISet([])
    assert s.intervals == []

    i1 = Interval('[1, 4]')
    i2 = Interval('[7, 9]')
    s = UISet([i1, i2])
    assert s.intervals == [Interval('[1, 4]'), Interval('[7, 9]')]

    i1 = Interval('[7, 9]')
    i2 = Interval('[1, 4]')
    s = UISet([i1, i2])
    assert s.intervals == [Interval('[1, 4]'), Interval('[7, 9]')]

    i1 = Interval('[1, 9]')
    i2 = Interval('[3, 5]')
    s = UISet([i1, i2])
    assert s.intervals == [Interval('[1, 9]')]

    i1 = Interval('[3, 5]')
    i2 = Interval('[1, 9]')
    s = UISet([i1, i2])
    assert s.intervals == [Interval('[1, 9]')]

    i1 = Interval('[1, 6]')
    i2 = Interval('[5, 8]')
    s = UISet([i1, i2])
    assert s.intervals == [Interval('[1, 8]')]

    i1 = Interval('[5, 8]')
    i2 = Interval('[1, 6]')
    s = UISet([i1, i2])
    assert s.intervals == [Interval('[1, 8]')]

    i1 = Interval('(0, 1)')
    i2 = Interval('(1, 2)')
    s = UISet([i1, i2])
    assert s.intervals == [Interval('(0, 1)'), Interval('(1, 2)')]


def test_uiset_bool():

    s = UISet()
    assert bool(s) is False

    s.add(Interval('[1, 2]'))
    assert bool(s) is True


def test_uiset_add():

    s = UISet()
    i1 = Interval('(-inf, 0)')
    s.add(i1)
    assert s.intervals == [i1]
    i2 = Interval('(-inf, 0)')
    s.add(i2)
    assert s.intervals == [i1]
    i3 = Interval('[-1, 0]')
    s.add(i3)
    assert s.intervals == [Interval('(-inf, 0]')]
    i4 = Interval('(0, 1)')
    s.add(i4)
    assert s.intervals == [Interval('(-inf, 0]'), i4]

    # Make sure original intervals has not changed.
    assert i1 == Interval('(-inf, 0)')
    assert i2 == Interval('(-inf, 0)')
    assert i3 == Interval('[-1, 0]')
    assert i4 == Interval('(0, 1)')


def test_uiset_inverse():

    i0 = Interval('(-inf, inf)')
    s = UISet([i0])
    assert (~s).intervals == []
    assert (~~s).intervals == s.intervals

    s = UISet()
    assert (~s).intervals == [i0]
    assert (~~s).intervals == s.intervals

    i1 = Interval('[1, 4]')
    i2 = Interval('[7, 9]')
    s = UISet([i1, i2])
    expected = [Interval('(-inf, 1)'), Interval('(4, 7)'), Interval('(9, inf)')]
    assert (~s).intervals == expected
    assert (~~s).intervals == s.intervals

    i3 = Interval('[5, 8]')
    i4 = Interval('[1, 6]')
    s = UISet([i3, i4])
    assert (~s).intervals == [Interval('(-inf, 1)'), Interval('(8, inf)')]
    assert (~~s).intervals == s.intervals

    i5 = Interval('(0, 1)')
    i6 = Interval('(1, 2)')
    s = UISet([i5, i6])
    expected = [Interval('(-inf, 0]'), Interval('[1, 1]'), Interval('[2, inf)')]
    assert (~s).intervals == expected
    assert (~~s).intervals == s.intervals

    i7 = Interval('(-inf, 0)')
    s = UISet([i7])
    assert (~s).intervals == [Interval('[0, inf)')]
    assert (~~s).intervals == s.intervals

    i8 = Interval('[0, inf)')
    s = UISet([i8])
    assert (~s).intervals == [i7]
    assert (~~s).intervals == s.intervals

    assert i0 == Interval('(-inf, inf)')
    assert i1 == Interval('[1, 4]')
    assert i2 == Interval('[7, 9]')
    assert i3 == Interval('[5, 8]')
    assert i4 == Interval('[1, 6]')
    assert i5 == Interval('(0, 1)')
    assert i6 == Interval('(1, 2)')
    assert i7 == Interval('(-inf, 0)')
    assert i8 == Interval('[0, inf)')

