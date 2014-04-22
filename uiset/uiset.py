from uiset.infinity import inf, neg_inf
from uiset.endpoint import Endpoint, are_bounding
from uiset.interval import Interval, unbounded


import functools
def _assert_intervals_are_ascending(fn):
    """
    Debug decorator for UISet methods.
    Makes sure every interval's start is greater than previous interval's end,
    and every open endpoint of one interval is not a closed endpoint of the other.
    """
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        res = fn(self, *args, **kwargs)
        for i, interval in enumerate(self.intervals[:-1]):
            end = interval.b
            start = self.intervals[i+1].a
            error = None
            if end >= start:
                error = '%s >= %s in UISet %s'
            elif end.value == start.value and end.excluded != start.excluded:
                error = 'no gap between %s and %s! in UISet %s'
            if error:
                params = (end.notation, start.notation, self.notation)
                assert False, error % params
        return res
    return wrapper


class UISet:
    """
    Uncountable Infinite Set

    UISet can be instantiated from either:
        - iterable of intervals: UISet([Interval('[1, 2]'), Interval('[5, inf)')])
        - notation string: UISet('[1, 2], [5, inf)'). Note that in this case all
            the intervals must be sorted in ascending order and must not intersect.
        - another UISet. Intervals will be copied.
        - nothing for empty UISet: UISet() 
    
    The subset and equality comparisons do not generalize to a total ordering function.
    For example, any two nonempty disjoint UISets are not equal and are not subsets of each other,
    so all of the following return False: a<b, a==b, or a>b.

    Note, the non-operator versions of union(), intersection(), difference(), and symmetric_difference(), issubset(), and issuperset() methods will accept any iterable as an argument.
    In contrast, their operator based counterparts require their arguments to be UISets.

    Note, the elem argument to the __contains__(), remove(), and discard() methods may be an UISet.

    In boolean context UISet is True if it is not empty and False if it is empty.
    """

    def __init_from_notation(self, notation):

        if ',' not in notation:
            raise ValueError('Invalid %s notation' % type(self).__name__)
        it = iter(notation.split(','))
        for a, b in zip(it, it):
            interval = Interval(a=Endpoint(a), b=Endpoint(b))
            if self.intervals:
                last = self.intervals[-1]
                if last.b > interval.a or last.b == ~interval.a:
                    emsg = '%s notation must be ascending' % type(self).__name__
                    raise ValueError(emsg)
            self.intervals.append(interval)

    @_assert_intervals_are_ascending
    def __init__(self, arg=None):
        
        if isinstance(arg, type(self)):
            self.intervals = [i.copy() for i in arg.intervals]
            return
        self.intervals = []
        if arg is None:
            return
        elif isinstance(arg, str):
            self.__init_from_notation(arg)
        else:
            # Initialize from iterable of intervals.
            for interval in arg:
                self.add(interval)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.intervals)

    @property
    def notation(self):
        return ', '.join(i.notation for i in self.intervals)

    def __bool__(self):
        return len(self.intervals) > 0

    def search(self, x, lo=0, hi=None, enumerated=False):
        """
        Return UISet`s Interval that contains scalar x, or None if none found.

        Implements Binary search.
        
        Optional args lo (default 0) and hi (default len(self.intervals)) bound the
            slice of self.intervals to be searched.
        
        If optional arg enumerated is True, tuple of 2 items below will be returned:
            - index of interval containing x,
            - interval itself.
        """
        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = len(self.intervals)
        while lo < hi:
            mid = (lo+hi) // 2
            mid_interval = self.intervals[mid]
            if mid_interval.b < x:
                lo = mid + 1
            elif mid_interval.a > x:
                hi = mid
            else:
                return enumerated and (mid, mid_interval) or mid_interval
        return None

    def __contains__(self, x):
        """
        x in self
        Test x for membership in UISet.
        x can be either scalar or Interval.
        Note that if x is interval, returning True does not mean that one of
        intervals equals to x, because there can be an interval larger than x.
        """
        if isinstance(x, Interval):
            interval = self.search(x.a)
            if interval is None:
                return False
            return x.b <= interval.b
        else:
            return bool(self.search(x))
        
    @_assert_intervals_are_ascending
    def __invert__(self):
        """
        ~self
        Return a new UISet with elements that self does not contain.
        Double inversion (~~self) returns UISet that is equal to self.
        """
        new = UISet([])
        if not self.intervals:
            new.intervals.append(unbounded.copy())
            return new
        if self.intervals[0] == unbounded.copy():
            return new
        # Get plain list of endpoints from original UISet.
        endpoints = []
        for i in self.intervals:
            endpoints += [i.a, i.b]
        # Make sure the first endpoint is either -inf or inverted original one.
        if endpoints[0].value == neg_inf:
            del endpoints[0]
            endpoints[0] = ~endpoints[0]
        else:
            endpoints.insert(0, Endpoint('(-inf'))
        # Make sure the last endpoint is either inf or inverted original one.
        if endpoints[-1].value == inf:
            del endpoints[-1]
            endpoints[-1] = ~endpoints[-1]
        else:
            endpoints.append(Endpoint('inf)'))
        # Invert inner endpoints.
        endpoints[1:-1] = [~e for e in endpoints[1:-1]]
        # Construct new UISet`s intervals from endpoint pairs.
        for a, b in zip(endpoints[::2], endpoints[1::2]):
            i = Interval(a=a, b=b)
            new.intervals.append(i)

        return new

    def isdisjoint(self, other):
        """
        Return True if UISet has no elements in common with other.
        UISets are disjoint if and only if their intersection is the empty UISet.
        """

    def __eq__(self, other):
        """
        self == other
        Test whether UISet contains all the elements of other and vice versa.
        """
        return isinstance(other, UISet) and self.intervals == other.intervals

    def __ne__(self, other):
        """
        self != other
        Test whether UISet contains at least one element that other does not contain or vice versa.
        """
        return not isinstance(other, UISet) or self.intervals != other.intervals

    def __gt__(self, other):
        """
        self > other
        Test whether the UISet is a proper superset of other.
        """

    def __ge__(self, other):
        """
        self >= other
        Test whether every element in other is in the UISet.
        """
        if not isinstance(other, UISet):
            raise TypeError('Can only compare to an UISet')
        lo = 0
        Y = iter(other.intervals)
        try:
            y = next(Y)
            while True:
                res = self.search(y.a, lo=lo, enumerated=True)
                if not res:
                    return False
                lo, x = res
                if y.b > x.b:
                    return False
                while True:
                    y = next(Y)
                    if y.a >= x.b or y.b == x.b:
                        break
                    if y.b < x.b:
                        continue
                    return False
        except StopIteration:
            return True

    def issuperset(self, other):
        """Test whether every element in other is in the UISet."""
        return self >= other

    def __le__(self, other):
        """
        self <= other
        Test whether every element in the UISet is in other.
        """
        return NotImplemented # so that other.__ge__ will be called

    def issubset(self, other):
        """Test whether every element in the UISet is in other."""
        return self <= other

    def __lt__(self, other):
        """
        self < other
        Test whether the UISet is a proper subset of other.
        """

    def __or__(self, other):
        """
        self | other
        Return a new UISet with elements from the UISet and other.
        """

    def union(self, *others):
        """Return a new UISet with elements from the UISet and all others."""
        # same as __or__

    def __and__(self, other):
        """
        self & other
        Return a new UISet with elements common to the UISet and other.
        """

    def intersection(self, *others):
        """Return a new UISet with elements common to the UISet and all others."""
        # same as __and__

    def __sub__(self, other):
        """
        self - other
        Return a new UISet with elements in the UISet that are not in other.
        """

    def difference(self, *others):
        """
        Return a new UISet with elements in the UISet that are not in the others.
        """
        # same as __sub__

    def __xor__(self, other):
        """
        self ^ other
        Return a new UISet with elements in either the UISet or other but not both."""

    def symmetric_difference(self, other):
        """
        Return a new UISet with elements in either the UISet or other but not both."""
        # same as __xor__

    def __ior__(self, other):
        """
        self |= other
        Update the UISet, adding elements from other.
        """

    def update(self, *others):
        """
        Update the UISet, adding elements from all others.
        """
        # same as __ior__

    def __iand__(self, other):
        """
        self &= other
        Update the UISet, keeping only elements found in it and other.
        """

    def intersection_update(self, *others):
        """
        Update the UISet, keeping only elements found in it and all others.
        """

    def __isub__(self, other):
        """
        self -= other
        Update the UISet, removing elements found in other.
        """

    def difference_update(self, *others):
        """
        Update the UISet, removing elements found in others.
        """

    def __ixor__(self, other):
        """
        self ^= other
        Update the UISet, keeping only elements found in either UISet, but not in both.
        """
    
    def symmetric_difference_update(self, other):
        """
        Update the UISet, keeping only elements found in either UISet, but not in both.
        """

    def bisect_left(self, x, lo=0, hi=None):
        """
        Return index of the first interval having a >= x,
        OR return -1 if such intervals does not exit.
        """
        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = len(self.intervals)
        while lo < hi:
            mid = (lo+hi) // 2
            if self.intervals[mid].a < x:
                lo = mid + 1
            else:
                hi = mid
        return lo == len(self.intervals) and -1 or lo

    @_assert_intervals_are_ascending
    def add(self, x):
        """Add interval x to existing intervals, merge them if needed."""
        x = x.copy()
        a, b = x.a, x.b
        intervals = self.intervals
        if not intervals:
            intervals.append(x)
            return
        na = self.bisect_left(x.a)
        if na == -1:
            prev = intervals[-1]
            if x.a > prev.b:
                if are_bounding(x.a, prev.b):
                    prev.b = b
                else:
                    intervals.append(x)
            else:
                a = prev.a
                b = max([prev.b, x.b])
                interval = Interval(a=a, b=b)
                intervals[-1] = interval
            return
        if na > 0:
            prev = intervals[na-1]
            if x.a < prev.b or are_bounding(x.a, prev.b):
                a = prev.a
                na -= 1
        nb = self.bisect_left(x.b, na)
        if nb != -1:
            if are_bounding(intervals[nb].a, x.b):
                nb += 1
                b = intervals[nb-1].b
            elif nb > na:
                b = max([x.b, intervals[nb-1].b])
        else:
            b = max([x.b, intervals[-1].b])
            nb = None
        interval = Interval(a=a, b=b)
        intervals[na:nb] = [interval]

    def remove(self, elem):
        """Remove element elem from the UISet.
        Raises LookupError if elem is not contained in the UISet."""

    @_assert_intervals_are_ascending
    def discard(self, elem):
        """Remove scalar element elem from the UISet if it is present.
        Dependently on values, none of intervals will change,
            or one of endpoints will be excluded,
            or one of intervals will be splitted into two intervals.
        """
        res = self.search(elem, enumerated=True)
        if not res:
            return
        n, interval = res
        if interval.a == elem:
            interval.a.excluded = True
        elif interval.b == elem:
            interval.b.excluded = True
        else:
            # Split interval by elem.
            i1 = Interval(a=interval.a, b=Endpoint(None, elem, True, False))
            i2 = Interval(a=Endpoint(None, elem, True, True), b=interval.b)
            self.intervals[n:n+1] = [i1, i2]

    def pop(self):
        """
        Remove and return an arbitrary element from the UISet.
        Raises KeyError if the UISet is empty."""

    def clear(self):
        """Remove all intervals from the UISet."""
        self.intervals = []

    def copy(self):
        """
        Return a copy of an UISet.
        Intervals are recreated.
        copy is safe as long as endpoint values are of immutable types.
        """
        new = UISet()
        new.intervals = [i.copy() for i in self.intervals]
        return new

