"""
UISet Library

Algebra of sets. Provides:
    Infinity, Negative Infinity
    Endpoint
    Interval
    Set
"""

__title__ = 'uiset'
__version__ = '0.3.1'
__author__ = 'Constantine Parkhimovich'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014-2018 Constantine Parkhimovich'


from uiset.endpoint import Endpoint, are_bounding
from uiset.infinity import Infinity, NegativeInfinity, is_finite, inf, neg_inf
from uiset.interval import Interval, is_interval, is_scalar, unbounded
from uiset.set_ import Set

