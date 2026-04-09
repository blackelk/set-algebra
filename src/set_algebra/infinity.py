from __future__ import annotations
import math
from numbers import Real
from types import NotImplementedType


def _is_orderable(x: object) -> bool:
    """
    Return True if x supports ordering operations by design.
    Note: NaN is considered orderable here and must be handled separately.
    """
    try:
        x < x # pylint: disable=comparison-with-itself
    except Exception:
        # Usually TypeError, though some exotic types raise other errors
        return False

    return True


def _isnan(x: object) -> bool:
    return isinstance(x, Real) and math.isnan(x)


class Infinity:
    """
    Class representing infinity.
    Supports comparsion operations.
    Is greater than everything except infinity / nan.
    """
    def __eq__(self, other: object) -> bool:
        """
        self == other
        Equality here is not purely type-based - it delegates to foreign `==`
        """
        return isinstance(other, Infinity) or other == float('inf')

    def __ne__(self, other: object) -> bool:
        """ self != other """
        return not self == other

    def __gt__(self, other: object) -> bool|NotImplementedType:
        """ self > other """
        if isinstance(other, Infinity) or other == float('inf') or _isnan(other):
            return False

        if _is_orderable(other):
            return True

        return NotImplemented

    def __lt__(self, other: object) -> bool|NotImplementedType:
        """ self < other """
        if isinstance(other, (Infinity, NegativeInfinity)):
            return False

        if _is_orderable(other):
            return False # +inf is not less than any orderable value

        return NotImplemented

    def __ge__(self, other: object) -> bool|NotImplementedType:
        """ self >= other """
        if _isnan(other):
            return False

        lt = self.__lt__(other)

        if lt is NotImplemented:
            return NotImplemented

        return not lt

    def __le__(self, other: object) -> bool|NotImplementedType:
        """ self <= other """
        if _isnan(other):
            return False

        gt = self.__gt__(other)

        if gt is NotImplemented:
            return NotImplemented

        return not gt

    def __neg__(self) -> NegativeInfinity:
        """ -self """
        return neg_inf

    def __repr__(self) -> str:
        return 'inf'


class NegativeInfinity:
    """
    Class representing negative infinity.
    Supports comparsion operations.
    Is less than everything except negative infinity / nan.
    """
    def __eq__(self, other: object) -> bool:
        """
        self == other
        Equality here is not purely type-based - it delegates to foreign `==`
        """
        return isinstance(other, NegativeInfinity) or other == float('-inf')

    def __ne__(self, other: object) -> bool:
        """ self != other """
        return not self == other

    def __gt__(self, other: object) -> bool|NotImplementedType:
        """ self > other """
        if isinstance(other, (Infinity, NegativeInfinity)):
            return False

        if _is_orderable(other):
            return False # -inf is not greater than any orderable value

        return NotImplemented

    def __lt__(self, other: object) -> bool|NotImplementedType:
        """ self < other """
        if isinstance(other, NegativeInfinity) or other == float('-inf') or _isnan(other):
            return False

        if _is_orderable(other):
            return True

        return NotImplemented

    def __ge__(self, other: object) -> bool|NotImplementedType:
        """ self >= other """
        if _isnan(other):
            return False

        lt = self.__lt__(other)

        if lt is NotImplemented:
            return NotImplemented

        return not lt

    def __le__(self, other: object) -> bool|NotImplementedType:
        """ self <= other """
        if _isnan(other):
            return False

        gt = self.__gt__(other)

        if gt is NotImplemented:
            return NotImplemented

        return not gt

    def __neg__(self) -> Infinity:
        """ -self """
        return inf

    def __repr__(self) -> str:
        return 'neg_inf'


def is_finite(x: object) -> bool:
    if _isnan(x):
        return False

    return neg_inf != x != inf


inf: Infinity = Infinity()
neg_inf: NegativeInfinity = NegativeInfinity()
