from uiset.infinity import inf, neg_inf


def parse_value(value_str):

    # TODO: docstring
    value_str = value_str.strip()
    if value_str.isdigit() or (value_str[0] == '-' and value_str[1:].isdigit()):
        value = int(value_str)
    elif value_str in ('-inf', 'neg_inf'):
        value = neg_inf
    elif value_str == 'inf':
        value = inf
    else:
        value = float(value_str)

    return value


def parse_endpoint_notation(notation):
    """
    Parses string representing Endpoint (endpoint notation).
    Returns tuple of 3 elements:
        0: int or float instance, or inf or neg_inf
        1: bool indicating whether endpoint is excluded
        2: bool indicating whether endpoint is open
    Raises ValueError for invalid notation.
    >>> parse_endpoint_notation('[5.7')
    (5.7, False, True)
    >>> parse_endpoint_notation('9]')
    (9, False, False)
    >>> parse_endpoint_notation('inf)')
    (inf, True, False)
    """

    notation = notation.strip()
    if len(notation) < 2:
        raise ValueError('Invalid Notation')
    if notation[0] == '[':
        value_str = notation[1:]
        open = True
        excluded = False
    elif notation[0] == '(':
        value_str = notation[1:]
        open = True
        excluded = True
    elif notation[-1] == ']':
        value_str = notation[:-1]
        open = False
        excluded = False
    elif notation[-1] == ')':
        value_str = notation[:-1]
        open = False
        excluded = True
    else:
        raise ValueError('Invalid notation')

    value = parse_value(value_str)

    return value, excluded, open
