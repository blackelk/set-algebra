from __future__ import annotations

from set_algebra.infinity import Infinity, NegativeInfinity, neg_inf, is_finite
from set_algebra.parser import (OPEN_LEFT_TO_BOUNDS_MAPPING, parse_bound,
    parse_endpoint_notation)


Scalar = object # For type annotations

class Endpoint:
    """
    Class representing point on an axis. Can be of four kinds:
        [1      left-closed
        (1      left-open
        1]      right-closed
        1)      right-open

    There are 2 ways to instantiate Endpoint:

    - From notation string (for numeric values only):
        Endpoint('[1'), Endpoint('-0.6)'), Endpoint('3.4e-5'), Endpoint('(-inf')

    - From value and bound character
        Endpoint(3, ']'), Endpoint(datetime.date.today(), '(')

    Endpoints can be compared with scalars and endpoints.
    Endpoints support bitwise inversion:
    ~Endpoint('[7') -> Endpoint('7)')

    To give an idea how Endpoint can be compared to other Endpoint or scalar,
    the figure below demonstrates some Endpoints located on the real axis:
           (0                   1)  1]  (1                   2)
                                   [1
        0                           1                            2
    ------------------------------------------------------------------------->

    See tests/test_endpoint.py for details.
    """

    __slots__ = ('value', 'open', 'left')

    PARSABLE_TYPES = (int, float, Infinity, NegativeInfinity)

    def __init__(self, notation_or_value: str|Scalar,
                       bound: str|None = None) -> None:
        if bound is None:
            value, open_, left = parse_endpoint_notation(notation_or_value)
        else:
            value = notation_or_value
            open_, left = parse_bound(bound)

        if not open_ and not is_finite(value):
            raise ValueError('Not open value cannot be infinite, use "(" or ")" as bound')

        self.value = value
        self.open: bool = open_
        self.left: bool = left

    @property
    def right(self) -> bool:
        return not self.left

    @property
    def notation(self) -> str:
        if self.left:
            format_ = '(%s' if self.open else '[%s'
        else:
            format_ = '%s)' if self.open else '%s]'

        value_str = self.value == neg_inf and '-inf' or str(self.value)

        return format_ % value_str

    def __repr__(self) -> str:
        classname = type(self).__name__

        if isinstance(self.value, self.PARSABLE_TYPES) and not isinstance(self.value, bool):
            repr_format = "%s('%s')"
            args = (classname, self.notation)
        else:
            repr_format = "%s(%s, '%s')"
            bound = OPEN_LEFT_TO_BOUNDS_MAPPING[self.open, self.left]
            args = (classname, repr(self.value), bound)

        return repr_format % args

    def __eq__(self, other: Endpoint|object) -> bool:
        """
        self == other
        When comparing two Endpoints,
            test whether all 3 slots (value, open, left) are equal.
        When other is not Endpoint test whether Endpoint value is equal to the other,
            and if Endpoint is not open:
        >>> Endpoint('[1') == 1
        True
        >>> Endpoint('(1') == 1
        False
        """
        if isinstance(other, Endpoint):
            return self.value == other.value \
               and self.open == other.open \
               and self.left == other.left

        return not self.open and self.value == other

    def __ne__(self, other: Endpoint|object) -> bool:
        """ self != other """
        return not self == other

    def __gt__(self, other: Endpoint|object) -> bool:
        """ self > other """
        if isinstance(other, Endpoint):
            if self.value == other.value:
                return self._cmp(other) == 1
            return self.value > other.value

        if self.value == other:
            return self.open and self.left

        return self.value > other

    def __ge__(self, other: Endpoint|object) -> bool:
        """ self >= other """
        if isinstance(other, Endpoint):
            if self.value == other.value:
                return self._cmp(other) != -1
            return self.value > other.value

        if self.value == other:
            return not self.open or self.left

        return self.value > other

    def __lt__(self, other: Endpoint|object) -> bool:
        """ self < other """
        if isinstance(other, Endpoint):
            if self.value == other.value:
                return self._cmp(other) == -1
            return self.value < other.value

        if self.value == other:
            return self.open and self.right

        return self.value < other

    def __le__(self, other: Endpoint|object) -> bool:
        """ self <= other """
        if isinstance(other, Endpoint):
            if self.value == other.value:
                return self._cmp(other) != 1
            return self.value < other.value

        if self.value == other:
            return not self.open or self.right

        return self.value < other

    def _cmp(self, other: Endpoint) -> int:
        """Compare two Endpoints with equal values."""
        assert self.value == other.value

        if self.left:
            if other.left:
                if not self.open and not other.open:
                    return 0
                if not self.open and other.open:
                    return -1
                if self.open and not other.open:
                    return 1
                return 0

            if not self.open and not other.open:
                return 0
            return 1

        if other.left:
            if not self.open and not other.open:
                return 0
            return -1

        if not self.open and not other.open:
            return 0

        if not self.open and other.open:
            return 1

        if self.open and not other.open:
            return -1

        return 0

    def __invert__(self) -> Endpoint:
        """
        Return Endpoint with same value but opposite "open" and "left" attributes.
        >>> ~Endpoint('[1')
        Endpoint('1)')
        """
        bound = OPEN_LEFT_TO_BOUNDS_MAPPING[not self.open, not self.left]
        return Endpoint(self.value, bound)

    def copy(self) -> Endpoint:
        """Return a shallow copy of the Endpoint"""
        bound = OPEN_LEFT_TO_BOUNDS_MAPPING[self.open, self.left]
        return Endpoint(self.value, bound)


def are_bounding(e1: Endpoint, e2: Endpoint) -> bool:
    """
    Return boolean indicating that 2 endpoints have no gap between them.
    >>> are_bounding(Endpoint('1]'), Endpoint('(1'))
    True
    >>> are_bounding(Endpoint('[1'), Endpoint('1]'))
    True
    >>> are_bounding(Endpoint('1)'), Endpoint('(1'))
    False
    """
    if e1.left is e2.left:
        raise ValueError(f'It is expected that e1.left != e2.left but the endpoints are both left={e1.left}')

    return e1.value == e2.value and (not e1.open or not e2.open)
