from uiset import Interval, UISet, inf, unbounded


def test_uiset_init():

    s = UISet()
    assert s.intervals == []

    s = UISet([])
    assert s.intervals == []

    s = UISet([unbounded])
    assert s.intervals[0] == unbounded
    assert s.intervals[0] is not unbounded

    i1 = Interval('[1, 4]')
    i2 = Interval('[7, 9]')
    s = UISet([i1, i2])
    assert s.intervals == [Interval('[1, 4]'), Interval('[7, 9]')]
    assert s.intervals[0] is not i1
    assert s.intervals[1] is not i2

    i1 = Interval('[7, 9]')
    i2 = Interval('[1, 4]')
    s = UISet([i1, i2])
    assert s.intervals == [Interval('[1, 4]'), Interval('[7, 9]')]
    assert s.intervals[0] is not i1
    assert s.intervals[1] is not i2

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
    assert s.intervals == [Interval('(-inf, 1)')]
    
    i5 = Interval('(1, 2)')
    s.add(i5)
    assert s.intervals == [Interval('(-inf, 1)'), Interval('(1, 2)')]

    s = UISet([i4])
    s.add(i3)
    assert s.intervals == [Interval('[-1, 1)')]

    i6 = Interval('[0, 1)')
    i7 = Interval('[-1, 0)')
    s = UISet([i6])
    s.add(i7)
    assert s.intervals == [Interval('[-1, 1)')]

    i8 = Interval('(0, 1)')
    i9 = Interval('(-1, 0)')
    s = UISet([i8])
    s.add(i9)
    assert s.intervals == [Interval('(-1, 0)'), Interval('(0, 1)')]

    # Make sure original intervals has not changed.
    assert i1 == Interval('(-inf, 0)')
    assert i2 == Interval('(-inf, 0)')
    assert i3 == Interval('[-1, 0]')
    assert i4 == Interval('(0, 1)')
    assert i5 == Interval('(1, 2)')
    assert i6 == Interval('[0, 1)')
    assert i7 == Interval('[-1, 0)')
    assert i8 == Interval('(0, 1)')
    assert i9 == Interval('(-1, 0)')


def test_uiset_bool():

    s = UISet()
    assert bool(s) is False

    s.add(Interval('[1, 2]'))
    assert bool(s) is True


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


def test_uiset_search():

    s = UISet()
    assert s.search(1) is None
    
    s = UISet([unbounded])
    assert s.search(1) == unbounded

    i1 = Interval('[0, 1]')
    i2 = Interval('(2, 3)')
    s = UISet([i1, i2])
    assert s.search(1) == i1
    assert s.search(2) is None
    assert s.search(2.5) == i2
    assert s.search(2.5, enumerated=True) == (1, i2)


def test_uiset_contains():

    s = UISet()
    assert 1 not in s

    s = UISet([unbounded])
    assert 1 in s

    i1 = Interval('[1, 3]')
    s = UISet([i1])
    assert 0 not in s
    assert 1 in s
    assert 2 in s
    assert 3 in s
    assert 4 not in s

    i2 = Interval('(5, 7)')
    s.add(i2)
    assert 0 not in s
    assert 1 in s
    assert 2 in s
    assert 3 in s
    assert 4 not in s
    assert 5 not in s
    assert 6 in s
    assert 7 not in s

    i3 = Interval('(7, inf)')
    s.add(i3)
    assert 0 not in s
    assert 1 in s
    assert 2 in s
    assert 3 in s
    assert 4 not in s
    assert 5 not in s
    assert 6 in s
    assert 7 not in s
    assert 100 in s
    assert inf not in s

    s = ~s
    assert 0 in s
    assert 1 not in s
    assert 2 not in s
    assert 3 not in s
    assert 4 in s
    assert 5 in s
    assert 6 not in s
    assert 7 in s
    assert 100 not in s
    assert inf not in s


def test_uiset_discard():

    s = UISet()
    i = Interval('[0, 2]')
    s.add(i)
    s.discard(0)
    assert s.intervals == [Interval('(0, 2]')]
    s.discard(2)
    assert s.intervals == [Interval('(0, 2)')]
    s.discard(1)
    s.discard(-1)
    assert s.intervals == [Interval('(0, 1)'), Interval('(1, 2)')]

    assert i == Interval('[0, 2]')

