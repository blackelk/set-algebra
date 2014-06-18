from uiset import UISet


def do_bulk_isdisjoint_tests(tests):

    for x, y, expected in tests:
        X = UISet(x)
        Y = UISet(y)
        res1 = X.isdisjoint(Y)
        emsg = "UISet('%s').isdisjoint(UISet('%s')) returns %s, %s expected"
        assert res1 == expected, emsg % (X.notation, Y.notation, res1, expected)
        res2 = Y.isdisjoint(X)
        assert res2 == expected, emsg % (X.notation, Y.notation, res2, expected)


def test_isdisjoint_empty():

    tests = [
        ([], [], True),
        ([0], [], True),
        ([0, 1], [], True),
        ('(0, 1)', [], True),
    ]
    do_bulk_isdisjoint_tests(tests)


def test_isdisjoint_scalars():

    tests = [
        ([0], [0], False),
        ([0], [1], True),
        ([1, 2], [0], True),
        ([1, 2], [1], False),
        ([1, 2], [2], False),
        ([1, 2], [3], True),
    ]
    do_bulk_isdisjoint_tests(tests)


def test_isdisjoint_intervals():

    tests = [
        ('[2, 5]', '[0, 1]', True),
        ('[2, 5]', '[0, 2)', True),
        ('[2, 5]', '[0, 2]', False),
        ('[2, 5]', '[0, 3]', False),
        ('[2, 5]', '[0, 5)', False),
        ('[2, 5]', '[0, 5]', False),
        ('[2, 5]', '[0, 6]', False),

        ('[2, 5]', '[2, 3]', False),
        ('[2, 5]', '(2, 3]', False),
        ('[2, 5]', '[2, 5]', False),
        ('[2, 5]', '[2, 5)', False),
        ('[2, 5]', '[2, 5]', False),
        ('[2, 5]', '[2, 6]', False),

        ('[2, 5]', '[3, 3]', False),
        ('[2, 5]', '(3, 4]', False),
        ('[2, 5]', '[3, 5]', False),
        ('[2, 5]', '[3, 5)', False),
        ('[2, 5]', '[3, 5]', False),
        ('[2, 5]', '[3, 6]', False),

        ('[2, 5]', '[5, 6]', False),
        ('[2, 5]', '(5, 6]', True),
        ('[2, 5]', '[6, 7]', True),

        ('(2, 5)', '(0, 2)', True),
        ('(2, 5)', '(0, 2]', True),
        ('(2, 5)', '(0, 3]', False),
        ('(2, 5)', '(5, 6]', True),
        ('(2, 5)', '[5, 6]', True),

        ('(0, 1), (2, 3), (4, 5)', '(1, 2), (3, 4)', True),
        ('(0, 1), (2, 3), (4, 5)', '[1, 2], [3, 4]', True),
        ('(0, 1), (2, 3), [4, 5)', '[1, 2], [3, 4]', False),
    ]
    do_bulk_isdisjoint_tests(tests)


def test_isdisjoint_scalars_and_intervals():

    tests = [
        ('[1, 3]', [0], True),
        ('[1, 3]', [1], False),
        ('[1, 3]', [2], False),
        ('[1, 3]', [3], False),
        ('[1, 3]', [4], True),
        ('[1, 3]', [0, 4], True),
        ('[1, 3]', [0, 1, 4], False),
        ('[1, 3]', [0, 1, 3, 4], False),

        ('(1, 3]', [0], True),
        ('(1, 3]', [1], True),
        ('(1, 3]', [2], False),
        ('(1, 3]', [3], False),
        ('(1, 3]', [4], True),
        ('(1, 3]', [0, 1, 4], True),
        ('(1, 3]', [0, 1, 3, 4], False),

        ('(1, 3)', [0], True),
        ('(1, 3)', [1], True),
        ('(1, 3)', [2], False),
        ('(1, 3)', [3], True),
        ('(1, 3)', [4], True),
        ('(1, 3)', [0, 1, 3, 4], True),

        ('(0, 2), {4}', '{0}, {2}, (3, 4), {5}', True),
        ('(0, 2), {4}', '{0}, {2}, (3, 4], {5}', False),

        ('[0, 2], [5, 6]', '(2, 3), (3, 4), (4, 5)', True),
        ('[0, 2], [5, 6]', '(2, 3), (3, 4), (4, 5]', False),
    ]
    do_bulk_isdisjoint_tests(tests)


def test_isdisjoint_inf():

    tests = [
        ('(-inf, inf)', [], True),
        ('(-inf, inf)', [1], False),
        ('(-inf, inf)', '(1, 2)', False),
        ('(-inf, 0)', '(0, inf)', True),
        ('(-inf, 0), (0, inf)', [0], True),
        ('(-inf, 0), (0, inf)', '(0, 1)', False),
    ]
    do_bulk_isdisjoint_tests(tests)

