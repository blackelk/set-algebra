import pytest
from uiset import Endpoint, Interval, UISet, inf, unbounded


def do_bulk_tests(tests, fn, mode):

    for test in tests:
        arg, x, expected = test
        if isinstance(arg, list):
            s = UISet()
            pieces_copy = []
            for a in arg:
                pieces_copy.append(a.copy() if isinstance(a, Interval) else a)
            s.pieces = pieces_copy
        elif isinstance(arg, str):
            s = UISet(arg)
        elif isinstance(arg, UISet):
            s = arg.copy()
        else:
            assert False
        res = fn(s, x)
        if mode == 'return':
            assert res == expected
        elif mode == 'pieces':
            assert s.pieces == expected
        else:
            raise ValueError('Invalid mode')


def test_uiset_init():

    s1 = UISet()
    s2 = UISet(s1)
    assert s1 == s2
    assert s1 is not s2

    s1 = UISet([Interval('[1, 2]')])
    s2 = UISet(s1)
    assert s1 == s2
    assert s1 is not s2

    s = UISet()
    assert s.pieces == []

    s = UISet([])
    assert s.pieces == []

    s = UISet([5])
    assert s.pieces == [5]
    s = UISet([5, 7])
    assert s.pieces == [5, 7]

    s = UISet(set())
    assert s.pieces == []
    s = UISet({''})
    assert s.pieces == ['']

    s = UISet([2, Interval('(4, 6)'), 5, 6, 8])
    assert s.pieces == [2, Interval('(4, 6]'), 8]

    s = UISet([unbounded])
    assert s.pieces[0] == unbounded
    assert s.pieces[0] is not unbounded

    i1 = Interval('[1, 4]')
    i2 = Interval('[7, 9]')
    s = UISet([i1, i2])
    assert s.pieces == [Interval('[1, 4]'), Interval('[7, 9]')]
    assert s.pieces[0] is not i1
    assert s.pieces[1] is not i2

    i1 = Interval('[7, 9]')
    i2 = Interval('[1, 4]')
    s = UISet([i1, i2])
    assert s.pieces == [Interval('[1, 4]'), Interval('[7, 9]')]
    assert s.pieces[0] is not i1
    assert s.pieces[1] is not i2

    i1 = Interval('[1, 9]')
    i2 = Interval('[3, 5]')
    s = UISet([i1, i2])
    assert s.pieces == [Interval('[1, 9]')]

    i1 = Interval('[3, 5]')
    i2 = Interval('[1, 9]')
    s = UISet([i1, i2])
    assert s.pieces == [Interval('[1, 9]')]

    i1 = Interval('[1, 6]')
    i2 = Interval('[5, 8]')
    s = UISet([i1, i2])
    assert s.pieces == [Interval('[1, 8]')]

    i1 = Interval('[5, 8]')
    i2 = Interval('[1, 6]')
    s = UISet([i1, i2])
    assert s.pieces == [Interval('[1, 8]')]

    i1 = Interval('(0, 1)')
    i2 = Interval('(1, 2)')
    s = UISet([i1, i2])
    assert s.pieces == [Interval('(0, 1)'), Interval('(1, 2)')]


def test_uiset_init_from_notation():

    s = UISet('[1, 2]')
    assert s.pieces == [Interval('[1, 2]')]

    s = UISet('[1, 2], (4, 5)')
    assert s.pieces == [Interval('[1, 2]'), Interval('(4, 5)')]

    s = UISet('[1, 2], [5, inf)')
    assert s.pieces == [Interval('[1, 2]'), Interval('[5, inf)')]


def test_uiset_init_from_notation_raises():

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
            s = UISet(notation)


def test_uiset_repr():

    s = UISet()
    assert repr(s) == 'UISet([])'

    s = UISet([Interval('[1, 2.5)'), Interval('(2.5, 4]'), Interval('[7, 9]')])
    assert eval(repr(s)).pieces == s.pieces

    s = UISet([1, 2, 3])
    assert eval(repr(s)).pieces == s.pieces

    s = UISet([1, Interval('(2, 3)')])
    assert eval(repr(s)).pieces == s.pieces


