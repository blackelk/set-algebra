import pytest

from set_algebra import Endpoint, Interval, Set, inf, unbounded


def test_set_init():

    s1 = Set()
    s2 = Set(s1)
    assert s1 == s2
    assert s1 is not s2

    s1 = Set([Interval('[1, 2]'), 3])
    s2 = Set(s1)
    assert s1 == s2
    assert s1 is not s2

    s = Set()
    assert s.pieces == []

    s = Set([])
    assert s.pieces == []

    s = Set([5])
    assert s.pieces == [5]
    s = Set([5, 7])
    assert s.pieces == [5, 7]

    s = Set(set())
    assert s.pieces == []
    s = Set({''})
    assert s.pieces == ['']

    s = Set([2, Interval('(4, 6)'), 5, 6, 8])
    assert s.pieces == [2, Interval('(4, 6]'), 8]

    s = Set([unbounded])
    assert s.pieces[0] == unbounded
    assert s.pieces[0] is not unbounded

    i1 = Interval('[1, 4]')
    i2 = Interval('[7, 9]')
    s = Set([i1, i2])
    assert s.pieces == [Interval('[1, 4]'), Interval('[7, 9]')]
    assert s.pieces[0] is not i1
    assert s.pieces[1] is not i2

    i1 = Interval('[7, 9]')
    i2 = Interval('[1, 4]')
    s = Set([i1, i2])
    assert s.pieces == [Interval('[1, 4]'), Interval('[7, 9]')]
    assert s.pieces[0] is not i1
    assert s.pieces[1] is not i2

    i1 = Interval('[1, 9]')
    i2 = Interval('[3, 5]')
    s = Set([i1, i2])
    assert s.pieces == [Interval('[1, 9]')]

    i1 = Interval('[3, 5]')
    i2 = Interval('[1, 9]')
    s = Set([i1, i2])
    assert s.pieces == [Interval('[1, 9]')]

    i1 = Interval('[1, 6]')
    i2 = Interval('[5, 8]')
    s = Set([i1, i2])
    assert s.pieces == [Interval('[1, 8]')]

    i1 = Interval('[5, 8]')
    i2 = Interval('[1, 6]')
    s = Set([i1, i2])
    assert s.pieces == [Interval('[1, 8]')]

    i1 = Interval('(0, 1)')
    i2 = Interval('(1, 2)')
    s = Set([i1, i2])
    assert s.pieces == [Interval('(0, 1)'), Interval('(1, 2)')]


def test_set_init_from_notation():

    s = Set('[1, 2]')
    assert s.pieces == [Interval('[1, 2]')]

    s = Set('[1, 2], (4, 5)')
    assert s.pieces == [Interval('[1, 2]'), Interval('(4, 5)')]

    s = Set('[1, 2], [5, inf)')
    assert s.pieces == [Interval('[1, 2]'), Interval('[5, inf)')]


def test_set_init_from_notation_raises():

    invalid_notations = [
        '',
        '1',
        ',',
        '[1',
        '[1,',
        '[1, [2',
        '[1, 3], [2, 4]',
        '[1, 2], (2, 3)',
        '[1, 2), [2, 3)',
        '{1}, (1, 2)',
        '{1}, [1, 2)',
        '(1)',
        '[1)',
        '[1]',
        '{inf}',
        '{2}, (1, 3)',
        '{5}, (1, 3)',
        '(1, 3), {3}',
        '(1, 3], {3}',
        '(1, 3], {2}',
        '[2, [3]',
        '[2, {3}',
        '{2',
        '2}',
        '[2, 3, 4]',
        '{2, 3, 4}',
    ]

    for notation in invalid_notations:
        with pytest.raises(ValueError):
            s = Set(notation)


def test_set_repr():

    s = Set()
    assert repr(s) == 'Set([])'

    s = Set([Interval('[1, 2.5)'), Interval('(2.5, 4]'), Interval('[7, 9]')])
    assert eval(repr(s)).pieces == s.pieces

    s = Set([1, 2, 3])
    assert eval(repr(s)).pieces == s.pieces

    s = Set([1, Interval('(2, 3)')])
    assert eval(repr(s)).pieces == s.pieces


def test_set_notation():

    s = Set()
    assert s.notation == ''

    s = Set([0])
    assert s.notation == '{0}'

    s = Set([Interval('(-inf, 0)')])
    assert s.notation == '(-inf, 0)'

    s = Set([Interval('(-inf, 0)'), Interval('[1, 2]')])
    assert s.notation == '(-inf, 0), [1, 2]'

    s = Set([Interval('(-inf, 0)'), Interval('[1, 2]'), 4])
    assert s.notation == '(-inf, 0), [1, 2], {4}'


