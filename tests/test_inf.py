from set_algebra import inf, neg_inf


def test_eq():
    assert inf == inf
    assert inf == float('inf')
    assert not inf == 1
    assert not inf == float('nan')
    assert not inf == 'A'
    assert not inf == neg_inf


def test_ne():
    assert inf != 1
    assert not inf != inf
    assert not inf != float('inf')
    assert inf != float('nan')
    assert inf != 'A'
    assert inf != neg_inf


def test_gt():
    assert not inf > inf
    assert not inf > float('inf')
    assert inf > 1
    assert not inf > float('nan')
    assert inf > 'A'
    assert inf > neg_inf


def test_ge():
    assert inf >= inf
    assert inf >= float('inf')
    assert inf >= 1
    assert not inf >= float('nan')
    assert inf >= 'A'
    assert inf >= neg_inf


def test_le():
    assert inf <= inf
    assert inf <= float('inf')
    assert not inf <= 1
    assert not inf <= float('nan')
    assert not inf <= 'A'
    assert not inf <= neg_inf


def test_lt():
    assert not inf < inf
    assert not inf < float('inf')
    assert not inf < 1
    assert not inf < float('nan')
    assert not inf < 'A'
    assert not inf < neg_inf


def test_other_eq_inf():
    assert float('inf') == inf
    assert not 1 == inf
    assert not float('nan') == inf
    assert not 'A' == inf


def test_other_lt_inf():
    assert not float('inf') < inf
    assert 1 < inf
    assert not float('nan') < inf
    assert 'A' < inf


def test_other_le_inf():
    assert float('inf') <= inf
    assert 1 <= inf
    assert not float('nan') <= inf
    assert 'A' <= inf


def test_other_ge_inf():
    assert float('inf') >= inf
    assert not 1 >= inf
    assert not float('nan') >= inf
    assert not 'A' >= inf


def test_other_gt_inf():
    assert not float('inf') > inf
    assert not 1 > inf
    assert not float('nan') > inf
    assert not 'A' > inf


def test_neg():
    assert -inf is neg_inf