def test_uiset_notation():

    s = UISet()
    assert s.notation == ''

    s = UISet([0])
    assert s.notation == '{0}'

    s = UISet([Interval('(-inf, 0)')])
    assert s.notation == '(-inf, 0)'

    s = UISet([Interval('(-inf, 0)'), Interval('[1, 2]')])
    assert s.notation == '(-inf, 0), [1, 2]'

    s = UISet([Interval('(-inf, 0)'), Interval('[1, 2]'), 4])
    assert s.notation == '(-inf, 0), [1, 2], {4}'


def test_uiset_add():

    s = UISet()
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

    s = UISet([i4])
    s.add(i3)
    assert s.pieces == [Interval('[-1, 1)')]

    i6 = Interval('[0, 1)')
    i7 = Interval('[-1, 0)')
    s = UISet([i6])
    s.add(i7)
    assert s.pieces == [Interval('[-1, 1)')]

    i8 = Interval('(0, 1)')
    i9 = Interval('(-1, 0)')
    s = UISet([i8])
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
    s0 = UISet('(4, 7)')
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
    s0 = UISet('(0, 4), (6, 8), (9, 10), (12, 15)')
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


def test_uiset_bool():

    s = UISet()
    assert bool(s) is False

    s.add(1)
    assert bool(s) is True

    s = UISet('[1, 2]')
    assert bool(s) is True


def test_uiset_invert():

    i0 = Interval('(-inf, inf)')
    s = UISet([i0])
    assert (~s).pieces == []
    assert (~~s).pieces == s.pieces

    s = UISet()
    assert (~s).pieces == [i0]
    assert (~~s).pieces == s.pieces

    i1 = Interval('[1, 4]')
    i2 = Interval('[7, 9]')
    s = UISet([i1, i2])
    expected = [Interval('(-inf, 1)'), Interval('(4, 7)'), Interval('(9, inf)')]
    assert (~s).pieces == expected
    assert (~~s).pieces == s.pieces

    i3 = Interval('[5, 8]')
    i4 = Interval('[1, 6]')
    s = UISet([i3, i4])
    assert (~s).pieces == [Interval('(-inf, 1)'), Interval('(8, inf)')]
    assert (~~s).pieces == s.pieces

    i5 = Interval('(0, 1)')
    i6 = Interval('(1, 2)')
    s = UISet([i5, i6])
    expected = [Interval('(-inf, 0]'), 1, Interval('[2, inf)')]
    assert (~s).pieces == expected
    assert (~~s).pieces == s.pieces

    i7 = Interval('(-inf, 0)')
    s = UISet([i7])
    assert (~s).pieces == [Interval('[0, inf)')]
    assert (~~s).pieces == s.pieces

    i8 = Interval('[0, inf)')
    s = UISet([i8])
    assert (~s).pieces == [i7]
    assert (~~s).pieces == s.pieces

    i9 = Interval('(0, inf)')
    s = UISet([i7, i9])
    assert (~s).pieces == [0]

    UISet('(-inf, 0), (0, inf)')
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

    s = UISet([0])
    assert (~s).pieces == [Interval('(-inf, 0)'), Interval('(0, inf)')]
    s = UISet([0, 1])
    assert (~s).pieces == [Interval('(-inf, 0)'), Interval('(0, 1)'), Interval('(1, inf)')]

    i1 = Interval('(-inf, 1]')
    i2 = Interval('(1, 2]')
    i3 = Interval('(2, 3)')
    i4 = Interval('(3, inf)')
    s = UISet([i2, 3])
    assert (~s).pieces == [i1, i3, i4]
    s = UISet([i1, 3])
    assert (~s).pieces == [Interval('(1, 3)'), i4]
    s = UISet([0, i2])
    assert (~s).pieces == [Interval('(-inf, 0)'), Interval('(0, 1]'), Interval('(2, inf)')]
    assert i1 == Interval('(-inf, 1]')
    assert i2 == Interval('(1, 2]')
    assert i3 == Interval('(2, 3)')
    assert i4 == Interval('(3, inf)')


def test_uiset_search():

    s = UISet()
    assert s.search(1) == (0, None)

    s = UISet('{1}')
    assert s.search(0) == (0, None)
    assert s.search(1) == (0, 1)
    assert s.search(2) == (1, None)
    
    s = UISet([unbounded])
    assert s.search(1) == (0, unbounded)
    assert s.search(float('-inf')) == (0, None)
    assert s.search(float('inf')) == (1, None)

    i1 = Interval('[0, 1]')
    i2 = Interval('(2, 3)')
    s = UISet([i1, i2])
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
    s = UISet([i1, 5, i2])
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