def test_set_add():

    s = Set()
    i1 = Interval('(-inf, 0)')
    s.add(i1)
    assert s.pieces == [i1]

    i2 = Interval('(-inf, 0)')
    s.add(i2)
    assert s.pieces == [i1]

    i3 = Interval('[-1, 0]')
    s.add(i3)
    assert s.pieces == [Interval('(-inf, 0]')]

    i4 = Interval('(0, 1)')
    s.add(i4)
    assert s.pieces == [Interval('(-inf, 1)')]

    i5 = Interval('(1, 2)')
    s.add(i5)
    assert s.pieces == [Interval('(-inf, 1)'), Interval('(1, 2)')]

    s = Set([i4])
    s.add(i3)
    assert s.pieces == [Interval('[-1, 1)')]

    i6 = Interval('[0, 1)')
    i7 = Interval('[-1, 0)')
    s = Set([i6])
    s.add(i7)
    assert s.pieces == [Interval('[-1, 1)')]

    i8 = Interval('(0, 1)')
    i9 = Interval('(-1, 0)')
    s = Set([i8])
    s.add(i9)
    assert s.pieces == [Interval('(-1, 0)'), Interval('(0, 1)')]

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

    # Bulk test 1
    s0 = Set('(4, 7)')
    tests = [
        ('(1, 2)', '(1, 2), (4, 7)'),
        ('(1, 4)', '(1, 4), (4, 7)'),
        ('(1, 4]', '(1, 7)'),
        ('(1, 5]', '(1, 7)'),
        ('(1, 7)', '(1, 7)'),
        ('(1, 7]', '(1, 7]'),
        ('(1, 8]', '(1, 8]'),
        ('(5, 6]', '(4, 7)'),
        ('(5, 7)', '(4, 7)'),
        ('(5, 7]', '(4, 7]'),
        ('(5, 8]', '(4, 8]'),
        ('(7, 9)', '(4, 7), (7, 9)'),
        ('[7, 9]', '(4, 9]'),
        ('[8, 9]', '(4, 7), [8, 9]'),
    ]

    for i_notation, res_notation in tests:
        s = s0.copy()
        interval = Interval(i_notation)
        s.add(interval)
        assert s.notation == res_notation

    # Bulk test 2
    s0 = Set('(0, 4), (6, 8), (9, 10), (12, 15)')

    tests = [
        ('(-inf, -1]', '(-inf, -1], (0, 4), (6, 8), (9, 10), (12, 15)'),
        ('(-inf, 0)', '(-inf, 0), (0, 4), (6, 8), (9, 10), (12, 15)'),
        ('(-inf, 0]', '(-inf, 4), (6, 8), (9, 10), (12, 15)'),
        ('(-inf, 1)', '(-inf, 4), (6, 8), (9, 10), (12, 15)'),
        ('(-inf, 4)', '(-inf, 4), (6, 8), (9, 10), (12, 15)'),
        ('(-inf, 4]', '(-inf, 4], (6, 8), (9, 10), (12, 15)'),
        ('(-inf, 5]', '(-inf, 5], (6, 8), (9, 10), (12, 15)'),
        ('(-inf, 6)', '(-inf, 6), (6, 8), (9, 10), (12, 15)'),
        ('(-inf, 6]', '(-inf, 8), (9, 10), (12, 15)'),
        ('(-inf, 7]', '(-inf, 8), (9, 10), (12, 15)'),
        ('(-inf, 8)', '(-inf, 8), (9, 10), (12, 15)'),
        ('(-inf, 8]', '(-inf, 8], (9, 10), (12, 15)'),
        ('(-inf, 13]', '(-inf, 15)'),
        ('(-inf, inf)', '(-inf, inf)'),
        ('[0, 1)', '[0, 4), (6, 8), (9, 10), (12, 15)'),
        ('(0, 1)', '(0, 4), (6, 8), (9, 10), (12, 15)'),
        ('[0, 4)', '[0, 4), (6, 8), (9, 10), (12, 15)'),
        ('(0, 4)', '(0, 4), (6, 8), (9, 10), (12, 15)'),
        ('[0, 4]', '[0, 4], (6, 8), (9, 10), (12, 15)'),
        ('(0, 4]', '(0, 4], (6, 8), (9, 10), (12, 15)'),
        ('[0, 5]', '[0, 5], (6, 8), (9, 10), (12, 15)'),
        ('(0, 5]', '(0, 5], (6, 8), (9, 10), (12, 15)'),
        ('[0, 6)', '[0, 6), (6, 8), (9, 10), (12, 15)'),
        ('(0, 6)', '(0, 6), (6, 8), (9, 10), (12, 15)'),
        ('[0, 6]', '[0, 8), (9, 10), (12, 15)'),
        ('(0, 6]', '(0, 8), (9, 10), (12, 15)'),
        ('[0, 13]', '[0, 15)'),
        ('(0, 13]', '(0, 15)'),
        ('(1, 2)', '(0, 4), (6, 8), (9, 10), (12, 15)'),
        ('(1, 4)', '(0, 4), (6, 8), (9, 10), (12, 15)'),
        ('(1, 4]', '(0, 4], (6, 8), (9, 10), (12, 15)'),
        ('(1, 5]', '(0, 5], (6, 8), (9, 10), (12, 15)'),
        ('(1, 7)', '(0, 8), (9, 10), (12, 15)'),
        ('(4, 5)', '(0, 4), (4, 5), (6, 8), (9, 10), (12, 15)'),
        ('[4, 5)', '(0, 5), (6, 8), (9, 10), (12, 15)'),
        ('(4, 6)', '(0, 4), (4, 6), (6, 8), (9, 10), (12, 15)'),
        ('[4, 6]', '(0, 8), (9, 10), (12, 15)'),
        ('(15, 16)', '(0, 4), (6, 8), (9, 10), (12, 15), (15, 16)'),
        ('[15, 16)', '(0, 4), (6, 8), (9, 10), (12, 16)'),
    ]

    for i_notation, res_notation in tests:
        s = s0.copy()
        interval = Interval(i_notation)
        s.add(interval)
        assert s.notation == res_notation


