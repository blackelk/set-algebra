import pytest
from uiset import Endpoint, Interval


def test_endpoint_init():

    e1 = Endpoint('[1')
    assert e1.open
    assert not e1.closed
    assert not e1.excluded
    assert e1.value == 1
    e2 = Endpoint('(1')
    assert e2.open
    assert not e2.closed
    assert e2.excluded
    assert e2.value == 1
    e3 = Endpoint('1]')
    assert not e3.open
    assert e3.closed
    assert not e3.excluded
    assert e3.value == 1
    e4 = Endpoint('1)')
    assert not e4.open
    assert e4.closed
    assert e4.excluded
    assert e4.value == 1


def test_endpoint_alt_init():

    assert Endpoint(value=1, excluded=False, open=True).notation == '[1'
    assert Endpoint(value=1, excluded=True, open=True).notation == '(1'
    assert Endpoint(value=1, excluded=False, open=False).notation == '1]'
    assert Endpoint(value=1, excluded=True, open=False).notation == '1)'


def test_endpoint_init_raises():

    with pytest.raises(TypeError): Endpoint('[1', 1)
    with pytest.raises(TypeError): Endpoint('[1', 1, True)
    with pytest.raises(TypeError): Endpoint('[1', 1, True, True)
    with pytest.raises(ValueError): Endpoint('1')
    with pytest.raises(ValueError): Endpoint('[1]')
    with pytest.raises(ValueError): Endpoint('[')
    with pytest.raises(ValueError): Endpoint('(1)')
    with pytest.raises(ValueError): Endpoint('(')
    with pytest.raises(ValueError): Endpoint(']')
    with pytest.raises(ValueError): Endpoint(')')
    with pytest.raises(ValueError): Endpoint('')
    with pytest.raises(ValueError): Endpoint('a')
    with pytest.raises(ValueError): Endpoint('[-inf')
    with pytest.raises(ValueError): Endpoint('inf]')


def test_endopint_parses_value():

    assert Endpoint('[1').value is 1
    v1 = Endpoint('[1.').value
    assert type(v1) is float and v1 == 1.0
    v2 = Endpoint('[1.0').value
    assert type(v2) is float and v2 == 1.0
    assert Endpoint('[10').value == 10
    assert Endpoint('[4.5e-6').value == 4.5e-6
    assert Endpoint('[4.5e6').value == 4.5e6
    assert Endpoint('(-inf').value == float('-inf')
    assert Endpoint('(neg_inf').value == float('-inf')
    assert Endpoint('inf)').value == float('inf')


def test_endpoint_repr():

    assert repr(Endpoint('[5')) == "Endpoint('[5')"
    assert repr(Endpoint('(-inf')) == "Endpoint('(neg_inf')"
    assert repr(Endpoint('inf)')) == "Endpoint('inf)')"
    assert repr(Endpoint(None, 3, True, False)) == "Endpoint('3)')"
    assert repr(Endpoint(None, '', True, True)) == "Endpoint(None, '', True, True)"


def test_endpoint_invert():

    assert ~Endpoint('[1') == Endpoint('1)')
    assert ~Endpoint('(1') == Endpoint('1]')
    assert ~Endpoint('1]') == Endpoint('(1')
    assert ~Endpoint('1)') == Endpoint('[1')
    assert ~~Endpoint('[2') == Endpoint('[2')


def test_endpoint_notation():

    assert Endpoint('[1').notation == '[1'
    assert Endpoint('(1').notation == '(1'
    assert Endpoint('1]').notation == '1]'
    assert Endpoint('1)').notation == '1)'


def test_endpoint_eq_scalar():

    assert Endpoint('[1') == 1
    assert Endpoint('1]') == 1
    assert not Endpoint('(1') == 1
    assert not Endpoint('1)') == 1
    assert not Endpoint('[1') == 2


def test_endpoint_ne_scalar():

    assert not Endpoint('[1') != 1
    assert not Endpoint('1]') != 1
    assert Endpoint('(1') != 1
    assert Endpoint('1)') != 1
    assert Endpoint('[1') != 2


def test_endpoint_gt_scalar():

    assert not Endpoint('[1') > 1
    assert Endpoint('(1') > 1
    assert not Endpoint('1]') > 1
    assert not Endpoint('1)') > 1
    assert Endpoint('[1') > 0
    assert Endpoint('(1') > 0
    assert Endpoint('1]') > 0
    assert Endpoint('1)') > 0
    assert not Endpoint('[1') > 2
    assert not Endpoint('(1') > 2
    assert not Endpoint('1]') > 2
    assert not Endpoint('1)') > 2