def test_uiset_contains_scalar():

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


def test_uiset_contains_interval():

    s = UISet()
    assert Interval('(1, 2)') not in s

    s = UISet('(1, 4)')
    assert Interval('(2, 3)') in s
    assert Interval('[1, 4)') not in s
    assert Interval('(1, 4]') not in s
    assert Interval('[1, 4]') not in s
    assert Interval('(0, 2)') not in s
    assert Interval('(3, 5)') not in s
    assert Interval('(0, 1)') not in s

    s = UISet('[1, 4)')
    assert Interval('(2, 3)') in s
    assert Interval('[1, 4)') in s
    assert Interval('(1, 4]') not in s
    assert Interval('[1, 4]') not in s
    assert Interval('(0, 2)') not in s
    assert Interval('(3, 5)') not in s

    s = UISet('(1, 4]')
    assert Interval('(2, 3)') in s
    assert Interval('[1, 4)') not in s
    assert Interval('(1, 4]') in s
    assert Interval('[1, 4]') not in s
    assert Interval('(0, 2)') not in s
    assert Interval('(3, 5)') not in s

    s = UISet('[1, 4]')
    assert Interval('(2, 3)') in s
    assert Interval('[1, 4)') in s
    assert Interval('(1, 4]') in s
    assert Interval('[1, 4]') in s
    assert Interval('(0, 2)') not in s
    assert Interval('(3, 5)') not in s


def test_uiset_eq_and_ne():

    s1 = UISet()
    s2 = UISet()
    assert s1 == s2
    s1.add(Interval('[1, 2]'))
    assert s1 != s2

    s2 = UISet([Interval('[1, 2]')])
    assert s1 == s2

    s2.remove(2)
    assert s1 != s2

    assert not s1 == 0
    assert s1 != 0

    s1 = UISet('{1}')
    s2 = UISet('{1}')
    assert s1 == s2
    s2 = UISet('{2}')
    assert s1 != s2


def test_uiset_remove():

    i1 = Interval('[0, 2]')
    s = UISet([i1])
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


def test_uiset_clear():

    i1 = Interval('[0, 1]')
    i2 = Interval('[2, 3]')
    s = UISet([i1, i2])
    s.clear()
    assert s.pieces == []


def test_uiset_copy():

    s1 = UISet()
    s2 = s1.copy()
    assert s1 == s2
    assert s1 is not s2

    s1 = UISet('{4}, {8}')
    s2 = s1.copy()
    assert s2.pieces == [4, 8]

    i = Interval('[1, 2]')
    s1 = UISet([i])
    s2 = s1.copy()
    assert s1 == s2
    assert s2.pieces[0] is not i

    l1 = [1, 2, 3]
    l2 = [4, 5, 6]
    a = Endpoint(None, l1, True, True)
    b = Endpoint(None, l2, True, False)
    i = Interval(None, a, b)
    s1 = UISet([i])
    s2 = s1.copy()
    s2.pieces[0].a.value[2] = -1
    assert i.a.value[2] == -1


def test_uiset_ge():

    s = UISet()
    assert s >= UISet()
    assert not s >= UISet('{1}')
    assert not s >= UISet('[1, 2]')

    s = UISet('{3}, {5}')
    assert s >= UISet()
    assert s >= UISet('{3}')
    assert s >= UISet('{5}')
    assert s >= UISet('{3}, {5}')
    assert not s >= UISet('{3}, {4}')
    assert not s >= UISet('(3, 5)')
    assert not s >= UISet('[3, 5]')

    s = UISet('(1, 6)')
    assert s >= UISet()
    assert not s >= UISet('{0}')
    assert not s >= UISet('{1}')
    assert s >= UISet('{3}')
    assert s >= UISet('{2}, {3}, {4}')
    assert not s >= UISet('{6}')
    assert not s >= UISet('[5, 6]')
    assert not s >= UISet('{7}')
    assert s >= UISet('(2, 3)')
    assert s >= UISet('(2, 3), {4}')
    assert s >= UISet('(2, 3), (4, 5)')
    assert s >= UISet('(1, 3), (4, 6)')
    assert s >= UISet('(1, 6)')
    assert not s >= UISet('(4, 6]')
    assert not s >= UISet('{3}, (4, 6]')
    assert not s >= UISet('(1, 6]')
    assert not s >= UISet('[1, 6)')
    assert not s >= UISet('[1, 6]')
    assert not s >= UISet('[2, 7]')

    s = UISet('(2, 4), (4, 6)')
    assert s >= UISet('(2, 4), (4, 6)')
    assert s >= UISet('(2, 3), (3, 4), (4, 6)')
    assert s >= UISet('{3}, {5}')
    assert not s >= UISet('(1, 3)')
    assert not s >= UISet('(3, 5)')
    assert not s >= UISet('(5, 7)')

    s = UISet('[1, 2]')
    assert s >= UISet('{1}')
    assert s >= UISet('{2}')
    assert not s >= UISet('{3}')
    assert s >= UISet('(1, 2)')
    assert s >= UISet('[1, 2]')

    s = UISet('[1, inf)')
    assert s >= UISet('{1}')
    assert s >= UISet('[1, 10]')
    assert not s >= UISet('(0, 10]')

    with pytest.raises(TypeError):
        UISet() >= 0
        UISet() >= -inf
    inf >= UISet()