def test_set_bool():

    s = Set()
    assert bool(s) is False

    s.add(1)
    assert bool(s) is True

    s = Set('[1, 2]')
    assert bool(s) is True


def test_set_invert():

    i0 = Interval('(-inf, inf)')
    s = Set([i0])
    assert (~s).pieces == []
    assert (~~s).pieces == s.pieces

    s = Set()
    assert (~s).pieces == [i0]
    assert (~~s).pieces == s.pieces

    i1 = Interval('[1, 4]')
    i2 = Interval('[7, 9]')
    s = Set([i1, i2])
    expected = [Interval('(-inf, 1)'), Interval('(4, 7)'), Interval('(9, inf)')]
    assert (~s).pieces == expected
    assert (~~s).pieces == s.pieces

    i3 = Interval('[5, 8]')
    i4 = Interval('[1, 6]')
    s = Set([i3, i4])
    assert (~s).pieces == [Interval('(-inf, 1)'), Interval('(8, inf)')]
    assert (~~s).pieces == s.pieces

    i5 = Interval('(0, 1)')
    i6 = Interval('(1, 2)')
    s = Set([i5, i6])
    expected = [Interval('(-inf, 0]'), 1, Interval('[2, inf)')]
    assert (~s).pieces == expected
    assert (~~s).pieces == s.pieces

    i7 = Interval('(-inf, 0)')
    s = Set([i7])
    assert (~s).pieces == [Interval('[0, inf)')]
    assert (~~s).pieces == s.pieces

    i8 = Interval('[0, inf)')
    s = Set([i8])
    assert (~s).pieces == [i7]
    assert (~~s).pieces == s.pieces

    i9 = Interval('(0, inf)')
    s = Set([i7, i9])
    assert (~s).pieces == [0]

    Set('(-inf, 0), (0, inf)')
    assert i0 == Interval('(-inf, inf)')
    assert i1 == Interval('[1, 4]')
    assert i2 == Interval('[7, 9]')
    assert i3 == Interval('[5, 8]')
    assert i4 == Interval('[1, 6]')
    assert i5 == Interval('(0, 1)')
    assert i6 == Interval('(1, 2)')
    assert i7 == Interval('(-inf, 0)')
    assert i8 == Interval('[0, inf)')
    assert i9 == Interval('(0, inf)')

    s = Set([0])
    assert (~s).pieces == [Interval('(-inf, 0)'), Interval('(0, inf)')]
    s = Set([0, 1])
    assert (~s).pieces == [Interval('(-inf, 0)'), Interval('(0, 1)'), Interval('(1, inf)')]

    i1 = Interval('(-inf, 1]')
    i2 = Interval('(1, 2]')
    i3 = Interval('(2, 3)')
    i4 = Interval('(3, inf)')
    s = Set([i2, 3])
    assert (~s).pieces == [i1, i3, i4]
    s = Set([i1, 3])
    assert (~s).pieces == [Interval('(1, 3)'), i4]
    s = Set([0, i2])
    assert (~s).pieces == [Interval('(-inf, 0)'), Interval('(0, 1]'), Interval('(2, inf)')]
    assert i1 == Interval('(-inf, 1]')
    assert i2 == Interval('(1, 2]')
    assert i3 == Interval('(2, 3)')
    assert i4 == Interval('(3, inf)')


def test_set_search():

    s = Set()
    assert s.search(1) == (0, None)

    s = Set('{1}')
    assert s.search(0) == (0, None)
    assert s.search(1) == (0, 1)
    assert s.search(2) == (1, None)

    s = Set([unbounded])
    assert s.search(1) == (0, unbounded)
    assert s.search(float('-inf')) == (0, None)
    assert s.search(float('inf')) == (1, None)

    i1 = Interval('[0, 1]')
    i2 = Interval('(2, 3)')
    s = Set([i1, i2])
    assert s.search(-1) == (0, None)
    assert s.search(0) == (0, i1)
    assert s.search(1) == (0, i1)
    assert s.search(2) == (1, None)
    assert s.search(2.5) == (1, i2)
    assert s.search(1, lo=1) == (1, None)
    assert s.search(2.5, hi=1) == (1, None)
    assert s.search(2.5, lo=1) == (1, i2)

    assert s.search(i1.a) == (0, i1)
    assert s.search(i1.b) == (0, i1)
    assert s.search(i2.a) == (1, i2)
    assert s.search(i2.b) == (1, i2)

    i1 = Interval('(1, 3)')
    i2 = Interval('[7, 8]')
    s = Set([i1, 5, i2])
    assert s.search(0) == (0, None)
    assert s.search(1) == (0, None)
    assert s.search(2) == (0, i1)
    assert s.search(3) == (1, None)
    assert s.search(4) == (1, None)
    assert s.search(5) == (1, 5)
    assert s.search(6) == (2, None)
    assert s.search(7) == (2, i2)
    assert s.search(8) == (2, i2)
    assert s.search(9) == (3, None)


