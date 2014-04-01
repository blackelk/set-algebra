import datetime
import pytest
from uiset import Endpoint, Interval


def test_interval_init_raises():

    with pytest.raises(ValueError):
        Interval('[6]')
    with pytest.raises(TypeError):
        Interval(a=1, b='')
    with pytest.raises(TypeError):
        Interval('[1, 2]', Endpoint('[1'))
    with pytest.raises(TypeError):
        Interval('[1, 2]', Endpoint('[1'), Endpoint('2]'))
    with pytest.raises(ValueError):
        Interval(a=Endpoint('[1'), b=Endpoint('[2'))
    with pytest.raises(ValueError):
        Interval(a=Endpoint('[1'), b=Endpoint('[0'))


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


def test_str_interval():

    a = Endpoint(value='p', excluded=False, open=True)
    b = Endpoint(value='q', excluded=True, open=False)
    p = Interval(a=a, b=b)
    assert p.notation == '[p, q)'
    assert 'o' not in p
    assert 'p' in p
    assert 'p' * 1000 in p
    assert 'q' not in p
    with pytest.raises(TypeError):
        1 in p
    with pytest.raises(TypeError):
        Interval(a=p, b=Endpoint('3]'))


def test_date_interval():

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    inaweek = today + datetime.timedelta(days=7)
    ad1 = datetime.date(1, 1, 1)
    a = Endpoint(value=today, excluded=False, open=True)
    b = Endpoint(value=inaweek, excluded=True, open=False)
    week = Interval(a=a, b=b)
    assert today in week
    assert tomorrow in week
    assert ad1 not in week
    assert week in week

