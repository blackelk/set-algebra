"""
uiset Library

According to set theory, provides instruments to represent and work with:
Infinity
Negative Infinity
Endpoint
Interval
Uncountable Infinite Set
"""

__title__ = 'uiset'
__version__ = '0.2.0'
__author__ = 'Constantine Parkhimovich'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Constantine Parkhimovich'


from uiset.infinity import Infinity, NegativeInfinity, is_finite, inf, neg_inf
from uiset.endpoint import Endpoint, are_bounding
from uiset.interval import Interval, is_interval, is_scalar, unbounded
from uiset.parser import parse_value, parse_endpoint_notation


import functools
def _assert_pieces_are_ascending(fn):
    """
    Debug decorator for UISet methods.
    Makes sure pieces are sorted in ascending order and do not intersect.
    """
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        res = fn(self, *args, **kwargs)
        error = None
        for i, cur in enumerate(self.pieces[:-1]):
            nex = self.pieces[i+1]
            if isinstance(cur, Interval):
                if isinstance(nex, Interval):
                    if cur.b >= nex.a:
                        error = '%s >= %s in UISet %s'
                        params = (cur.b.notation, nex.a.notation, self.notation)
                    elif are_bounding(cur.b, nex.a):
                        error = 'no gap between %s and %s! in UISet %s'
                        params = (cur.b.notation, nex.a.notation, self.notation)
                else:
                    if cur.b >= nex:
                        error = '%s >= %s in UISet %s'
                        params = (cur, nex.a.notation, self.notation)
                    elif cur.b.value == nex:
                        error = 'no gap between %s and %s! in UISet %s'
                        params = (cur.b.notation, nex, self.notation)
            else:
                if isinstance(nex, Interval):
                    if cur >= nex.a:
                        error = '%s >= %s in UISet %s'
                        params = (cur, nex.a.notation, self.notation)
                    elif cur == nex.a.value:
                        error = 'no gap between %s and %s! in UISet %s'
                        params = (cur, nex.a.notation, self.notation)
                else:
                    if cur >= nex:
                        error = '%s >= %s in UISet %s'
                        params = (cur, nex, self.notation)
            if error:
                assert False, error % params
        return res
    return wrapper


