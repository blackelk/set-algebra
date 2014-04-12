class UISet:
    """
    Uncountable Infinite Set
    
    The subset and equality comparisons do not generalize to a total ordering function.
    For example, any two nonempty disjoint UISets are not equal and are not subsets of each other,
    so all of the following return False: a<b, a==b, or a>b.

    Note, the non-operator versions of union(), intersection(), difference(), and symmetric_difference(), issubset(), and issuperset() methods will accept any iterable as an argument.
    In contrast, their operator based counterparts require their arguments to be UISets.

    Note, the elem argument to the __contains__(), remove(), and discard() methods may be an UISet.
    """

    def __init__(self, intervals):
        self.intervals = []
        for interval in intervals:
            self.add(interval)

    def __repr__(self):
        pass

    def __contains__(self, x):
        """
        x in self
        Test x for membership in UISet.
        """
    
    def __invert__(self):
        """
        ~self
        Return a new UISet with elements that self does not contain.
        Double inversion (~~self) returns UISet that is equal to self.
        """

    # TODO: maybe slicing?

    def isdisjoint(self, other):
        """
        Return True if UISet has no elements in common with other.
        Uisets are disjoint if and only if their intersection is the empty UISet.
        """

    def __eq__(self, other):
        """
        self == other
        Test whether UISet contains all the elements of other and vice versa.
        """

    def __ne__(self, other):
        """
        self != other
        Test whether UISet contains at least one element that other does not contain or vice versa.
        """

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

    def issuperset(self, other):
        """Test whether every element in other is in the UISet."""
        # same as __ge__

    def __le__(self, other):
        """
        self <= other
        Test whether every element in the UISet is in other.
        """

    def issubset(self, other):
        """Test whether every element in the UISet is in other."""
        # same as __le__

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

    def add(self, new):
        """Merge existing intervals with a new one."""
        for n, i in enumerate(self.intervals):
            if i.b < new.a:
                continue
            if i.a > new.b:
                self.intervals.insert(n, new)
                return
            if i.a > new.a:
                i.a = new.a
            if new.b > i.b:
                i.b = new.b
            return
        self.intervals.append(new)

    def remove(self, elem):
        """Remove element elem from the UISet.
        Raises KeyError if elem is not contained in the UISet."""

    def discard(self, elem):
        """Remove element elem from the UISet if it is present."""

    def pop(self):
        """
        Remove and return an arbitrary element from the UISet.
        Raises KeyError if the UISet is empty."""

    def clear(self):
        """Remove all elements from the UISet."""