def test_set_contains_scalar():

    s = Set()
    assert 1 not in s

    s = Set([unbounded])
    assert 1 in s

    i1 = Interval('[1, 3]')
    s = Set([i1])
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


def test_set_contains_interval():

    s = Set()
    assert Interval('(1, 2)') not in s

    s = Set('(1, 4)')
    assert Interval('(2, 3)') in s
    assert Interval('[1, 4)') not in s
    assert Interval('(1, 4]') not in s
    assert Interval('[1, 4]') not in s
    assert Interval('(0, 2)') not in s
    assert Interval('(3, 5)') not in s
    assert Interval('(0, 1)') not in s

    s = Set('[1, 4)')
    assert Interval('(2, 3)') in s
    assert Interval('[1, 4)') in s
    assert Interval('(1, 4]') not in s
    assert Interval('[1, 4]') not in s
    assert Interval('(0, 2)') not in s
    assert Interval('(3, 5)') not in s

    s = Set('(1, 4]')
    assert Interval('(2, 3)') in s
    assert Interval('[1, 4)') not in s
    assert Interval('(1, 4]') in s
    assert Interval('[1, 4]') not in s
    assert Interval('(0, 2)') not in s
    assert Interval('(3, 5)') not in s

    s = Set('[1, 4]')
    assert Interval('(2, 3)') in s
    assert Interval('[1, 4)') in s
    assert Interval('(1, 4]') in s
    assert Interval('[1, 4]') in s
    assert Interval('(0, 2)') not in s
    assert Interval('(3, 5)') not in s


def test_set_eq_and_ne():

    s1 = Set()
    s2 = Set()
    assert s1 == s2
    s1.add(Interval('[1, 2]'))
    assert s1 != s2

    s2 = Set([Interval('[1, 2]')])
    assert s1 == s2

    s2.remove(2)
    assert s1 != s2

    assert not s1 == 0
    assert s1 != 0

    s1 = Set('{1}')
    s2 = Set('{1}')
    assert s1 == s2
    s2 = Set('{2}')
    assert s1 != s2


def test_set_remove():

    i1 = Interval('[0, 2]')
    s = Set([i1])
    s.remove(0)
    assert s.pieces == [Interval('(0, 2]')]
    s.remove(2)
    assert s.pieces == [Interval('(0, 2)')]
    s.remove(1)
    s.remove(-1)
    assert s.pieces == [Interval('(0, 1)'), Interval('(1, 2)')]
    i2 = Interval('[2, inf)')
    s.add(i2)
    s.remove(inf)
    assert s.pieces == [Interval('(0, 1)'), Interval('(1, inf)')]

    assert i1 == Interval('[0, 2]')
    assert i2 == Interval('[2, inf)')


def test_set_clear():

    i1 = Interval('[0, 1]')
    i2 = Interval('[2, 3]')
    s = Set([i1, i2])
    s.clear()
    assert s.pieces == []


def test_set_copy():

    s1 = Set()
    s2 = s1.copy()
    assert s1 == s2
    assert s1 is not s2

    s1 = Set('{4}, {8}')
    s2 = s1.copy()
    assert s2.pieces == [4, 8]

    i = Interval('[1, 2]')
    s1 = Set([i])
    s2 = s1.copy()
    assert s1 == s2
    assert s2.pieces[0] is not i

    l1 = [1, 2, 3]
    l2 = [4, 5, 6]
    a = Endpoint(l1, '(')
    b = Endpoint(l2, ')')
    i = Interval(a, b)
    s1 = Set([i])
    s2 = s1.copy()
    s2.pieces[0].a.value[2] = -1
    assert i.a.value[2] == -1


