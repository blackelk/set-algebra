from set_algebra.infinity import Infinity, NegativeInfinity, inf, neg_inf


def parse_value(value_str: str) -> int | float | Infinity | NegativeInfinity:
    """
    Parse numeric string, return either:
    int
    float
    Infinity, NegativeInfinity
    """
    if not isinstance(value_str, str):
        classname = type(value_str).__name__
        raise TypeError(f'value_str must be a string, not {classname}')

    value_str = value_str.strip()

    if value_str.isdigit() or (value_str.startswith('-') and value_str[1:].isdigit()):
        value = int(value_str)
    elif value_str in ('-inf', 'neg_inf'):
        value = neg_inf
    elif value_str == 'inf':
        value = inf
    else:
        value = float(value_str)

    return value


BOUNDS_TO_OPEN_LEFT_MAPPING = {
    '[': (False, True),
    '(': (True, True),
    ']': (False, False),
    ')': (True, False),
}

OPEN_LEFT_TO_BOUNDS_MAPPING = {v: k for k, v in BOUNDS_TO_OPEN_LEFT_MAPPING.items()}


def parse_bound(bound: str) -> tuple[bool, bool]:
    """
    Given 1 length string, return a tuple of two booleans: (open, left)
    """
    if not isinstance(bound, str):
        classname = type(bound).__name__
        raise TypeError(f'bound must be a string, not {classname}')

    try:
        return BOUNDS_TO_OPEN_LEFT_MAPPING[bound]
    except KeyError:
        raise ValueError(f'bound must be one of [](), not {bound}') from None


def parse_endpoint_notation(notation: str) -> tuple[int|float|Infinity|NegativeInfinity, bool, bool]:
    """
    Parse string representing Endpoint (endpoint notation).

    Returns tuple of 3 elements:
        0: int or float instance, or inf or neg_inf
        1: bool indicating whether endpoint is open
        2: bool indicating whether endpoint is left
    Raises ValueError for invalid notation.

    >>> parse_endpoint_notation('[5.7')
    (5.7, False, True)
    >>> parse_endpoint_notation('9]')
    (9, False, False)
    >>> parse_endpoint_notation('inf)')
    (inf, True, False)
    """
    if not isinstance(notation, str):
        classname = type(notation).__name__
        raise TypeError(f'notation must be a string, not {classname}')

    notation = notation.strip()

    if len(notation) < 2:
        raise ValueError('Invalid Notation')

    if notation[0] in '[(':
        bound, value_str = notation[0], notation[1:]

    elif notation[-1] in '])':
        value_str, bound = notation[:-1], notation[-1]

    else:
        raise ValueError('Invalid notation')

    open_, left = BOUNDS_TO_OPEN_LEFT_MAPPING[bound]

    value = parse_value(value_str)

    return value, open_, left
