from uiset.endpoint import Endpoint
from uiset.infinity import inf, neg_inf


class Interval:
    """
    Class representing interval on an axis.
    Contains two Endpoint instances - a and b.

    There are 2 ways to instantiate Interval:
    - From notation string (for numeric values only):
        Interval('[0, 1]'), Interval('(3.4e+7, 5.6e+7]'), Interval('[0, inf]')
    - From two endpoints:
        a = Endpoint('[0')
        b = Endpoint('1]');
        Interval(a=a, b=b)
        will produce Interval('[0, 1]')
    Values of two endpoints must be comparable to each other.
    
    Instances of Interval support membership test ("in") operation for scalars,
        Endpoint instances and other Interval instances.

    See tests/test_interval.py

    >>> real = Interval('[-inf, inf]')
    >>> 99999999 in real
    True
    >>> percentage = Interval('[0, 100]')
    >>> 50 in percentage
    True
    >>> 200 in percentage
    False
    >>> negative = Interval('[-inf, 0)')
    >>> negative
    Interval('[-inf, 0)')
    >>> 0 in negative
    False
    >>> -1 in negative
    True
    >>> negative in real
    True
    >>> percentage in negative
    False
    >>> negative in percentage
    False
    >>>
    >>> a = Endpoint(value='p', excluded=False, open=True)
    >>> b = Endpoint(value='q', excluded=True, open=False)
    >>> p = Interval(a=a, b=b)
    >>> 'o' in p
    False
    >>> 'p' in p
    True
    >>> 'p' * 1000 in p
    True
    >>> 'q' in p
    False
    """
    __slots__ = ('a', 'b')

    def __init__(self, notation=None, a=None, b=None):

        if (notation is None) ^ any(k is not None for k in [a, b]):
            emsg = '%s() takes notation or 2 kwargs: a and b'
            raise TypeError(emsg % self.__class__.__name__)
        if notation is None:
            if not isinstance(a, Endpoint) or not isinstance(b, Endpoint):
                raise TypeError('Kwargs a and b must be instances of Endpoint')
        else:
            parts = notation.split(',')
            if len(parts) != 2:
                raise ValueError('Invalid notation')
            a, b = (Endpoint(part) for part in parts)
        if not a.open:
            raise ValueError('First endpoint must be open')
        if b.open:
            raise ValueError('Second endpoint must be closed')
        if b < a:
            raise ValueError('Second endpoint is less than the first one')
        self.a = a
        self.b = b

    @property
    def notation(self):
        return '%s, %s' % (self.a.notation, self.b.notation)

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, self.notation)

    def __eq__(self, other):
        return isinstance(other, Interval)\
           and self.a == other.a and self.b == other.b

    def __contains__(self, other):

        if isinstance(other, Interval):
            return self.a <= other.a and other.b <= self.b
        else:
            return self.a <= other <= self.b

    def copy(self):
        """Return a shallow copy of an Interval"""
        return Interval(a=self.a.copy(), b=self.b.copy())


def is_scalar(obj):
    return not isinstance(obj, Interval)


# unbounded represents interval from -inf to inf
unbounded = Interval(
    a=Endpoint(value=neg_inf, excluded=True, open=True),
    b=Endpoint(value=inf, excluded=True, open=False))
