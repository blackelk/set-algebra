import pytest

from set_algebra import Endpoint, are_bounding


def test_endpoint_init_from_notation():

    e1 = Endpoint('[1')
    assert e1.left
    assert not e1.right
    assert not e1.open
    assert e1.value == 1
    e2 = Endpoint('(1')
    assert e2.left
    assert not e2.right
    assert e2.open
    assert e2.value == 1
    e3 = Endpoint('1]')
    assert not e3.left
    assert e3.right
    assert not e3.open
    assert e3.value == 1
    e4 = Endpoint('1)')
    assert not e4.left
    assert e4.right
    assert e4.open
    assert e4.value == 1


def test_endpoint_init_from_value_and_bound():

    assert Endpoint(1, '[').notation == '[1'
    assert Endpoint(1, '(').notation == '(1'
    assert Endpoint(1, ']').notation == '1]'
    assert Endpoint(1, ')').notation == '1)'


def test_endpoint_init_raises():

    with pytest.raises(TypeError): Endpoint(1)
    with pytest.raises(TypeError): Endpoint('[1', 1)

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


def test_endopint_init_from_notation():

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

    e1 = Endpoint('[5')
    e2 = Endpoint('(-inf')
    e3 = Endpoint('inf)')
    e4 = Endpoint(3, ')')
    e5 = Endpoint('A', '(')

    assert repr(e1) == "Endpoint('[5')"
    assert repr(e2) == "Endpoint('(-inf')"
    assert repr(e3) == "Endpoint('inf)')"
    assert repr(e4) == "Endpoint('3)')"
    assert repr(e5) == "Endpoint('A', '(')"

    assert eval(repr(e1)) == e1
    assert eval(repr(e2)) == e2
    assert eval(repr(e3)) == e3
    assert eval(repr(e4)) == e4
    assert eval(repr(e5)) == e5


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


def test_are_bounding():

    assert not are_bounding(Endpoint('(1'), Endpoint('1)'))
    assert are_bounding(Endpoint('(1'), Endpoint('1]'))
    assert are_bounding(Endpoint('[1'), Endpoint('1)'))
    assert are_bounding(Endpoint('[1'), Endpoint('1]'))
    assert not are_bounding(Endpoint('[1'), Endpoint('2]'))