def test_set_ge():

    s = Set()
    assert s >= Set()
    assert not s >= Set('{1}')
    assert not s >= Set('[1, 2]')

    s = Set('{3}, {5}')
    assert s >= Set()
    assert s >= Set('{3}')
    assert s >= Set('{5}')
    assert s >= Set('{3}, {5}')
    assert not s >= Set('{3}, {4}')
    assert not s >= Set('(3, 5)')
    assert not s >= Set('[3, 5]')

    s = Set('(1, 6)')
    assert s >= Set()
    assert not s >= Set('{0}')
    assert not s >= Set('{1}')
    assert s >= Set('{3}')
    assert s >= Set('{2}, {3}, {4}')
    assert not s >= Set('{6}')
    assert not s >= Set('[5, 6]')
    assert not s >= Set('{7}')
    assert s >= Set('(2, 3)')
    assert s >= Set('(2, 3), {4}')
    assert s >= Set('(2, 3), (4, 5)')
    assert s >= Set('(1, 3), (4, 6)')
    assert s >= Set('(1, 6)')
    assert not s >= Set('(4, 6]')
    assert not s >= Set('{3}, (4, 6]')
    assert not s >= Set('(1, 6]')
    assert not s >= Set('[1, 6)')
    assert not s >= Set('[1, 6]')
    assert not s >= Set('[2, 7]')

    s = Set('(2, 4), (4, 6)')
    assert s >= Set('(2, 4), (4, 6)')
    assert s >= Set('(2, 3), (3, 4), (4, 6)')
    assert s >= Set('{3}, {5}')
    assert not s >= Set('(1, 3)')
    assert not s >= Set('(3, 5)')
    assert not s >= Set('(5, 7)')

    s = Set('[1, 2]')
    assert s >= Set('{1}')
    assert s >= Set('{2}')
    assert not s >= Set('{3}')
    assert s >= Set('(1, 2)')
    assert s >= Set('[1, 2]')

    s = Set('[1, inf)')
    assert s >= Set('{1}')
    assert s >= Set('[1, 10]')
    assert not s >= Set('(0, 10]')

    with pytest.raises(TypeError):
        Set() >= 0
        Set() >= -inf
    inf >= Set()


def test_set_le():

    s = Set()
    assert s <= Set()
    assert s <= Set('{1}')
    assert s <= Set('[1, 2]')

    s = Set('(1, 6)')
    assert not s <= Set()
    assert not s <= Set('{3}')
    assert not s <= Set('(2, 3)')
    assert not s <= Set('(2, 3), (4, 5)')
    assert not s <= Set('(1, 3), (4, 6)')
    assert s <= Set('(1, 6)')
    assert not s <= Set('(4, 6]')
    assert not s <= Set('{1}')
    assert s <= Set('(1, 6]')
    assert s <= Set('[1, 6)')
    assert s <= Set('[1, 6]')
    assert not s <= Set('[2, 7]')

    s = Set('(2, 4), (4, 6)')
    assert s <= Set('(2, 4), (4, 6)')
    assert not s <= Set('(2, 3), (3, 4), (4, 6)')
    assert not s <= Set('(1, 3)')
    assert not s <= Set('(3, 5)')
    assert not s <= Set('(5, 7)')

    s = Set('[1, 2]')
    assert not s <= Set('(1, 2)')
    assert s <= Set('[1, 2]')

    s = Set('[1, inf)')
    assert not s <= Set('[1, 10]')
    assert not s <= Set('(0, 10]')

    with pytest.raises(TypeError):
        Set() <= 0


def test_set_issuperset():

    assert Set('[1, 3]').issuperset(Set('(1, 3)'))
    assert Set('[1, 3]').issuperset(Set('{1}, {2}, {3}'))
    assert not Set().issuperset(Set('(1, 3)'))

    assert Set('[1, 3]').issuperset('(1, 2), {3}')
    assert Set('[1, 3]').issuperset([])
    assert not Set('[1, 3]').issuperset([0])

    assert Set.issuperset(Set('(0, 8)'), [2, 3, Interval('[3, 5]'), 6])


def test_set_issubset():

    assert not Set('[1, 3]').issubset(Set('(1, 3)'))
    assert Set().issubset(Set('{1}'))
    assert Set().issubset(Set('(1, 3)'))

    assert Set('{1}').issubset('(0, 2)')
    assert not Set('{1}, {2}').issubset([1, 3])

    assert Set.issubset(Set('(-2, -1)'), [Interval('(-inf, 0)')])


def test_set_gt():

    assert not Set() > Set()
    assert not Set() > Set('{1}')
    assert Set('{1}') > Set()
    assert not Set('{1}') > Set('{1}')
    assert not Set('{1}') > Set('{2}')
    s1 = Set('(1, 2)')
    s2 = Set('[1, 2)')
    s3 = Set('(1, 2]')
    s4 = Set('[1, 2]')
    assert not s1 > s1
    assert not s1 > s2
    assert not s1 > s3
    assert not s1 > s4
    assert s2 > s1
    assert not s2 > s3
    assert not s2 > s4
    assert s3 > s1
    assert not s3 > s2
    assert not s3 > s4
    assert s4 > s1
    assert s4 > s2
    assert s4 > s3

    s1 = Set('(1, 2), {4}')
    s2 = Set('(1, 2)')
    assert s1 > s2
    assert not s2 > s1

    s = Set('(1, 4)')
    assert s > Set('{2}')
    assert s > Set('{2}, {3}')
    assert not s > Set('{0}')
    assert not s > Set('{1}')
    assert not s > Set('{4}')
    assert not s > Set('{5}')
    assert s > Set('(1, 3)')
    assert s > Set('(2, 3)')
    assert s > Set('(2, 4)')

    s = Set('(-inf, inf)')
    assert s > Set('[1, 2], (3, inf)')
    assert not s > Set('(-inf, inf)')

    with pytest.raises(TypeError):
        Set('(1, 2)') > Interval('(1, 2)')
        Set('(1, 2)') > 0


