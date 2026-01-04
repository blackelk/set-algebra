## 0.4.0
#### 2026 January 4
- Infinity ordering semantics refined:
    - comparisons apply only to orderable values
    - propagate comparisons via reflected operators
    - treat NaN as unordered.
    - is\_finite() no longer considers NaN finite.
- Interval.is\_degenerate property
- Collapse degenerate intervals into scalars when adding/removing them to/from Set
- Tested on python3.12 - 3.13
- Discontinued python <3.10 support


## 0.3.6
#### 2024 March 30
- Tested on python3.10 - 3.11


## 0.3.5
##### 2018 June 16
Renamed excluded to open


## 0.3.4
##### 2018 June 3
Renamed open to left, closed to right


## 0.3.3
##### 2018 June 3
Init Interval from two values and bounds string


## 0.3.2
##### 2018 June 1
uiset -> set-algebra


## 0.3.1
##### 2018 May 29
- UISet -> Set


## 0.3.0
##### 2018 May 27
0.3.0 Init Endpoint from value and bound character


## 0.2.2
##### 2014 June 20
- Released on PyPI

##### 2014 June 18
- Set.isdisjoint()
- Set.\_\_and\_\_()
- Set.\_\_iand\_\_()
- Set.intersection()
- Set.intersection\_update()


## 0.2.1
##### 2014 June 16
- Set.\_\_xor\_\_()
- Set.\_\_ixor\_\_()
- Set.symmetric\_difference()
- Set.symmetric\_difference\_update()
- Set.\_\_sub\_\_()
- Set.\_\_isub\_\_()
- Set.difference()
- Set.difference\_update()
- Set.\_\_or\_\_()
- Set.\_ior\_\_()
- Set.union()
- Set.update()
- Set.\_\_gt\_\_
- Set.\_\_lt\_\_


## 0.2.0
##### 2014 May 3
- Scalars for Set
- Set.issubset()
- Set.issuperset()
- Set.\_\_le\_\_()
- Interval() in Set()
- Set.\_\_ge\_\_()
- Set.copy()
- Set.\_\_init\_\_ from notation
- Set.\_\_eq\_\_()
- Set.\_\_ne\_\_()
- Set.\_\_repr\_\_()
- Set.notation()
- Set.clear()
- Set.discard()
- Set.search()
- Set.\_\_contains\_\_()
- Set.\_\_bool\_\_
- Set.\_\_invert\_\_()
- Set.add()
- Endpoint.copy()
- Interval.copy()


## 0.1.0
##### 2014 Apr 1
- Endpoint
- Interval
- Infinity
- NegativeInfinity