def test_endpoint_ge_scalar():

    assert Endpoint('[1') >= 1
    assert Endpoint('(1') >= 1
    assert Endpoint('1]') >= 1
    assert not Endpoint('1)') >= 1
    assert Endpoint('[1') >= 0
    assert Endpoint('(1') >= 0
    assert Endpoint('1]') >= 0
    assert Endpoint('1)') >= 0
    assert not Endpoint('[1') >= 2
    assert not Endpoint('(1') >= 2
    assert not Endpoint('1]') >= 2
    assert not Endpoint('1)') >= 2


def test_endpoint_lt_scalar():

    assert not Endpoint('[1') < 1
    assert not Endpoint('(1') < 1
    assert not Endpoint('1]') < 1
    assert Endpoint('1)') < 1
    assert not Endpoint('[1') < 0
    assert not Endpoint('(1') < 0
    assert not Endpoint('1]') < 0
    assert not Endpoint('1)') < 0
    assert Endpoint('[1') < 2
    assert Endpoint('(1') < 2
    assert Endpoint('1]') < 2
    assert Endpoint('1)') < 2


def test_endpoint_le_scalar():

    assert Endpoint('[1') <= 1
    assert not Endpoint('(1') <= 1
    assert Endpoint('1]') <= 1
    assert Endpoint('1)') <= 1
    assert not Endpoint('[1') <= 0
    assert not Endpoint('(1') <= 0
    assert not Endpoint('1]') <= 0
    assert not Endpoint('1)') <= 0
    assert Endpoint('[1') <= 2
    assert Endpoint('(1') <= 2
    assert Endpoint('1]') <= 2
    assert Endpoint('1)') <= 2


def test_endpoint_eq_enpoint():

    assert Endpoint('[1') == Endpoint('[1')
    assert Endpoint('(1') == Endpoint('(1')
    assert Endpoint('1]') == Endpoint('1]')
    assert Endpoint('1)') == Endpoint('1)')
    assert Endpoint('[1') != Endpoint('(1')
    assert Endpoint('[1') != Endpoint('1]')
    assert Endpoint('[1') != Endpoint('(1')


def test_endpoint_gt_endpoint():

    assert Endpoint('[1') > Endpoint('[0')
    assert Endpoint('[1') > Endpoint('(0')
    assert not Endpoint('[1') > Endpoint('[1')
    assert not Endpoint('[1') > Endpoint('(1')
    assert not Endpoint('[1') > Endpoint('[2')
    assert not Endpoint('[1') > Endpoint('(2')
    assert Endpoint('(1') > Endpoint('[0')
    assert Endpoint('(1') > Endpoint('(0')
    assert Endpoint('(1') > Endpoint('[1')
    assert not Endpoint('(1') > Endpoint('(1')
    assert not Endpoint('(1') > Endpoint('[2')
    assert not Endpoint('(1') > Endpoint('(2')
    assert Endpoint('1]') > Endpoint('[0')
    assert Endpoint('1]') > Endpoint('(0')
    assert not Endpoint('1]') > Endpoint('[1')
    assert not Endpoint('1]') > Endpoint('(1')
    assert not Endpoint('1]') > Endpoint('[2')
    assert not Endpoint('1]') > Endpoint('(2')
    assert Endpoint('1)') > Endpoint('[0')
    assert Endpoint('1)') > Endpoint('(0')
    assert not Endpoint('1)') > Endpoint('[1')
    assert not Endpoint('1)') > Endpoint('(1')
    assert not Endpoint('1)') > Endpoint('[2')
    assert not Endpoint('1)') > Endpoint('(2')

    assert Endpoint('[1') > Endpoint('0]')
    assert Endpoint('[1') > Endpoint('0)')
    assert not Endpoint('[1') > Endpoint('1]')
    assert Endpoint('[1') > Endpoint('1)')
    assert not Endpoint('[1') > Endpoint('2]')
    assert not Endpoint('[1') > Endpoint('2)')
    assert Endpoint('(1') > Endpoint('0]')
    assert Endpoint('(1') > Endpoint('0)')
    assert Endpoint('(1') > Endpoint('1]')
    assert Endpoint('(1') > Endpoint('1)')
    assert not Endpoint('(1') > Endpoint('2]')
    assert not Endpoint('(1') > Endpoint('2)')
    assert Endpoint('1]') > Endpoint('0]')
    assert Endpoint('1]') > Endpoint('0)')
    assert not Endpoint('1]') > Endpoint('1]')
    assert Endpoint('1]') > Endpoint('1)')
    assert not Endpoint('1]') > Endpoint('2]')
    assert not Endpoint('1]') > Endpoint('2)')
    assert Endpoint('1)') > Endpoint('0]')
    assert Endpoint('1)') > Endpoint('0)')
    assert not Endpoint('1)') > Endpoint('1]')
    assert not Endpoint('1)') > Endpoint('1)')
    assert not Endpoint('1)') > Endpoint('2]')
    assert not Endpoint('1)') > Endpoint('2)')


