import datetime
import sys
import pytest

from set_algebra import Endpoint, Interval, inf


def test_interval_init_from_notation():

    i1 = Interval('[1, 2]')
    assert i1.a.value == 1
    assert not i1.a.excluded
    assert i1.a.open
    assert i1.b.value == 2

    i2 = Interval('(1, inf)')
    assert i2.a.value == 1
    assert i2.a.excluded
    assert not i2.b.open
    assert i2.b.value == inf


def test_interval_init_from_values_and_bounds():

    i1 = Interval(1, 2, '[]')
    assert i1.a.value == 1
    assert not i1.a.excluded
    assert i1.a.open
    assert i1.b.value == 2

    i2 = Interval(1, inf, '()')
    assert i2.a.value == 1
    assert i2.a.excluded
    assert not i2.b.open
    assert i2.b.value == inf


def test_interval_init_from_endpoints():

    i1 = Interval(Endpoint(1, '['), Endpoint(2, ']'))
    assert i1.a.value == 1
    assert not i1.a.excluded
    assert i1.a.open
    assert i1.b.value == 2

    i2 = Interval(Endpoint(1, '('), Endpoint(inf, ')'))
    assert i2.a.value == 1
    assert i2.a.excluded
    assert not i2.b.open
    assert i2.b.value == inf


def test_interval_init_degenerate():

    i = Interval('[1, 1]')
    assert i.a.value == i.b.value == 1


def test_interval_repr():

    i1 = Interval('[1, 2]')
    i2 = Interval('[1, 2)')
    i3 = Interval('(1, 2]')
    i4 = Interval('(1, 2)')
    i5 = Interval('(-inf, 2)')
    i6 = Interval('(1, inf)')
    a = Endpoint('A', '[')
    b = Endpoint('Z', ']')
    i7 = Interval(a, b)

    assert repr(i1) == "Interval('[1, 2]')"
    assert repr(i2) == "Interval('[1, 2)')"
    assert repr(i3) == "Interval('(1, 2]')"
    assert repr(i4) == "Interval('(1, 2)')"
    assert repr(i5) == "Interval('(-inf, 2)')"
    assert repr(i6) == "Interval('(1, inf)')"
    assert repr(i7) == "Interval('A', 'Z', '[]')"

    assert eval(repr(i1)) == i1
    assert eval(repr(i2)) == i2
    assert eval(repr(i3)) == i3
    assert eval(repr(i4)) == i4
    assert eval(repr(i5)) == i5
    assert eval(repr(i6)) == i6
    assert eval(repr(i7)) == i7


def test_interval_init_invalid_notation_raises():

    with pytest.raises(ValueError):
        Interval('[6')
    with pytest.raises(ValueError):
        Interval('[6]')
    with pytest.raises(ValueError):
        Interval('[6,')
    with pytest.raises(ValueError):
        Interval('[6, 6)')
    with pytest.raises(ValueError):
        Interval('(6, 6]')
    with pytest.raises(ValueError):
        Interval('(6, 6)')
    with pytest.raises(ValueError):
        Interval('[6, 5)')


def test_interval_init_notation_with_bounds_raises():

    with pytest.raises(TypeError):
        Interval('[1, 2)', bounds='[)')


def test_interval_init_endpoint_with_value_raises():

    with pytest.raises(TypeError):
        Interval(Endpoint('[1'), 2)
    with pytest.raises(TypeError):
        Interval(Endpoint('[1'), 2, bounds='[)')
    with pytest.raises(TypeError):
        Interval(1, Endpoint('2)'))
    with pytest.raises(TypeError):
        Interval(1, Endpoint('2)'), bounds='[)')


if sys.version_info[0] == 3:
    def test_interval_init_not_comparable_endpoints_raises():
        with pytest.raises(TypeError):
            Interval(Endpoint('[1'), Endpoint('a', ')'))


def test_interval_init_not_ascending_endpoints_raises():

    with pytest.raises(ValueError):
        Interval(Endpoint('[1'), Endpoint('1)'))
    with pytest.raises(ValueError):
        Interval(Endpoint('(1'), Endpoint('1]'))
    with pytest.raises(ValueError):
        Interval(Endpoint('(1'), Endpoint('1)'))
    with pytest.raises(ValueError):
        Interval(Endpoint('[1'), Endpoint('-1]'))


def test_interval_init_not_ascending_values_raises():

    with pytest.raises(ValueError):
        Interval(1, 1, '[)')
    with pytest.raises(ValueError):
        Interval(1, 1, '(]')
    with pytest.raises(ValueError):
        Interval(1, 1, '()')
    with pytest.raises(ValueError):
        Interval(1, -11, '[]')


def test_interval_init_not_open_closed_raises():

    with pytest.raises(ValueError):
        Interval(Endpoint('[1'), Endpoint('(2'))
    with pytest.raises(ValueError):
        Interval(Endpoint('1]'), Endpoint('2)'))


def test_interval_init_not_valid_bounds_raises():

    with pytest.raises(ValueError):
        Interval(1, 2, '[[')
    with pytest.raises(ValueError):
        Interval(1, 2, '[(')
    with pytest.raises(ValueError):
        Interval(1, 2, ')(')
    with pytest.raises(ValueError):
        Interval(1, 2, '](')