def test_set_lt():

    assert not Set() < Set()
    assert Set() < Set('{3}')
    assert Set() < Set('(1, 2)')
    assert not Set('{0}') < Set('(1, 2)')
    assert Set('{1}') < Set('{1}, {2}')

    with pytest.raises(TypeError):
        Set() < 5


def test_set_or():

    s1 = Set()
    s2 = Set()
    assert s1 | s2 == Set()

    s1 = Set()
    s2 = Set('{3}')
    assert s2 | s2 == s2
    assert s1 | s2 == s2 | s1 == s2

    s1 = Set('(1, 2)')
    s2 = Set('[2, 3]')
    assert s1 | s2 == s2 | s1 == Set('(1, 3]')

    s1 = Set('(1, 2)')
    s2 = Set('{2}')
    assert s1 | s2 == s2 | s1 == Set('(1, 2]')

    s1 = Set('(1, 3), (3, 5), (5, 7)')
    s2 = Set('{3}, {5}')
    assert s1 | s2 == s2 | s1 == Set('(1, 7)')

    s1 = Set('(-inf, 0), {2}, [4, 6], (9, 12]')
    s2 = Set('(-inf, 0], (2, 3), {5}, (7, 8), {9}, (20, inf)')
    expected = Set('(-inf, 0], [2, 3), [4, 6], (7, 8), [9, 12], (20, inf)')
    assert s1 | s2 == s2 | s1 == expected
    assert s1 == Set('(-inf, 0), {2}, [4, 6], (9, 12]')
    assert s2 == Set('(-inf, 0], (2, 3), {5}, (7, 8), {9}, (20, inf)')

    with pytest.raises(TypeError):
        Set() | 0


def test_set_ior():

    s1 = Set()
    s2 = Set()
    s1 |= s2
    assert s1 == Set()

    s1 = Set()
    s2 = Set('{3}')
    s1 |= s2
    s2 |= s1
    assert s1 == s2 == Set('{3}')

    s1 = Set('(1, 2)')
    s2 = Set('{1}')
    s1 |= s2
    s2 |= s1
    assert s1 == s2 == Set('[1, 2)')

    s1 = Set('(1, 2)')
    s2 = Set('(2, 3)')
    s1 |= s2
    s2 |= s1
    assert s1 == s2 == Set('(1, 2), (2, 3)')
    s1 |= s1
    assert s1 == Set('(1, 2), (2, 3)')

    with pytest.raises(TypeError):
        s1 |= 0


def test_set_union():

    s1 = Set()
    s2 = Set()
    s3 = Set()
    assert s1.union(s2, s3) == Set()

    s1 = Set('{1}')
    s2 = Set('{3}')
    s3 = Set('{2}')
    assert s1.union(s2, s3) == Set('{1}, {2}, {3}')
    assert s1 == Set('{1}')
    assert s2 == Set('{3}')
    assert s3 == Set('{2}')

    s1 = Set('(3, 4)')
    s2 = Set('[2, 3]')
    s3 = Set('[4, 5]')
    assert s1.union(s2, s3) == s2.union(s1, s3) == s3.union(s1, s2) == Set('[2, 5]')
    assert s1.union(s1, s1, s3, s2, s3, s1, s2, s3) == Set('[2, 5]')
    assert Set.union(s1) == s1
    assert Set.union(s1, s2, s3) == Set('[2, 5]')
    assert s1 == Set('(3, 4)')
    assert s2 == Set('[2, 3]')
    assert s3 == Set('[4, 5]')

    i1 = Interval('(-inf, 0)')
    i2 = Interval('(-10, 2)')
    s1 = Set('(-inf, -5)')
    s2 = Set('{5}')
    assert s1.union(s2, [i1, i2], [4, i1], []) == Set('(-inf, 2), {4}, {5}')


def test_set_update():

    s1 = Set()
    s2 = Set()
    s3 = Set()
    s1.update(s2, s3)
    assert s1 == Set()

    s1 = Set('{1}')
    s2 = Set('{3}')
    s3 = Set('{2}')
    s1.update(s2, s3)
    assert s1 == Set('{1}, {2}, {3}')
    assert s2 == Set('{3}')
    assert s3 == Set('{2}')

    s1 = Set('(3, 4)')
    s2 = Set('[2, 3]')
    s3 = Set('[4, 5]')
    s1.update(s1, s2, s1, s3, s2, s3, s1, s2, s3)
    assert s1 == Set('[2, 5]')
    assert s2 == Set('[2, 3]')
    assert s3 == Set('[4, 5]')


