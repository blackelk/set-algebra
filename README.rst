uiset
=====

| How to have a set containing all numbers from 1 to 10 not including 10?
| How to add interval from 20 to 30 to that set?
| How to make sure this set is a subset of set of positive numbers?
| How to add scalar number to it?
| How to invert that set?

.. code:: python

    >>> from uiset import Interval, UISet
    >>> s = UISet('[1, 10)')
    >>> 1 in s
    True
    >>> 10 in s
    False
    >>> s.add(Interval('[20, 30]'))
    >>> 25 in s
    True
    >>> s <= UISet('(0, inf)')
    True
    >>> s.add(100)
    >>> s.notation
    '[1, 10), [20, 30], {100}'
    >>> (~s).notation
    '(-inf, 1), [10, 20), (30, 100), (100, inf)'

uiset provides classes representing math concepts:

- Infinity
- Endpoint
- Interval
- Uncountable Infinite Set

Besides numbers, uiset supports all objects that can be compared to each other - strings, datetimes, etc.

Infinity() is greater than any of these objects except float('inf') and float('nan').
NegativeInfinity included as well.


uiset fully supports Python3. Tested on python 2.7, 3.2, 3.3, 3.4.

Not yet implemented features
----------------------------
uiset is under active development. Currently, the following UISet methods are not implemented:

| isdisjoint
| __and__
| __iand__
| intersection
| intersection_update
| __xor__
| __ixor__
| symmetric_difference
| symmetric_difference_update