class UISet(object):
    """
    Uncountable Infinite Set

    UISet can be instantiated from either:
        - iterable of intervals or scalars:
            UISet([Interval('[1, 2]'), Interval('[5, inf)')])
            UISet([Interval('1, 2'), 0, Interval('[6, 7]')])
        - notation string: UISet('[1, 2], {3}, [5, inf)'). Note that in this case all
            the pieces must be sorted in ascending order and must not intersect.
        - another UISet. Intervals will be copied.
        - nothing for empty UISet: UISet() 
    
    The subset and equality comparisons do not generalize to a total ordering function.
    For example, any two nonempty disjoint UISets are not equal and are not subsets of each other,
    so all of the following return False: a<b, a==b, or a>b.

    Note, the non-operator versions of union(), intersection(), difference(), and symmetric_difference(), issubset(), and issuperset() methods will accept any iterable as an argument.
    In contrast, their operator based counterparts require their arguments to be UISets.

    In boolean context UISet is True if it is not empty and False if it is empty.
    """

    def __init_from_notation(self, notation):

        a = None
        for part in notation.split(','):
            part = part.strip()
            if part.startswith('{') and part.endswith('}'):
                scalar = parse_value(part[1:-1])
                if not is_finite(scalar):
                    raise ValueError('scalar %s must be finite' % scalar)
                if self.pieces:
                    pre = self.pieces[-1]
                    if isinstance(pre, Interval):
                        pre = pre.b.value
                    if pre >= scalar:
                        raise ValueError('%s >= %s!' % (pre, scalar))
                self.pieces.append(scalar)
            else:
                value, excluded, open = parse_endpoint_notation(part)
                endpoint = Endpoint(None, value, excluded, open)
                if a is None:
                    a = endpoint
                else:
                    interval = Interval(a=a, b=endpoint)
                    if self.pieces:
                        pre = self.pieces[-1]
                        if isinstance(pre, Interval):
                            if pre.b > interval.a:
                                raise ValueError('%s > %s!' % (pre.b, interval.a))
                            if are_bounding(pre.b, interval.a):
                                raise ValueError('%s and %s have no gap!' % (pre.b, interval.a))
                        else:
                            if pre >= interval.a.value:
                                raise ValueError('%s >= %s!' % (pre, interval.a))
                    self.pieces.append(interval)
                    a = None
        if a is not None:
            raise ValueError('Invalid notation')

    @_assert_pieces_are_ascending
    def __init__(self, arg=None):
        
        if isinstance(arg, type(self)):
            # Init from UISet
            self.pieces = [i.copy() for i in arg.pieces]
            return
        self.pieces = []
        if arg is None:
            # Init empty UISet from None
            return
        elif isinstance(arg, str):
            # Init from notation string
            self.__init_from_notation(arg)
        else:
            # Init from iterable of intervals or scalars.
            for p in arg:
                self.add(p)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.pieces)

    @property
    def notation(self):
        chunks = []
        for i in self.pieces:
            if isinstance(i, Interval):
                chunks.append(i.notation)
            else:
                chunks.append('{%s}' % i)
        return ', '.join(chunks)

    def __bool__(self):
        return len(self.pieces) > 0

    def __nonzero__(self):
        return len(self.pieces) > 0

    def search(self, x, lo=0, hi=None):
        """
        Search scalar x in UISet.
        Return tuple of two elements:
            the index where to insert x in list of UISet pieces.
            piece that contains x or equals to x, or None if none found.

        Implements Binary search.
        
        Optional args lo (default 0) and hi (default len(self.pieces)) bound the
            slice of self.pieces to be searched.
        """
        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = len(self.pieces)
        while lo < hi:
            mid = (lo+hi) // 2
            piece = self.pieces[mid]
            if isinstance(piece, Interval):
                start, end = piece.a, piece.b
            else:
                start, end = piece, piece
            if end < x:
                lo = mid + 1
            elif start > x:
                hi = mid
            else:
                return mid, piece

        return lo, None

    def __contains__(self, x):
        """
        x in self
        Test scalar or interval x for membership in UISet.
        Note that if x is interval, returning True does not mean that one of
        intervals equals to x, because there can be an interval larger than x.
        """
        if isinstance(x, Interval):
            _, piece = self.search(x.a)
            return piece is not None and is_interval(piece) and x.b <= piece.b
        else:
            return self.search(x)[1] is not None
        
    @_assert_pieces_are_ascending
    def __invert__(self):
        """
        ~self
        Return a new UISet with pieces that self does not contain.
        Double inversion (~~self) returns UISet that is equal to self.
        """
        new = UISet()
        if not self.pieces:
            new.pieces.append(unbounded.copy())
            return new
        if self.pieces[0] == unbounded.copy():
            return new
        # Get plain list of endpoints from original UISet.
        endpoints = []
        for i in self.pieces:
            if isinstance(i, Interval):
                endpoints += [i.a, i.b]
            else:
                e1 = Endpoint(value=i, excluded=False, open=True)
                e2 = Endpoint(value=i, excluded=False, open=False)
                endpoints += [e1, e2]
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
        # If values of endpoints are same add scalar.
        for a, b in zip(endpoints[::2], endpoints[1::2]):
            if a.value == b.value:
                p = a.value
            else:
                p = Interval(a=a, b=b)
            new.pieces.append(p)

        return new

    def isdisjoint(self, other):
        """
        Return True if UISet has no elements in common with other.
        UISets are disjoint if and only if their intersection is the empty UISet.
        """
        raise NotImplementedError

    def __eq__(self, other):
        """
        self == other
        Test whether UISet contains all the elements of other and vice versa.
        """
        return isinstance(other, UISet) and self.pieces == other.pieces

    def __ne__(self, other):
        """
        self != other
        Test whether UISet contains at least one element that other does not contain or vice versa.
        """
        return not isinstance(other, UISet) or self.pieces != other.pieces

    def __gt__(self, other):
        """
        self > other
        Test whether the UISet is a proper superset of other.
        """
        if not isinstance(other, UISet):
            raise TypeError('Can only compare to an UISet')
        return self != other and self >= other

    def __ge__(self, other):
        """
        self >= other
        Test whether every piece in other is in the UISet.
        """
        if not isinstance(other, UISet):
            raise TypeError('Can only compare to an UISet')
        lo = 0
        X = iter(other.pieces)
        try:
            x = next(X)
            while True:
                xa, xb = isinstance(x, Interval) and (x.a, x.b) or (x, x)
                lo, p = self.search(xa, lo=lo)
                if p is None:
                    return False
                pa, pb = isinstance(p, Interval) and (p.a, p.b) or (p, p)
                if xb > pb:
                    return False
                while True:
                    x = next(X)
                    xa, xb = isinstance(x, Interval) and (x.a, x.b) or (x, x)
                    if xa >= pb or xb == pb:
                        break
                    if xb < pb:
                        continue
                    return False
        except StopIteration:
            return True
        return False

    def issuperset(self, other):
        """Test whether every element in other is in the UISet."""
        return self >= other

    def __le__(self, other):
        """
        self <= other
        Test whether every element in the UISet is in other.
        """
        if not isinstance(other, UISet):
            raise TypeError('Can only compare to an UISet')
        return NotImplemented # so that other.__ge__ will be called

    def issubset(self, other):
        """Test whether every element in the UISet is in other."""
        return self <= other

    def __lt__(self, other):
        """
        self < other
        Test whether the UISet is a proper subset of other.
        """
        if not isinstance(other, UISet):
            raise TypeError('Can only compare to an UISet')
        return NotImplemented # so that other.__gt__ will be called

    def __or__(self, other):
        """
        self | other
        Return a new UISet with merged pieces from the UISets self and other.
        """
        new = self.copy()
        lo = 0
        for x in other.pieces:
            lo = new._add(x, lo)
        return new

    def __ior__(self, other):
        """
        self |= other
        Update the UISet, adding pieces from other.
        """
        lo = 0
        for x in other.pieces:
            lo = self._add(x, lo)
        return self
        
    def union(self, *others):
        """Return a new UISet with pieces from the UISet and all others."""
        new = self.copy()
        for other in others:
            if isinstance(other, UISet):
                lo = 0
                for x in other.pieces:
                    lo = new._add(x, lo)
            else:
                for x in other:
                    new.add(x)
        return new

    def update(self, *others):
        """Update the UISet, adding pieces from all others."""
        for other in others:
            lo = 0
            for x in other.pieces:
                lo = self._add(x, lo)

    def __and__(self, other):
        """
        self & other
        Return a new UISet with elements common to the UISet and other.
        """
        raise NotImplementedError

    def intersection(self, *others):
        """Return a new UISet with elements common to the UISet and all others."""
        raise NotImplementedError

    def __sub__(self, other):
        """
        self - other
        Return a new UISet with elements in the UISet that are not in other.
        """
        raise NotImplementedError

    def difference(self, *others):
        """
        Return a new UISet with elements in the UISet that are not in the others.
        """
        raise NotImplementedError

    def __xor__(self, other):
        """
        self ^ other
        Return a new UISet with elements in either the UISet or other but not both."""
        raise NotImplementedError

    def symmetric_difference(self, other):
        """
        Return a new UISet with elements in either the UISet or other but not both."""
        raise NotImplementedError

    def __iand__(self, other):
        """
        self &= other
        Update the UISet, keeping only elements found in it and other.
        """
        raise NotImplementedError

    def intersection_update(self, *others):
        """
        Update the UISet, keeping only elements found in it and all others.
        """
        raise NotImplementedError

    def __isub__(self, other):
        """
        self -= other
        Update the UISet, removing elements found in other.
        """
        raise NotImplementedError

    def difference_update(self, *others):
        """
        Update the UISet, removing elements found in others.
        """
        raise NotImplementedError

    def __ixor__(self, other):
        """
        self ^= other
        Update the UISet, keeping only elements found in either UISet, but not in both.
        """
        raise NotImplementedError
    
    def symmetric_difference_update(self, other):
        """
        Update the UISet, keeping only elements found in either UISet, but not in both.
        """
        raise NotImplementedError

    def _add_scalar(self, x, lo=0):

        if not is_finite(x):
            raise ValueError('x must be finite')
        idx, piece = self.search(x, lo)
        if piece is not None:
            return idx
        
        pieces = self.pieces
        pre = pieces[idx-1] if idx > 0 else None
        nex = pieces[idx] if len(pieces) >= idx+1 else None
        pre, nex = (isinstance(p, Interval) and p or None for p in [pre, nex])

        if pre is not None:
            if pre.b.value == x:
                if nex is not None and nex.a.value == x:
                    # Adding b to (a, b), (b, c)
                    interval = Interval(a=pre.a.copy(), b=nex.b.copy())
                    pieces[idx-1:idx+1] = [interval]
                else:
                    # Adding b to (a, b)
                    b = Endpoint(value=x, excluded=False, open=False)
                    pieces[idx-1] = Interval(a=pre.a.copy(), b=b)
                return idx
        if nex is not None and nex.a.value == x:
            # Adding a to (a, b)
            a = Endpoint(value=x, excluded=False, open=True)
            pieces[idx] = Interval(a=a, b=nex.b.copy())
            return idx
        pieces.insert(idx, x)
        
        return idx + 1
            
    def _add_interval(self, x, lo=0):

        pieces = self.pieces
        idx1, piece1 = self.search(x.a, lo)
        idx2, piece2 = self.search(x.b, idx1)

        a = x.a.copy()
        if piece1 is not None:
            if isinstance(piece1, Interval):
                a = piece1.a.copy()
        elif idx1 > 0:
            pre = pieces[idx1-1]
            if isinstance(pre, Interval):
                if are_bounding(pre.b, x.a):
                    a = pre.a.copy()
                    idx1 -= 1
            elif pre == x.a.value:
                a = Endpoint(value=pre, excluded=False, open=True)
                idx1 -= 1

        b = x.b.copy()
        if piece2 is not None:
            idx2 += 1
            if isinstance(piece2, Interval):
                b = piece2.b.copy()
        elif len(pieces) >= idx2+1:
            nex = pieces[idx2]
            if isinstance(nex, Interval):
                if are_bounding(x.b, nex.a):
                    b = nex.b.copy()
                    idx2 += 1
            elif nex == x.b.value:
                b = Endpoint(value=nex, excluded=False, open=False)
                idx2 += 1

        pieces[idx1:idx2] = [Interval(a=a, b=b)]
        return min([idx2, len(self.pieces)])

    def _add(self, x, lo=0):
        """
        Add scalar or interval x to UISet, starting from piece at index lo.
        return index of the first piece that does not intersect with x.
        """
        if isinstance(x, Interval):
            return self._add_interval(x, lo)
        else:
            return self._add_scalar(x, lo)
        
    @_assert_pieces_are_ascending
    def add(self, x):
        """Add scalar or interval x to UISet, merge some of them if needed."""
        self._add(x)

    def _remove_scalar(self, x):

        idx, piece = self.search(x)
        if piece is None:
            return
        
        if isinstance(piece, Interval):
            if piece.a.value == x:
                piece.a.excluded = True
            elif piece.b.value == x:
                piece.b.excluded = True
            else:
                # Split interval by x.
                b1 = Endpoint(value=x, excluded=True, open=False)
                i1 = Interval(a=piece.a, b=b1)
                a2 = Endpoint(value=x, excluded=True, open=True)
                i2 = Interval(a=a2, b=piece.b)
                self.pieces[idx:idx+1] = [i1, i2]
        else:
            self.pieces[idx:idx+1] = []


    def _remove_interval(self, x):

        pieces = self.pieces
        idx1, piece1 = self.search(x.a)
        idx2, piece2 = self.search(x.b, idx1)

        if piece1 is piece2 and piece1 is not None: # so they are both are Intervals
            new_pieces = []
            if x.a.value == piece1.a.value:
                if x.a.excluded and not piece1.a.excluded:
                    new_pieces.append(x.a.value)
            else:
                new_pieces.append(Interval(a=piece1.a, b=~x.a))
            if x.b.value == piece1.b.value:
                if x.b.excluded and not piece1.b.excluded:
                    new_pieces.append(x.b.value)
            else:
                new_pieces.append(Interval(a=~x.b, b=piece2.b))
            pieces[idx1:idx1+1] = new_pieces
            return

        if piece1 is not None:
            if isinstance(piece1, Interval):
                if x.a.value == piece1.a.value:
                    if x.a.excluded and not piece1.a.excluded:
                        pieces[idx1] = x.a.value
                        idx1 += 1
                else:
                    piece1.b = ~x.a
                    idx1 += 1

        if piece2 is not None:
            if isinstance(piece2, Interval):
                if x.b.value == piece2.b.value:
                    if x.b.excluded and not piece2.b.excluded:
                        pieces[idx2] = x.b.value
                    else:
                        idx2 += 1
                else:
                    piece2.a = ~x.b
            else:
                idx2 += 1

        pieces[idx1:idx2] = []

    @_assert_pieces_are_ascending
    def remove(self, x):
        """Remove scalar or interval x from the UISet."""
        if isinstance(x, Interval):
            self._remove_interval(x)
        else:
            self._remove_scalar(x)

    def clear(self):
        """Remove all pieces from the UISet."""
        self.pieces = []

    def copy(self):
        """
        Return a copy of an UISet.
        Intervals are recreated.
        copy is safe as long as endpoint values are of immutable types.
        """
        new = UISet()
        new.pieces = [p.copy() if is_interval(p) else p for p in self.pieces]
        return new