def test_uiset_le():

    s = UISet()
    assert s <= UISet()
    assert s <= UISet('{1}')
    assert s <= UISet('[1, 2]')

    s = UISet('(1, 6)')
    assert not s <= UISet()
    assert not s <= UISet('{3}')
    assert not s <= UISet('(2, 3)')
    assert not s <= UISet('(2, 3), (4, 5)')
    assert not s <= UISet('(1, 3), (4, 6)')
    assert s <= UISet('(1, 6)')
    assert not s <= UISet('(4, 6]')
    assert not s <= UISet('{1}')
    assert s <= UISet('(1, 6]')
    assert s <= UISet('[1, 6)')
    assert s <= UISet('[1, 6]')
    assert not s <= UISet('[2, 7]')

    s = UISet('(2, 4), (4, 6)')
    assert s <= UISet('(2, 4), (4, 6)')
    assert not s <= UISet('(2, 3), (3, 4), (4, 6)')
    assert not s <= UISet('(1, 3)')
    assert not s <= UISet('(3, 5)')
    assert not s <= UISet('(5, 7)')

    s = UISet('[1, 2]')
    assert not s <= UISet('(1, 2)')
    assert s <= UISet('[1, 2]')

    s = UISet('[1, inf)')
    assert not s <= UISet('[1, 10]')
    assert not s <= UISet('(0, 10]')

    with pytest.raises(TypeError):
        UISet() <= 0


def test_uiset_issuperset():

    assert UISet('[1, 3]').issuperset(UISet('(1, 3)'))
    assert UISet('[1, 3]').issuperset(UISet('{1}, {2}, {3}'))
    assert not UISet().issuperset(UISet('(1, 3)'))

    assert UISet('[1, 3]').issuperset('(1, 2), {3}')
    assert UISet('[1, 3]').issuperset([])
    assert not UISet('[1, 3]').issuperset([0])

    assert UISet.issuperset(UISet('(0, 8)'), [2, 3, Interval('[3, 5]'), 6])


def test_uiset_issubset():

    assert not UISet('[1, 3]').issubset(UISet('(1, 3)'))
    assert UISet().issubset(UISet('{1}'))
    assert UISet().issubset(UISet('(1, 3)'))

    assert UISet('{1}').issubset('(0, 2)')
    assert not UISet('{1}, {2}').issubset([1, 3])

    assert UISet.issubset(UISet('(-2, -1)'), [Interval('(-inf, 0)')])


def test_uiset_gt():

    assert not UISet() > UISet()
    assert not UISet() > UISet('{1}')
    assert UISet('{1}') > UISet()
    assert not UISet('{1}') > UISet('{1}')
    assert not UISet('{1}') > UISet('{2}')
    s1 = UISet('(1, 2)')
    s2 = UISet('[1, 2)')
    s3 = UISet('(1, 2]')
    s4 = UISet('[1, 2]')
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
    
    s1 = UISet('(1, 2), {4}')
    s2 = UISet('(1, 2)')
    assert s1 > s2
    assert not s2 > s1

    s = UISet('(1, 4)')
    assert s > UISet('{2}')
    assert s > UISet('{2}, {3}')
    assert not s > UISet('{0}')
    assert not s > UISet('{1}')
    assert not s > UISet('{4}')
    assert not s > UISet('{5}')
    assert s > UISet('(1, 3)')
    assert s > UISet('(2, 3)')
    assert s > UISet('(2, 4)')

    s = UISet('(-inf, inf)')
    assert s > UISet('[1, 2], (3, inf)')
    assert not s > UISet('(-inf, inf)')

    with pytest.raises(TypeError):
        UISet('(1, 2)') > Interval('(1, 2)')
        UISet('(1, 2)') > 0
    

