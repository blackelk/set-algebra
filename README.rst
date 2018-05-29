Algebra of sets in python
=================================

| How to have a set containing all real numbers from 1 to 10 not including 10?
| How to add interval from 20 to 30 to the set?
| How to make sure this set is a subset of set of positive numbers?
| How to add scalar number to it?
| How to get complement of the set?

.. code:: python

    >>> from uiset import Interval, Set
    >>> s = Set('[1, 10)')
    >>> 1 in s
    True
    >>> 10 in s
    False
    >>> s.add(Interval('[20, 30]'))
    >>> 25 in s
    True
    >>> s <= Set('(0, inf)')
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


uiset fully supports Python3. Tested on python 2.7, 3.2 - 3.6.