def test_interval_eq():

    assert Interval('[1, 2]') == Interval('[1, 2]')
    assert Interval('[1, 2)') == Interval('[1, 2)')
    assert Interval('(1, 2]') == Interval('(1, 2]')
    assert Interval('(1, 2)') == Interval('(1, 2)')
    assert Interval('[1, 2]') != Interval('[1, 2)')
    assert Interval('[1, 2]') != Interval('(1, 2]')
    assert Interval('[1, 2]') != Interval('(1, 2)')
    assert Interval('[1, 2]') != Interval('[1, 3]')


def test_scalar_in_interval():

    assert 0 not in Interval('[1, 2]')
    assert 0 not in Interval('[1, 2)')
    assert 0 not in Interval('(1, 2]')
    assert 0 not in Interval('(1, 2)')
    assert 1 in Interval('[1, 2]')
    assert 1 in Interval('[1, 2)')
    assert 1 not in Interval('(1, 2]')
    assert 1 not in Interval('(1, 2)')
    assert 2 in Interval('[1, 2]')
    assert 2 not in Interval('[1, 2)')
    assert 2 in Interval('(1, 2]')
    assert 2 not in Interval('(1, 2)')
    assert 3 not in Interval('[1, 2]')
    assert 3 not in Interval('[1, 2)')
    assert 3 not in Interval('(1, 2]')
    assert 3 not in Interval('(1, 2)')
    

def test_endpoint_in_interval():

    assert Endpoint('[0') not in Interval('[1, 3]')
    assert Endpoint('(0') not in Interval('[1, 3]')
    assert Endpoint('0]') not in Interval('[1, 3]')
    assert Endpoint('0)') not in Interval('[1, 3]')
    assert Endpoint('[1') in Interval('[1, 3]')
    assert Endpoint('(1') in Interval('[1, 3]')
    assert Endpoint('1]') in Interval('[1, 3]')
    assert Endpoint('1)') not in Interval('[1, 3]')
    assert Endpoint('[2') in Interval('[1, 3]')
    assert Endpoint('(2') in Interval('[1, 3]')
    assert Endpoint('2]') in Interval('[1, 3]')
    assert Endpoint('2)') in Interval('[1, 3]')
    assert Endpoint('[3') in Interval('[1, 3]')
    assert Endpoint('(3') not in Interval('[1, 3]')
    assert Endpoint('3]') in Interval('[1, 3]')
    assert Endpoint('3)') in Interval('[1, 3]')
    assert Endpoint('[4') not in Interval('[1, 3]')
    assert Endpoint('(4') not in Interval('[1, 3]')
    assert Endpoint('4]') not in Interval('[1, 3]')
    assert Endpoint('4)') not in Interval('[1, 3]')


def test_interval_in_interval():

    assert Interval('[1, 2]') in Interval('[1, 2]')
    assert Interval('[1, 2]') not in Interval('[1, 2)')
    assert Interval('[1, 2]') not in Interval('(1, 2]')
    assert Interval('[1, 2]') not in Interval('(1, 2)')
    assert Interval('[1, 2)') in Interval('[1, 2]')
    assert Interval('[1, 2)') in Interval('[1, 2)')
    assert Interval('[1, 2)') not in Interval('(1, 2)')
    assert Interval('[1, 2)') not in Interval('(1, 2)')
    assert Interval('(1, 2]') in Interval('[1, 2]')
    assert Interval('(1, 2]') not in Interval('[1, 2)')
    assert Interval('(1, 2]') in Interval('(1, 2]')
    assert Interval('(1, 2]') not in Interval('(1, 2)')
    assert Interval('(1, 2)') in Interval('[1, 2]')
    assert Interval('(1, 2)') in Interval('[1, 2)')
    assert Interval('(1, 2)') in Interval('(1, 2]')
    assert Interval('(1, 2)') in Interval('(1, 2)')


def test_interval_copy():

    a = Endpoint('[1')
    b = Endpoint('2]')
    i1 = Interval(a, b)
    i2 = i1.copy()

    assert i1 == i2
    assert i1 is not i2
    assert a == i2.a
    assert a is not i2.a
    assert b == i2.b
    assert b is not i2.b


def test_str_interval():

    a = Endpoint('p', '(')
    b = Endpoint('q', ']')
    p = Interval(a, b)

    assert p.notation == '(p, q]'
    assert 'o' not in p
    assert 'p' not in p
    assert 'p' * 1000 in p
    assert 'pq' in p
    assert 'q' in p

    assert a in p
    assert b in p

    if sys.version_info[0] == 3:
        with pytest.raises(TypeError):
            1 in p
        with pytest.raises(TypeError):
            Endpoint('3]') in p


def test_date_interval():

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    week_later = today + datetime.timedelta(days=7)
    ad1 = datetime.date(1, 1, 1)
    week = Interval(today, week_later, '[)')

    assert today in week
    assert tomorrow in week
    assert ad1 not in week
    assert week in week