def test_endpoint_ge_endpoint():

    assert Endpoint('[1') >= Endpoint('[0')
    assert Endpoint('[1') >= Endpoint('(0')
    assert Endpoint('[1') >= Endpoint('[1')
    assert not Endpoint('[1') >= Endpoint('(1')
    assert not Endpoint('[1') >= Endpoint('[2')
    assert not Endpoint('[1') >= Endpoint('(2')
    assert Endpoint('(1') >= Endpoint('[0')
    assert Endpoint('(1') >= Endpoint('(0')
    assert Endpoint('(1') >= Endpoint('[1')
    assert Endpoint('(1') >= Endpoint('(1')
    assert not Endpoint('(1') >= Endpoint('[2')
    assert not Endpoint('(1') >= Endpoint('(2')
    assert Endpoint('1]') >= Endpoint('[0')
    assert Endpoint('1]') >= Endpoint('(0')
    assert Endpoint('1]') >= Endpoint('[1')
    assert not Endpoint('1]') >= Endpoint('(1')
    assert not Endpoint('1]') >= Endpoint('[2')
    assert not Endpoint('1]') >= Endpoint('(2')
    assert Endpoint('1)') >= Endpoint('[0')
    assert Endpoint('1)') >= Endpoint('(0')
    assert not Endpoint('1)') >= Endpoint('[1')
    assert not Endpoint('1)') >= Endpoint('(1')
    assert not Endpoint('1)') >= Endpoint('[2')
    assert not Endpoint('1)') >= Endpoint('(2')

    assert Endpoint('[1') >= Endpoint('0]')
    assert Endpoint('[1') >= Endpoint('0)')
    assert Endpoint('[1') >= Endpoint('1]')
    assert Endpoint('[1') >= Endpoint('1)')
    assert not Endpoint('[1') >= Endpoint('2]')
    assert not Endpoint('[1') >= Endpoint('2)')
    assert Endpoint('(1') >= Endpoint('0]')
    assert Endpoint('(1') >= Endpoint('0)')
    assert Endpoint('(1') >= Endpoint('1]')
    assert Endpoint('(1') >= Endpoint('1)')
    assert not Endpoint('(1') >= Endpoint('2]')
    assert not Endpoint('(1') >= Endpoint('2)')
    assert Endpoint('1]') >= Endpoint('0]')
    assert Endpoint('1]') >= Endpoint('0)')
    assert Endpoint('1]') >= Endpoint('1]')
    assert Endpoint('1]') >= Endpoint('1)')
    assert not Endpoint('1]') >= Endpoint('2]')
    assert not Endpoint('1]') >= Endpoint('2)')
    assert Endpoint('1)') >= Endpoint('0]')
    assert Endpoint('1)') >= Endpoint('0)')
    assert not Endpoint('1)') >= Endpoint('1]')
    assert Endpoint('1)') >= Endpoint('1)')
    assert not Endpoint('1)') >= Endpoint('2]')
    assert not Endpoint('1)') >= Endpoint('2)')


