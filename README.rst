uiset
=====

| How to have a set containing all numbers from 1 to 10 not including 10?
| How to add interval from 20 to 30 to that set?
| How to make sure this set is a subset of set of positive numbers?

.. code:: python

    >>> from uiset import Interval, UISet
    >>> s = UISet('[1, 10)')
    >>> 5 in s
    True
    >>> 10 in s
    False
    >>> s.add(Interval('[20, 30]'))
    >>> 25 in s
    True
    >>> s <= UISet('(0, inf)')
    True

uiset provides classes representing math concepts:

- Infinity
- Endpoint
- Interval
- Uncountable Infinite Set

Besides numbers, uiset can contain any objects that can be compared to each other - strings, datetimes, etc.

Infinity() is greater than any of these objects except float('inf') and float('nan').
NegativeInfinity included as well.


uiset is written in Python3.