def test_uiset_lt():

    assert not UISet() < UISet()
    assert UISet() < UISet('{3}')
    assert UISet() < UISet('(1, 2)')
    assert not UISet('{0}') < UISet('(1, 2)')
    assert UISet('{1}') < UISet('{1}, {2}')

    with pytest.raises(TypeError):
        UISet() < 5


def test_uiset_or():

    s1 = UISet()
    s2 = UISet()
    assert s1 | s2 == UISet()

    s1 = UISet()
    s2 = UISet('{3}')
    assert s2 | s2 == s2
    assert s1 | s2 == s2 | s1 == s2

    s1 = UISet('(1, 2)')
    s2 = UISet('[2, 3]')
    assert s1 | s2 == s2 | s1 == UISet('(1, 3]')

    s1 = UISet('(1, 2)')
    s2 = UISet('{2}')
    assert s1 | s2 == s2 | s1 == UISet('(1, 2]')

    s1 = UISet('(1, 3), (3, 5), (5, 7)')
    s2 = UISet('{3}, {5}')
    assert s1 | s2 == s2 | s1 == UISet('(1, 7)')

    s1 = UISet('(-inf, 0), {2}, [4, 6], (9, 12]')
    s2 = UISet('(-inf, 0], (2, 3), {5}, (7, 8), {9}, (20, inf)')
    expected = UISet('(-inf, 0], [2, 3), [4, 6], (7, 8), [9, 12], (20, inf)')
    assert s1 | s2 == s2 | s1 == expected
    assert s1 == UISet('(-inf, 0), {2}, [4, 6], (9, 12]')
    assert s2 == UISet('(-inf, 0], (2, 3), {5}, (7, 8), {9}, (20, inf)')
    

def test_uiset_ior():

    s1 = UISet()
    s2 = UISet()
    s1 |= s2
    assert s1 == UISet()

    s1 = UISet()
    s2 = UISet('{3}')
    s1 |= s2
    s2 |= s1
    assert s1 == s2 == UISet('{3}')

    s1 = UISet('(1, 2)')
    s2 = UISet('{1}')
    s1 |= s2
    s2 |= s1
    assert s1 == s2 == UISet('[1, 2)')

    s1 = UISet('(1, 2)')
    s2 = UISet('(2, 3)')
    s1 |= s2
    s2 |= s1
    assert s1 == s2 == UISet('(1, 2), (2, 3)')
    s1 |= s1
    assert s1 == UISet('(1, 2), (2, 3)')


def test_uiset_union():

    s1 = UISet()
    s2 = UISet()
    s3 = UISet()
    assert s1.union(s2, s3) == UISet()

    s1 = UISet('{1}')
    s2 = UISet('{3}')
    s3 = UISet('{2}')
    assert s1.union(s2, s3) == UISet('{1}, {2}, {3}')
    assert s1 == UISet('{1}')
    assert s2 == UISet('{3}')
    assert s3 == UISet('{2}')

    s1 = UISet('(3, 4)')
    s2 = UISet('[2, 3]')
    s3 = UISet('[4, 5]')
    assert s1.union(s2, s3) == s2.union(s1, s3) == s3.union(s1, s2) == UISet('[2, 5]')
    assert s1.union(s1, s1, s3, s2, s3, s1, s2, s3) == UISet('[2, 5]')
    assert UISet.union(s1) == s1
    assert UISet.union(s1, s2, s3) == UISet('[2, 5]')
    assert s1 == UISet('(3, 4)')
    assert s2 == UISet('[2, 3]')
    assert s3 == UISet('[4, 5]')

    i1 = Interval('(-inf, 0)')
    i2 = Interval('(-10, 2)')
    s1 = UISet('(-inf, -5)')
    s2 = UISet('{5}')
    assert s1.union(s2, [i1, i2], [4, i1], []) == UISet('(-inf, 2), {4}, {5}')


