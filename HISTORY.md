## 0.4.0.dev2
#### 2026 April 12
- Infinity ordering semantics refined:
    - comparisons apply only to orderable values
    - propagate comparisons via reflected operators
    - treat `NaN` as unordered.
    - `is_finite()` no longer considers `NaN` finite.
- `Interval.is_degenerate` property
- Fixed `Set.update()` to accept iterables in addition to Set instances
- Collapse degenerate intervals into scalars when adding/removing them to/from `Set`
- Tested on python3.12 - 3.14
- Discontinued python <3.10 support
- Added type annotations
- Set comparisons now return `NotImplemented` (instead of raising TypeError) when the other operand is not a `Set`


## 0.3.6
#### 2024 March 30
- Tested on python3.10 - 3.11


## 0.3.5
##### 2018 June 16
- Renamed `excluded` to `open`


## 0.3.4
##### 2018 June 3
- Renamed `open` to `left`, `closed` to `right`


## 0.3.3
##### 2018 June 3
- Init `Interval` from two values and bounds string


## 0.3.2
##### 2018 June 1
- Renamed `uiset` to `set-algebra`


## 0.3.1
##### 2018 May 29
- Renamed `UISet` to `Set`


## 0.3.0
##### 2018 May 27
- Init `Endpoint` from value and bound character


## 0.2.2
##### 2014 June 20
- Released on PyPI


##### 2014 June 18
- `Set.isdisjoint()`
- `Set.__and__()`
- `Set.__iand__()`
- `Set.intersection()`
- `Set.intersection_update()`


## 0.2.1
##### 2014 June 16
- `Set.__xor__()`
- `Set.__ixor__()`
- `Set.symmetric\_difference()`
- `Set.symmetric_difference_update()`
- `Set.__sub__()`
- `Set.__isub__()`
- `Set.difference()`
- `Set.difference_update()`
- `Set.__or__()`
- `Set.__ior__()`
- `Set.union()`
- `Set.update()`
- `Set.__gt__`
- `Set.__lt__`


## 0.2.0
##### 2014 May 3
- `Set` supports scalars
- `Set.issubset()`
- `Set.issuperset()`
- `Set.__le__()`
- `Interval() in Set()`
- `Set.__ge__()`
- `Set.copy()`
- `Set.__init__` from notation
- `Set.__eq__()`
- `Set.__ne__()`
- `Set.__repr__()`
- `Set.notation()`
- `Set.clear()`
- `Set.discard()`
- `Set.search()`
- `Set.__contains__()`
- `Set.__bool__`
- `Set.__invert__()`
- `Set.add()`
- `Endpoint.copy()`
- `Interval.copy()`


## 0.1.0
##### 2014 Apr 1
- `Endpoint`
- `Interval`
- `Infinity`
- `NegativeInfinity`
