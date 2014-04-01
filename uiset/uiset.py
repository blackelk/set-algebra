class uiset:
    """
    Uncountable Infinite Set
    
    The subset and equality comparisons do not generalize to a total ordering function.
    For example, any two nonempty disjoint uisets are not equal and are not subsets of each other,
    so all of the following return False: a<b, a==b, or a>b.

    Note, the non-operator versions of union(), intersection(), difference(), and symmetric_difference(), issubset(), and issuperset() methods will accept any iterable as an argument.
    In contrast, their operator based counterparts require their arguments to be uisets.

    Note, the elem argument to the __contains__(), remove(), and discard() methods may be an uiset.
    """

    def __init__(self, elements):
        pass

    def __repr__(self):
        pass

    def __contains__(self, x):
        """
        x in self
        Test x for membership in uiset.
        """
    
    def __invert__(self):
        """
        ~self
        Return a new uiset with elements that self does not contain.
        Double inversion (~~self) returns uiset that is equal to self.
        """

    # TODO: maybe slicing?

    def isdisjoint(self, other):
        """
        Return True if uiset has no elements in common with other.
        Uisets are disjoint if and only if their intersection is the empty uiset.
        """

    def __eq__(self, other):
        """
        self == other
        Test whether uiset contains all the elements of other and vice versa.
        """

    def __ne__(self, other):
        """
        self != other
        Test whether uiset contains at least one element that other does not contain or vice versa.
        """

    def __gt__(self, other):
        """
        self > other
        Test whether the uiset is a proper superset of other.
        """

    def __ge__(self, other):
        """
        self >= other
        Test whether every element in other is in the uiset.
        """

    def issuperset(self, other):
        """Test whether every element in other is in the uiset."""
        # same as __ge__

    def __le__(self, other):
        """
        self <= other
        Test whether every element in the uiset is in other.
        """

    def issubset(self, other):
        """Test whether every element in the uiset is in other."""
        # same as __le__

    def __lt__(self, other):
        """
        self < other
        Test whether the uiset is a proper subset of other.
        """

    def __or__(self, other):
        """
        self | other
        Return a new uiset with elements from the uiset and other.
        """

    def union(self, *others):
        """Return a new uiset with elements from the uiset and all others."""
        # same as __or__

    def __and__(self, other):
        """
        self & other
        Return a new uiset with elements common to the uiset and other.
        """

    def intersection(self, *others):
        """Return a new uiset with elements common to the uiset and all others."""
        # same as __and__

    def __sub__(self, other):
        """
        self - other
        Return a new uiset with elements in the uiset that are not in other.
        """

    def difference(self, *others):
        """
        Return a new uiset with elements in the uiset that are not in the others.
        """
        # same as __sub__

    def __xor__(self, other):
        """
        self ^ other
        Return a new uiset with elements in either the uiset or other but not both."""

    def symmetric_difference(self, other):
        """
        Return a new uiset with elements in either the uiset or other but not both."""
        # same as __xor__

    def __ior__(self, other):
        """
        self |= other
        Update the uiset, adding elements from other.
        """

    def update(self, *others):
        """
        Update the uiset, adding elements from all others.
        """
        # same as __ior__

    def __iand__(self, other):
        """
        self &= other
        Update the uiset, keeping only elements found in it and other.
        """

    def intersection_update(self, *others):
        """
        Update the uiset, keeping only elements found in it and all others.
        """

    def __isub__(self, other):
        """
        self -= other
        Update the uiset, removing elements found in other.
        """

    def difference_update(self, *others):
        """
        Update the uiset, removing elements found in others.
        """

    def __ixor__(self, other):
        """
        self ^= other
        Update the uiset, keeping only elements found in either uiset, but not in both.
        """
    
    def symmetric_difference_update(self, other):
        """
        Update the uiset, keeping only elements found in either uiset, but not in both.
        """

    def add(self, elem):
        """Add element elem to the uiset."""

    def remove(self, elem):
        """Remove element elem from the uiset.
        Raises KeyError if elem is not contained in the uiset."""

    def discard(self, elem):
        """Remove element elem from the uiset if it is present."""

    def pop(self):
        """
        Remove and return an arbitrary element from the uiset.
        Raises KeyError if the uiset is empty."""

    def clear(self):
        """Remove all elements from the uiset."""

