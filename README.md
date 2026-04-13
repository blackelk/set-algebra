# set-algebra

`set-algebra` is a Python library for working with mathematical sets built from intervals and singleton values.

It provides four core concepts:

- `Infinity` and `NegativeInfinity`
- `Endpoint`
- `Interval`
- `Set`

The library is designed for cases where you need interval-aware set logic rather than plain Python hash sets.<br>
It supports open and closed bounds, unbounded intervals, singleton points, membership checks, complements, unions, intersections, differences, and symmetric differences.

It can also be useful for schedule calculations, such as [finding overlapping meeting times](#scheduling-and-availability) between multiple people.

**All code examples in this README are automatically extracted and tested to ensure they stay correct.**


## What the library does

`set-algebra` models subsets of an ordered axis.

That axis is usually numeric, and the string parser is numeric-focused, but the core `Endpoint`, `Interval`, and `Set` classes can also work with other comparable values when you construct them directly instead of parsing from strings.

Examples of supported representations:

- a single point: `{3}`
- a closed interval: `[1, 5]`
- an open interval: `(1, 5)`
- an unbounded interval: `(-inf, 10]`
- a mixed set: `[1, 2], {3}, (5, inf)`


## Installation

```bash
pip install set-algebra
```

## Quick start

```python
>>> from set_algebra import Interval, Set

>>> percentage = Interval('[0, 100]')
>>> 50 in percentage
True
>>> 200 in percentage
False

>>> negative = Interval('(-inf, 0)')
>>> -1 in negative
True
>>> 0 in negative
False

>>> s = Set('[1, 2], {3}')
>>> 1.5 in s
True
>>> 2 in s
True
>>> 3 in s
True
>>> 4 in s
False
>>> 100 in s
False
>>> s |= Set('[5, inf)')
>>> 100 in s
True
```

## Public API

### `Infinity`, `NegativeInfinity`, `inf`, `neg_inf`

Special objects representing positive and negative infinity.

```python
>>> from set_algebra import inf, neg_inf

>>> inf > 10000000000
True
>>> neg_inf < -1.e20
True
>>> -inf == neg_inf
True
>>> -inf == -inf
True
```

Use unary minus on the library objects:

```python
>>> from set_algebra import inf, neg_inf

>>> -inf is neg_inf
True
>>> -neg_inf is inf
True
```

Use `is_finite(x)` to test whether a value is neither infinity nor NaN:
```python
>>> from set_algebra import inf, is_finite

>>> is_finite(inf)
False
>>> is_finite(float('inf'))
False
>>> is_finite(999)
True
```

### `Endpoint`

Represents one boundary point of an interval.

Four endpoint forms are supported:

- `[1`   left-closed
- `(1`   left-open
- `1]`   right-closed
- `1)`   right-open

Construction styles:

```python
>>> from set_algebra import Endpoint

>>> Endpoint('[1')
Endpoint('[1')

>>> Endpoint('3)')
Endpoint('3)')

>>> Endpoint('(-inf')
Endpoint('(-inf')

>>> Endpoint(1, '[')
Endpoint('[1')

>>> Endpoint(3, ')')
Endpoint('3)')
```

Endpoints can be compared with scalars and with other endpoints.

```python
>>> from set_algebra import Endpoint

>>> Endpoint('[1') <= 1
True
>>> Endpoint('(1') <= 1
False
>>> Endpoint('1]') == 1
True
>>> Endpoint('1)') == 1
False
```

Bitwise inversion flips side and openness while keeping the same value:

```python
>>> from set_algebra import Endpoint

>>> ~Endpoint('[7')
Endpoint('7)')
>>> ~Endpoint('3]')
Endpoint('(3')
```

Use `are_bounding(e1, e2)` to check whether two opposite-side endpoints touch with no gap between them.

```python
>>> from set_algebra import are_bounding, Endpoint

>>> are_bounding( Endpoint('7)'), Endpoint('[7') )
True
>>> are_bounding( Endpoint('7)'), Endpoint('(7') )
False
```

### `Interval`

Represents a single interval with two endpoints, `a` and `b`.

Construction styles:

```python
>>> from set_algebra import Interval, Endpoint

>>> Interval('[0, 1]')
Interval('[0, 1]')

>>> Interval(1, 2, '[)')
Interval('[1, 2)')

>>> Interval(Endpoint('(-1'), Endpoint('1]'))
Interval('(-1, 1]')
```

#### Interval Membership

- scalar in interval
- endpoint in interval
- interval in interval

```python
>>> from set_algebra import Interval

>>> real = Interval('(-inf, inf)')
>>> 999 in real
True

>>> percentage = Interval('[0, 100]')
>>> 50 in percentage
True
>>> 200 in percentage
False

>>> small = Interval('[10, 20]')
>>> small in percentage
True
```

#### Useful attributes and methods

- `a`, `b`: left and right endpoints
- `notation`: normalized interval notation
- `is_degenerate`: whether both endpoint values are equal
- `copy()`

A predefined unbounded interval is also available:

```python
>>> from set_algebra import unbounded
>>> unbounded
Interval('(-inf, inf)')
```

### `Set`

Represents a set as an ordered sequence of non-overlapping pieces, where each piece is either:

- an `Interval`
- a singleton scalar value

#### Construction styles

```python
>>> from set_algebra import Set, Interval

>>> Set()
Set([])

>>> Set('[1, 2], {3}, [5, inf)')
Set([Interval('[1, 2]'), 3, Interval('[5, inf)')])

>>> Set([Interval('[1, 2]'), 3, Interval('[5, inf)')])
Set([Interval('[1, 2]'), 3, Interval('[5, inf)')])

>>> Set(Set('[1, 2], {3}'))
Set([Interval('[1, 2]'), 3])

>>> Set('[1, 2], {3}')
Set([Interval('[1, 2]'), 3])
```

The notation parser for `Set` expects pieces in ascending order with gaps between them. Adjacent or overlapping pieces must be represented in their merged form.

Valid:

```python
Set('[1, 2], {4}, [6, 7]')
```

Invalid because there is no gap between pieces:

```python
Set('[1, 2], {2}')
Set('[1, 2], (2, 3)')
```

#### Set Membership

```python
>>> from set_algebra import Set, Interval
>>> s = Set('[1, 2], {3}, [5, 10)')

>>> 1 in s
True
>>> 3 in s
True
>>> 4 in s
False
>>> Interval('[6, 7]') in s
True
```

#### Boolean value

```python
>>> from set_algebra import Set
>>> bool(Set())
False
>>> bool(Set('{10}'))
True
```

#### Set operations

Operator forms require another `Set`.

```python
>>> from set_algebra import Set

>>> a = Set('[1, 5]')
>>> b = Set('[4, 10]')

>>> a | b  # union
Set([Interval('[1, 10]')])

>>> a & b  # intersection
Set([Interval('[4, 5]')])

>>> a - b  # difference
Set([Interval('[1, 4)')])

>>> a ^ b  # symmetric difference
Set([Interval('[1, 4)'), Interval('(5, 10]')])

>>> ~a  # complement relative to (-inf, inf)
Set([Interval('(-inf, 1)'), Interval('(5, inf)')])
```

Method forms are more permissive and also accept iterables of intervals and/or scalars:

```python
>>> from set_algebra import Set, Interval
>>> a = Set('[1, 5]')

>>> a.union([6, Interval('[10, 12]')])
Set([Interval('[1, 5]'), 6, Interval('[10, 12]')])

>>> a.intersection([Interval('[3, 4]')])
Set([Interval('[3, 4]')])

>>> a.difference([2, 3])
Set([Interval('[1, 2)'), Interval('(2, 3)'), Interval('(3, 5]')])
```

#### In-place mutating operators

`Set` supports mutating operators that modify the object in place:

- `|=`: union update
- `&=`: intersection update
- `-=`: difference update
- `^=`: symmetric difference update

```python
>>> from set_algebra import Set

>>> s = Set('[0, 5)')
>>> s |= Set('[10, 20]')
>>> s.notation
'[0, 5), [10, 20]'

>>> s &= Set('[3, 12]')
>>> s.notation
'[3, 5), [10, 12]'

>>> s -= Set('{4}, [11, 20]')
>>> s.notation
'[3, 4), (4, 5), [10, 11)'

>>> s ^= Set('[0, 3], {10}')
>>> s.notation
'[0, 3), (3, 4), (4, 5), (10, 11)'
```

#### Supported mutating methods

- `add(x)`
- `remove(x)`
- `clear()`
- `update(*others)`
- `intersection_update(*others)`
- `difference_update(*others)`
- `symmetric_difference_update(*others)`

###### `add(x)`

```python
>>> from set_algebra import Set, Interval

>>> s = Set('[0, 5]')
>>> s.add(10)
>>> s.notation
'[0, 5], {10}'

>>> s.add(Interval('[7, 9]'))
>>> s.notation
'[0, 5], [7, 9], {10}'
```

###### `remove(x)`

```python
>>> from set_algebra import Set

>>> s = Set('[0, 10]')
>>> s.remove(5)
>>> s.notation
'[0, 5), (5, 10]'
```

Unlike Python built-in `set.remove(x)`, `Set.remove(x)` does not raise an exception when `x` is not present:

```python
>>> from set_algebra import Set

>>> s = Set('[0, 5]')
>>> s.remove(10)
>>> s.notation
'[0, 5]'
```
Because removal is already tolerant of missing values, there is no separate discard() method.


###### `clear()`

```python
>>> from set_algebra import Set

>>> s = Set('[0, 5], {10}')

>>> bool(s)
True

>>> s.clear()
>>> bool(s)
False

>>> s.notation
''
```

###### `update(*others)`

```python
>>> from set_algebra import Set, Interval

>>> s = Set('[0, 5]')
>>> s.update(
...     Set('[10, 20]'),
...     [30,    Interval('[40, 50]')],
... )
>>> s.notation
'[0, 5], [10, 20], {30}, [40, 50]'
```

###### `intersection_update(*others)`

```python
>>> from set_algebra import Set, Interval

>>> s = Set('[0, 20]')
>>> s.intersection_update(
...     Set('[5, 15]'),
...     [Interval('[10, 25]')],
... )
>>> s.notation
'[10, 15]'
```

#### Supported comparison operators

- `a == b`
- `a != b`
- `a > b`
- `a >= b`
- `a < b`
- `a <= b`

###### Equality and inequality

```python
>>> from set_algebra import Set

>>> Set('[0, 5]') == Set('[0, 5]')
True

>>> Set('[0, 5]') != Set('[0, 10]')
True

>>> Set('[0, 5]') == Set('[0, 5], {10}')
False
```

###### Superset and proper superset

```python
>>> from set_algebra import Set

>>> Set('[0, 10]') >= Set('[2, 4]')
True

>>> Set('[0, 10]') >= Set('[2, 12]')
False

>>> Set('[0, 10]') > Set('[2, 4]')
True

>>> Set('[0, 10]') > Set('[0, 10]')
False
```

###### Subset and proper subset

```python
>>> from set_algebra import Set

>>> Set('[2, 4]') <= Set('[0, 10]')
True

>>> Set('[2, 12]') <= Set('[0, 10]')
False

>>> Set('[2, 4]') < Set('[0, 10]')
True

>>> Set('[0, 10]') < Set('[0, 10]')
False
```

Two nonempty disjoint sets are neither subsets nor supersets of each other:

```python
>>> from set_algebra import Set

>>> a = Set('[0, 5]')
>>> b = Set('[10, 20]')

>>> a < b
False

>>> a > b
False

>>> a == b
False
```

#### Supported query methods

- `search(x)`
- `issubset(other)`
- `issuperset(other)`
- `isdisjoint(other)`
- `copy()`

###### `search(x)`

```python
>>> from set_algebra import Set, Interval

>>> s = Set('[0, 5], {10}, [20, 30]')
>>> s.search(3)
(0, Interval('[0, 5]'))

>>> s.search(10)
(1, 10)

>>> s.search(15)
(2, None)

>>> s.search(25)
(2, Interval('[20, 30]'))
```

###### `issubset(other)`

```python
>>> from set_algebra import Set, Interval

>>> Set('[2, 4]').issubset(Set('[0, 10]'))
True

>>> Set('[2, 12]').issubset(Set('[0, 10]'))
False

>>> Set('[2, 4]').issubset([Interval('[0, 10]')])
True
```

###### `issuperset(other)`

```python
>>> from set_algebra import Set, Interval

>>> Set('[0, 10]').issuperset(Set('[2, 4]'))
True

>>> Set('[0, 10]').issuperset(Set('[2, 12]'))
False

>>> Set('[0, 10]').issuperset([Interval('[2, 4]')])
True
```

###### `isdisjoint(other)`

```python
>>> from set_algebra import Set

>>> Set('[0, 5]').isdisjoint(Set('[10, 20]'))
True

>>> Set('[0, 5]').isdisjoint(Set('[3, 10]'))
False

>>> Set('{5}').isdisjoint(Set('(5, 10]'))
True
```

###### `copy()`

```python
>>> from set_algebra import Set

>>> s1 = Set('[0, 5]')
>>> s2 = s1.copy()

>>> s1 == s2
True

>>> s1 is s2
False

>>> s2.add(10)
>>> s1.notation
'[0, 5]'

>>> s2.notation
'[0, 5], {10}'
```

### Parser helpers

The parser module provides helpers used by notation-based constructors:

- `parse_value()`
- `parse_bound()`
- `parse_endpoint_notation()`

These parse numeric strings, bounds, infinities, and endpoint notation.


## Important behavior notes

### String parsing is numeric-oriented

Notation strings such as `"[1, 2]"` or `"(-inf, 5]"` parse values as:

- `int`
- `float`
- `inf`
- `neg_inf`

If you need intervals over non-numeric comparable values, construct `Endpoint` and `Interval` directly:

```python
>>> from set_algebra import Endpoint, Interval

>>> left = Endpoint('p', '[')
>>> right = Endpoint('z', ']')
>>> letters = Interval(left, right)
>>> 'r' in letters
True
>>> 'sA' in letters # because 'p' <= 'sA' <= 'z'
True
```

### Degenerate intervals

An interval whose endpoint values are equal is considered degenerate.

For `Set`, only the closed form `[a, a]` contributes a point. Other degenerate bound combinations are treated as empty when added or removed from a set.

### `Set` stores normalized pieces

When you add overlapping or touching pieces, `Set` merges them into the minimal normalized representation.

```python
>>> from set_algebra import Set, Interval

>>> s = Set()
>>> s.add(Interval('[1, 2)'))
>>> s.add(2)
>>> s.add(Interval('(2, 3]'))

>>> s.notation
'[1, 3]'
```

### Complement is relative to the whole axis

The complement operator `~` means complement within `(-inf, inf)`, not relative to some custom universe.


## Examples

### Interval containment

```python
>>> from set_algebra import Interval

>>> outer = Interval('[0, 100]')
>>> inner = Interval('[20, 30]')
>>> inner in outer
True
```

### Mixed set construction

```python
from set_algebra import Set

s = Set('[1, 2], {4}, (10, 20]')
print(s.notation)
# [1, 2], {4}, (10, 20]
```

### Union and difference

```python
from set_algebra import Set

A = Set('[1, 5], {10}')
B = Set('[4, 8]')

print((A | B).notation)
# [1, 8], {10}

print((A - B).notation)
# [1, 4), {10}
```

### Complement

```python
from set_algebra import Set

s = Set('[0, 1], {3}')
print((~s).notation)
# (-inf, 0), (1, 3), (3, inf)
```

### Scheduling and Availability

Alice can meet on 2026-04-12 from 10:00 to 14:00, and on 2026-04-14 from 13:00 to 15:00.<br>
Bob can meet on 2026-04-12 from 12:00 to 16:00.<br>
Find the time when they are both available.

```python
>>> from datetime import date, datetime, time

>>> from set_algebra import Interval, Set

>>> apr12 = date(2026, 4, 12)
>>> apr14 = date(2026, 4, 14)

>>> alice = Set([
...    Interval(
...        datetime.combine(apr12, time(10, 0)),
...        datetime.combine(apr12, time(14, 0)),
...        '[]',
...    ),
...    Interval(
...        datetime.combine(apr14, time(13, 0)),
...        datetime.combine(apr14, time(15, 0)),
...        '[]',
...    ),
... ])

>>> bob = Set([
...    Interval(
...        datetime.combine(apr12, time(12, 0)),
...        datetime.combine(apr12, time(16, 0)),
...        '[]',
...    ),
... ])

>>> common = alice & bob
>>> common.notation
'[2026-04-12 12:00:00, 2026-04-12 14:00:00]'
```


## Exported names

The package exports the following names from `set_algebra.__init__`:

```
Endpoint
are_bounding
Infinity
NegativeInfinity
is_finite
inf
neg_inf
Interval
is_interval
is_scalar
unbounded
Set
```


## License

MIT