def test_endpoint_lt_endpoint():

    assert not Endpoint('[1') < Endpoint('[0')
    assert not Endpoint('[1') < Endpoint('(0')
    assert not Endpoint('[1') < Endpoint('[1')
    assert Endpoint('[1') < Endpoint('(1')
    assert Endpoint('[1') < Endpoint('[2')
    assert Endpoint('[1') < Endpoint('(2')
    assert not Endpoint('(1') < Endpoint('[0')
    assert not Endpoint('(1') < Endpoint('(0')
    assert not Endpoint('(1') < Endpoint('[1')
    assert not Endpoint('(1') < Endpoint('(1')
    assert Endpoint('(1') < Endpoint('[2')
    assert Endpoint('(1') < Endpoint('(2')
    assert not Endpoint('1]') < Endpoint('[0')
    assert not Endpoint('1]') < Endpoint('(0')
    assert not Endpoint('1]') < Endpoint('[1')
    assert Endpoint('1]') < Endpoint('(1')
    assert Endpoint('1]') < Endpoint('[2')
    assert Endpoint('1]') < Endpoint('(2')
    assert not Endpoint('1)') < Endpoint('[0')
    assert not Endpoint('1)') < Endpoint('(0')
    assert Endpoint('1)') < Endpoint('[1')
    assert Endpoint('1)') < Endpoint('(1')
    assert Endpoint('1)') < Endpoint('[2')
    assert Endpoint('1)') < Endpoint('(2')

    assert not Endpoint('[1') < Endpoint('0]')
    assert not Endpoint('[1') < Endpoint('0)')
    assert not Endpoint('[1') < Endpoint('1]')
    assert not Endpoint('[1') < Endpoint('1)')
    assert Endpoint('[1') < Endpoint('2]')
    assert Endpoint('[1') < Endpoint('2)')
    assert not Endpoint('(1') < Endpoint('0]')
    assert not Endpoint('(1') < Endpoint('0)')
    assert not Endpoint('(1') < Endpoint('1]')
    assert not Endpoint('(1') < Endpoint('1)')
    assert Endpoint('(1') < Endpoint('2]')
    assert Endpoint('(1') < Endpoint('2)')
    assert not Endpoint('1]') < Endpoint('0]')
    assert not Endpoint('1]') < Endpoint('0)')
    assert not Endpoint('1]') < Endpoint('1]')
    assert not Endpoint('1]') < Endpoint('1)')
    assert Endpoint('1]') < Endpoint('2]')
    assert Endpoint('1]') < Endpoint('2)')
    assert not Endpoint('1)') < Endpoint('0]')
    assert not Endpoint('1)') < Endpoint('0)')
    assert Endpoint('1)') < Endpoint('1]')
    assert not Endpoint('1)') < Endpoint('1)')
    assert Endpoint('1)') < Endpoint('2]')
    assert Endpoint('1)') < Endpoint('2)')


def test_endpoint_le_endpoint():

    assert not Endpoint('[1') <= Endpoint('[0')
    assert not Endpoint('[1') <= Endpoint('(0')
    assert Endpoint('[1') <= Endpoint('[1')
    assert Endpoint('[1') <= Endpoint('(1')
    assert Endpoint('[1') <= Endpoint('[2')
    assert Endpoint('[1') <= Endpoint('(2')
    assert not Endpoint('(1') <= Endpoint('[0')
    assert not Endpoint('(1') <= Endpoint('(0')
    assert not Endpoint('(1') <= Endpoint('[1')
    assert Endpoint('(1') <= Endpoint('(1')
    assert Endpoint('(1') <= Endpoint('[2')
    assert Endpoint('(1') <= Endpoint('(2')
    assert not Endpoint('1]') <= Endpoint('[0')
    assert not Endpoint('1]') <= Endpoint('(0')
    assert Endpoint('1]') <= Endpoint('[1')
    assert Endpoint('1]') <= Endpoint('(1')
    assert Endpoint('1]') <= Endpoint('[2')
    assert Endpoint('1]') <= Endpoint('(2')
    assert not Endpoint('1)') <= Endpoint('[0')
    assert not Endpoint('1)') <= Endpoint('(0')
    assert Endpoint('1)') <= Endpoint('[1')
    assert Endpoint('1)') <= Endpoint('(1')
    assert Endpoint('1)') <= Endpoint('[2')
    assert Endpoint('1)') <= Endpoint('(2')

    assert not Endpoint('[1') <= Endpoint('0]')
    assert not Endpoint('[1') <= Endpoint('0)')
    assert Endpoint('[1') <= Endpoint('1]')
    assert not Endpoint('[1') <= Endpoint('1)')
    assert Endpoint('[1') <= Endpoint('2]')
    assert Endpoint('[1') <= Endpoint('2)')
    assert not Endpoint('(1') <= Endpoint('0]')
    assert not Endpoint('(1') <= Endpoint('0)')
    assert not Endpoint('(1') <= Endpoint('1]')
    assert not Endpoint('(1') <= Endpoint('1)')
    assert Endpoint('(1') <= Endpoint('2]')
    assert Endpoint('(1') <= Endpoint('2)')
    assert not Endpoint('1]') <= Endpoint('0]')
    assert not Endpoint('1]') <= Endpoint('0)')
    assert Endpoint('1]') <= Endpoint('1]')
    assert not Endpoint('1]') <= Endpoint('1)')
    assert Endpoint('1]') <= Endpoint('2]')
    assert Endpoint('1]') <= Endpoint('2)')
    assert not Endpoint('1)') <= Endpoint('0]')
    assert not Endpoint('1)') <= Endpoint('0)')
    assert Endpoint('1)') <= Endpoint('1]')
    assert Endpoint('1)') <= Endpoint('1)')
    assert Endpoint('1)') <= Endpoint('2]')
    assert Endpoint('1)') <= Endpoint('2)')


def test_endpoint_copy():

    e1 = Endpoint('1]')
    e2 = e1.copy()
    assert e1 == e2
    assert e1 is not e2