def test_set_sub():

    s0 = Set()
    s1 = Set('{1}')
    s2 = Set('{1}, {2}')
    s3 = Set('[1, 2]')
    assert s0 - s0 == s0
    assert s1 - s0 == s1
    assert s0 - s1 == s0
    assert s2 - s1 == Set('{2}')
    assert s0 == Set()
    assert s1 == Set('{1}')
    assert s2 == Set('{1}, {2}')
    assert s3 == Set('[1, 2]')
    assert s3 - s1 == Set('(1, 2]')
    assert s3 - s2 == Set('(1, 2)')
    assert s3 - s3 == s0

    s1 = Set('(1, 4)')
    s2 = Set('{1}, {2}, {3}, {4}')
    assert s1 - s2 == Set('(1, 2), (2, 3), (3, 4)')
    assert s2 - s1 == Set('{1}, {4}')

    s1 = Set('(-inf, 0), {2}, [4, 6], [8, 20]')
    s2 = Set('{-3}, {2}, (4, 9), [10, 11], {15}, {20}')
    assert s1 - s2 == Set('(-inf, -3), (-3, 0), {4}, [9, 10), (11, 15), (15, 20)')
    assert s2 - s1 == Set('(6, 8)')

    s1 = Set('(-757, -742), [-541, -539], (-365, -329], [-310, 7], (10, 314], (426, 541), [627, 831), (884, 961]')
    s2 = Set('[-750, -724], [-635, -580], (-552, -257], [-239, -195), (-107, 46), (320, 356), [624, 680), [726, 794], (810, 860)')
    assert s1 - s2 == Set('(-757, -750), (-257, -239), [-195, -107], [46, 314], (426, 541), [680, 726), (794, 810], (884, 961]')

    s1 = Set('[-818, -805], [-793, -624], [-548, -520], [-453, -369), (-312, -221), [-72, 321], [503, 657], (684, 712], [715, 891)')
    s2 = Set('[-971, -924), (-816, -150), [6, 47], [237, 603)')
    assert s1 - s2 == Set('[-818, -816], [-72, 6), (47, 237), [603, 657], (684, 712], [715, 891)')

    with pytest.raises(TypeError):
        Set() - 0


def test_set_isub():

    s = Set()
    s -= s
    assert s == Set()

    s = Set('(-inf, inf)')
    s -= Set('{0}')
    assert s == Set('(-inf, 0), (0, inf)')
    s -= Set('{0}, {1}')
    assert s == Set('(-inf, 0), (0, 1), (1, inf)')
    s -= Set('(-inf, -2), (0, 1), (2, inf)')
    assert s == Set('[-2, 0), (1, 2]')
    s -= Set('{0}, {1}')
    assert s == Set('[-2, 0), (1, 2]')
    s -= Set('(-2, 2)')
    assert s == Set('{-2}, {2}')
    s -= s.copy()
    assert s == Set()

    with pytest.raises(TypeError):
        s -= 5


def test_set_difference():

    s = Set()
    assert s.difference(s) == s

    s = Set('[1, 3], [4, 5], [6, 7], [8, 10]')
    s = s.difference(Set('(2, 9)'), Set())
    assert s == Set('[1, 2], [9, 10]')
    s = s.difference(Set('{1}, {2}, {3}'), Set('{4}'), Set('{8}, {9}, {10}'))
    assert s == Set('(1, 2), (9, 10)')

    s = Set('(-inf, 0), {1}, {2}, [5, 9]')
    s = s.difference([Interval('(-inf, 3)'), 4, Interval('(5, 6)')], Set())
    assert s == Set('{5}, [6, 9]')

    s = Set('[1, 3], {4}, [5, 7], {8}, (10, inf)')
    expected = Set('[2, 3], {4}, (5, 6), (6, 7), (10, inf)')
    assert s.difference([6], [8, 5, 7], Set('(-inf, 2)')) == expected

    assert Set.difference(Set('[1, 3]'), Set('[2, 4]')) == Set('[1, 2)')


def test_set_difference_update():

    s = Set()
    s.difference_update(s, s)
    assert s == s

    s = Set('{1}, {2}, {3}, (4, 6), [8, 9]')
    s.difference_update([Interval('[1, 4]'), 5], Set('{2}, (8, 9)'))
    assert s == Set('(4, 5), (5, 6), {8}, {9}')
    s.difference_update(~s)
    assert s == Set('(4, 5), (5, 6), {8}, {9}')


def test_set_and():

    s1 = Set()
    s2 = Set()
    assert s1 & s2 == s2 & s1 == Set()

    s1 = Set('[0, 3]')
    s2 = Set('(1, 2)')
    assert s1 & s2 == s2 & s1 == Set('(1, 2)')

    s1 = Set('{0}, {1}, {2}')
    s2 = Set('(0, 2)')
    assert s1 & s2 == s2 & s1 == Set([1])
    assert s1 == Set('{0}, {1}, {2}')
    assert s2 == Set('(0, 2)')

    with pytest.raises(TypeError):
        s1 & 0


def test_set_iand():

    s1 = Set()
    s2 = Set('[0, 1]')
    s1 &= s2
    assert s1 == Set()
    assert s2 == Set('[0, 1]')

    s1 = Set('(0, 2), {3}, [4, 5]')
    s2 = Set('(1, 5)')
    s1 &= s2
    assert s1 == Set('(1, 2), {3}, [4, 5)')
    assert s2 == Set('(1, 5)')

    s1 = Set('[0, 1], [3, 4], [5, 6]')
    s1_id = id(s1)
    s2 = Set('{0}, (3, 4), [5, 7), {8}')
    s1 &= s2
    assert s1 == Set('{0}, (3, 4), [5, 6]')
    assert id(s1) == s1_id

    with pytest.raises(TypeError):
        s1 &= '[0, 1]'