def test_uiset_update():

    s1 = UISet()
    s2 = UISet()
    s3 = UISet()
    s1.update(s2, s3)
    assert s1 == UISet()

    s1 = UISet('{1}')
    s2 = UISet('{3}')
    s3 = UISet('{2}')
    s1.update(s2, s3)
    assert s1 == UISet('{1}, {2}, {3}')
    assert s2 == UISet('{3}')
    assert s3 == UISet('{2}')

    s1 = UISet('(3, 4)')
    s2 = UISet('[2, 3]')
    s3 = UISet('[4, 5]')
    s1.update(s1, s2, s1, s3, s2, s3, s1, s2, s3)
    assert s1 == UISet('[2, 5]')
    assert s2 == UISet('[2, 3]')
    assert s3 == UISet('[4, 5]')


def test_uiset_sub():

    s0 = UISet()
    s1 = UISet('{1}')
    s2 = UISet('{1}, {2}')
    s3 = UISet('[1, 2]')
    assert s0 - s0 == s0
    assert s1 - s0 == s1
    assert s0 - s1 == s0
    assert s2 - s1 == UISet('{2}')
    assert s0 == UISet()
    assert s1 == UISet('{1}')
    assert s2 == UISet('{1}, {2}')
    assert s3 == UISet('[1, 2]')
    assert s3 - s1 == UISet('(1, 2]')
    assert s3 - s2 == UISet('(1, 2)')
    assert s3 - s3 == s0

    s1 = UISet('(1, 4)')
    s2 = UISet('{1}, {2}, {3}, {4}')
    assert s1 - s2 == UISet('(1, 2), (2, 3), (3, 4)')
    assert s2 - s1 == UISet('{1}, {4}')

    s1 = UISet('(-inf, 0), {2}, [4, 6], [8, 20]')
    s2 = UISet('{-3}, {2}, (4, 9), [10, 11], {15}, {20}')
    assert s1 - s2 == UISet('(-inf, -3), (-3, 0), {4}, [9, 10), (11, 15), (15, 20)')
    assert s2 - s1 == UISet('(6, 8)')
    
    with pytest.raises(TypeError):
        UISet() - 0


def test_uiset_isub():

    s = UISet()
    s -= s
    assert s == UISet()

    s = UISet('(-inf, inf)')
    s -= UISet('{0}')
    assert s == UISet('(-inf, 0), (0, inf)')
    s -= UISet('{0}, {1}')
    assert s == UISet('(-inf, 0), (0, 1), (1, inf)')
    s -= UISet('(-inf, -2), (0, 1), (2, inf)')
    assert s == UISet('[-2, 0), (1, 2]')
    s -= UISet('{0}, {1}')
    assert s == UISet('[-2, 0), (1, 2]')
    s -= UISet('(-2, 2)')
    assert s == UISet('{-2}, {2}')
    s -= s.copy()
    assert s == UISet()

    with pytest.raises(TypeError):
        s -= 5


def test_uiset_difference():

    s = UISet()
    assert s.difference(s) == s

    s = UISet('[1, 3], [4, 5], [6, 7], [8, 10]')
    s = s.difference(UISet('(2, 9)'), UISet())
    assert s == UISet('[1, 2], [9, 10]')
    s = s.difference(UISet('{1}, {2}, {3}'), UISet('{4}'), UISet('{8}, {9}, {10}'))
    assert s == UISet('(1, 2), (9, 10)')

    s = UISet('(-inf, 0), {1}, {2}, [5, 9]')
    s = s.difference([Interval('(-inf, 3)'), 4, Interval('(5, 6)')], UISet())
    assert s == UISet('{5}, [6, 9]')

    s = UISet('[1, 3], {4}, [5, 7], {8}, (10, inf)')
    expected = UISet('[2, 3], {4}, (5, 6), (6, 7), (10, inf)')
    assert s.difference([6], [8, 5, 7], UISet('(-inf, 2)')) == expected

    assert UISet.difference(UISet('[1, 3]'), UISet('[2, 4]')) == UISet('[1, 2)')


def test_uiset_difference_update():

    s = UISet()
    s.difference_update(s, s)
    assert s == s

    s = UISet('{1}, {2}, {3}, (4, 6), [8, 9]')
    s.difference_update([Interval('[1, 4]'), 5], UISet('{2}, (8, 9)'))
    assert s == UISet('(4, 5), (5, 6), {8}, {9}')
    s.difference_update(~s)
    assert s == UISet('(4, 5), (5, 6), {8}, {9}')

