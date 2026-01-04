from set_algebra import inf, neg_inf


def test_eq():
    assert neg_inf == neg_inf
    assert neg_inf == float('-inf')
    assert not neg_inf == 1
    assert not neg_inf == float('nan')
    assert not neg_inf == 'A'
    assert not neg_inf == inf


def test_ne():
    assert neg_inf != 1
    assert not neg_inf != neg_inf
    assert not neg_inf != float('-inf')
    assert neg_inf != float('nan')
    assert neg_inf != 'A'
    assert neg_inf != inf


def test_gt():
    assert not neg_inf > neg_inf
    assert not neg_inf > float('-inf')
    assert not neg_inf > 1
    assert not neg_inf > float('nan')
    assert not neg_inf > 'A'
    assert not neg_inf > inf


def test_ge():
    assert neg_inf >= neg_inf
    assert neg_inf >= float('-inf')
    assert not neg_inf >= 1
    assert not neg_inf >= float('nan')
    assert not neg_inf >= 'A'
    assert not neg_inf >= inf


def test_le():
    assert neg_inf <= neg_inf
    assert neg_inf <= float('-inf')
    assert neg_inf <= 1
    assert not neg_inf <= float('nan')
    assert neg_inf <= 'A'
    assert neg_inf <= inf


def test_lt():
    assert not neg_inf < neg_inf
    assert not neg_inf < float('-inf')
    assert neg_inf < 1
    assert not neg_inf < float('nan')
    assert neg_inf < 'A'
    assert neg_inf < inf


def test_other_eq_neg_inf():
    assert float('-inf') == neg_inf
    assert not 1 == neg_inf
    assert not float('nan') == neg_inf
    assert not 'A' == neg_inf


def test_other_lt_neg_inf():
    assert not float('-inf') < neg_inf
    assert not 1 < neg_inf
    assert not float('nan') < neg_inf
    assert not 'A' < neg_inf


def test_other_le_neg_inf():
    assert float('-inf') <= neg_inf
    assert not 1 <= neg_inf
    assert not float('nan') <= neg_inf
    assert not 'A' <= neg_inf


def test_other_ge_neg_inf():
    assert float('-inf') >= neg_inf
    assert 1 >= neg_inf
    assert not float('nan') >= neg_inf
    assert 'A' >= neg_inf


def test_other_gt_neg_inf():
    assert not float('-inf') > neg_inf
    assert 1 > neg_inf
    assert not float('nan') > neg_inf
    assert 'A' > neg_inf


def test_neg():
    assert -neg_inf is inf
