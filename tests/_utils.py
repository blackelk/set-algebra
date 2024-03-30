from set_algebra import Interval, Set

def do_bulk_tests(tests, fn, mode):

    for test in tests:
        arg, x, expected = test

        if isinstance(arg, list):
            s = Set()
            pieces_copy = []
            for a in arg:
                pieces_copy.append(a.copy() if isinstance(a, Interval) else a)
            s.pieces = pieces_copy
        elif isinstance(arg, str):
            s = Set(arg)
        elif isinstance(arg, Set):
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
