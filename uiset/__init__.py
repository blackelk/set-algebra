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
__version__ = '0.1.0'
__author__ = 'Constantine Parkhimovich'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Constantine Parkhimovich'


from uiset.infinity import Infinity, NegativeInfinity, is_finite, inf, neg_inf
from uiset.endpoint import Endpoint
from uiset.interval import Interval, is_scalar, unbounded
from uiset.uiset import UISet