def test_set_intersection():

    s1 = Set('{0}, (1, 2), [3, 6]')
    s2 = Set('[0, 3], [4, 6]')
    s3 = Set('(-inf, 6)')
    assert s1.intersection(s2, s3) == Set('{0}, (1, 2), {3}, [4, 6)')
    assert s1 == Set('{0}, (1, 2), [3, 6]')
    assert s2 == Set('[0, 3], [4, 6]')
    assert s3 == Set('(-inf, 6)')

    s1 = Set('[0, 2], [3, 4], (6, inf)')
    s2 = Set('(0, 7), {8}')
    i1 = Interval('(1, 4)')
    i2 = Interval('[2, 3]')
    assert s1.intersection(s1, s2, [i1, i2]) == Set('(1, 2], [3, 4)')
    assert s1.intersection(s1, s2, [i1], [i2]) == Set([2, 3])
    assert s1 == Set('[0, 2], [3, 4], (6, inf)')
    assert s2 == Set('(0, 7), {8}')
    assert i1 == Interval('(1, 4)')
    assert i2 == Interval('[2, 3]')


def test_set_intersection_update():

    s1 = Set('(-inf, inf)')
    s1_id = id(s1)
    s2 = Set('[0, inf)')
    s3 = Set('(-inf, 2), [3, 5), {6}, (7, 8), (9, inf)')
    i1 = Interval('[2, 3]')
    i2 = Interval('(4, 8)')
    i3 = Interval('[9, inf)')
    s1.intersection_update(s1, s2, s3, [i2, i1, i3])
    assert s1 == Set('{3}, (4, 5), {6}, (7, 8), (9, inf)')

    s1.intersection_update(range(11))
    assert s1 == Set([3, 6, 10])

    assert id(s1) == s1_id

    assert s2 == Set('[0, inf)')
    assert s3 == Set('(-inf, 2), [3, 5), {6}, (7, 8), (9, inf)')
    assert i1 == Interval('[2, 3]')
    assert i2 == Interval('(4, 8)')
    assert i3 == Interval('[9, inf)')


def test_set_xor():

    s1 = Set()
    s2 = Set()
    assert s1 ^ s2 == s2 ^ s1 == Set()

    s1 = Set('[0, 3]')
    s2 = Set('(1, 2)')
    assert s1 ^ s2 == s2 ^ s1 == Set('[0, 1], [2, 3]')

    s1 = Set('{0}, {1}, {2}')
    s2 = Set('(0, 2)')
    assert s1 ^ s2 == s2 ^ s1 == Set('[0, 1), (1, 2]')
    assert s1 == Set('{0}, {1}, {2}')
    assert s2 == Set('(0, 2)')

    with pytest.raises(TypeError):
        s1 ^ 0


def test_set_ixor():

    s1 = Set()
    s1_id = id(s1)
    s2 = Set('[0, 1]')
    s1 ^= s2
    assert s1 == s2
    assert s2 == Set('[0, 1]')

    s3 = Set('{0}, {1}')
    s1 ^= s3
    assert s1 == Set('(0, 1)')
    assert s3 == Set('{0}, {1}')

    s4 = Set('[1, 2]')
    s1 ^= s4
    assert s1 == Set('(0, 2]')
    assert s4 == Set('[1, 2]')

    assert id(s1) == s1_id

    with pytest.raises(TypeError):
        s1 ^= '[0, 1]'


def test_set_symmetric_difference():

    s1 = Set([1, 2, 3])
    s2 = Set([2, 3])
    assert s1.symmetric_difference(s2) == Set('{1}')
    assert s2.symmetric_difference(s1) == Set('{1}')
    assert s2 == Set([2, 3])

    s3 = Set('[1, 3]')
    assert s1.symmetric_difference(s3) == Set('(1, 2), (2, 3)')
    assert s3.symmetric_difference(s1) == Set('(1, 2), (2, 3)')

    assert s1.symmetric_difference([1]) == Set([2, 3])
    assert s1.symmetric_difference([1], [2, 3]) == Set()

    assert s1 == Set([1, 2, 3])


def test_set_symmetric_difference_update():

    s1 = Set([1, 2, 3])
    s1_id = id(s1)
    s2 = Set()
    s1.symmetric_difference_update(s2)
    assert s1 == Set([1, 2, 3])
    assert s2 == Set()

    s2 = Set([2, 3])
    s1.symmetric_difference_update(s2)
    assert s1 == Set([1])
    assert s2 == Set([2, 3])

    s2 = Set('(0, 1), (1, 2), (2, 3)')
    s1.symmetric_difference_update(s2)
    assert s1 == Set('(0, 2), (2, 3)')
    assert s2 == Set('(0, 1), (1, 2), (2, 3)')

    i1 = Interval('[1, 3]')
    i2 = Interval('[4, 5]')
    s1.symmetric_difference_update([i1, i2], Set())
    assert s1 == Set('(0, 1), {2}, {3}, [4, 5]')
    assert i1 == Interval('[1, 3]')
    assert i2 == Interval('[4, 5]')

    assert id(s1) == s1_id
