from uiset import inf, neg_inf


def test_inf():

    assert inf == inf
    assert inf == float('inf')
    assert not inf == 1
    assert not inf == 'Z'

    assert 1 != inf
    assert not inf != inf

    assert not inf > inf
    assert not inf > float('inf')
    assert inf > 1
    assert inf > 'Z'

    assert inf >= inf
    assert inf >= float('inf')
    assert inf >= 1
    assert inf >= 'Z'
    
    assert inf <= inf
    assert inf <= float('inf')
    assert not inf <= 1
    assert not inf <= 'Z'

    assert not inf < inf
    assert not inf < float('inf')
    assert not inf < 1
    assert not inf < 'Z'

    assert -inf is neg_inf


def test_neg_inf():

    assert neg_inf == neg_inf
    assert neg_inf == float('-inf')
    assert not neg_inf == 1
    assert not neg_inf == 'Z'

    assert 1 != neg_inf
    assert not neg_inf != neg_inf

    assert not neg_inf > neg_inf
    assert not neg_inf > float('-inf')
    assert not neg_inf > 1
    assert not neg_inf > 'Z'

    assert neg_inf >= neg_inf
    assert neg_inf >= float('-inf')
    assert not neg_inf >= 1
    assert not neg_inf >= 'Z'
    
    assert neg_inf <= neg_inf
    assert neg_inf <= float('-inf')
    assert neg_inf <= 1
    assert neg_inf <= 'Z'

    assert not neg_inf < neg_inf
    assert not neg_inf < float('-inf')
    assert neg_inf < 1
    assert neg_inf < 'Z'

    assert -neg_inf is inf

