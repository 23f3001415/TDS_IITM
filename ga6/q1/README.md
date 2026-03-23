# Q1: The Bug Hunter (Property-Based Testing)

## ELI15 Step-by-Step (Complete Beginner)

1. A normal unit test checks a few hand-picked inputs like `[3, 1, 2]`.
2. A property-based test asks Hypothesis to generate many inputs automatically.
3. The bug hint says duplicates near even indices are important.
4. With plain integers, swapping equal numbers is invisible because `5` and `5` look identical.
5. So we make tiny objects that have:
   - a `value` used for sorting
   - a `tag` used only to remember original order
6. Two objects can have the same `value` but different `tag`, like:
   - `RankedValue(value=7, tag=0)`
   - `RankedValue(value=7, tag=1)`
7. A correct stable sort should keep equal-valued items in the same order they started.
8. The buggy function swaps adjacent equal-valued items when the left index is even.
9. That means the `tag` order changes, and our property test catches it.
10. We let Hypothesis generate:
    - one integer called `duplicated_value`
    - one tail list of more integers
11. Then inside the test we build a list starting with `[duplicated_value, duplicated_value, ...tail]`.
12. We compare:
   - `sort_ranked_queue(items)`
   - Python's stable `sorted(items, key=lambda item: item.value)`
13. If both `value` order and `tag` order match, the test passes.
14. On the buggy implementation, Hypothesis quickly finds a counterexample.
15. On the reference implementation, the test should pass.

## Why This Works

- `value` checks the list is actually sorted.
- `tag` checks equal-valued items keep their original relative order.
- That second check is what exposes the hidden duplicate-swap bug.

## Final Answer To Submit

```python
from dataclasses import dataclass

from hypothesis import given, strategies as st


@dataclass(frozen=True)
class RankedValue:
    value: int
    tag: int

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return isinstance(other, RankedValue) and self.value == other.value


@given(st.integers(), st.lists(st.integers(), max_size=8))
def test_sort_ranked_queue_matches_stable_sorted_order(duplicated_value, tail):
    values = [duplicated_value, duplicated_value, *tail]
    items = [RankedValue(value=v, tag=i) for i, v in enumerate(values)]
    result = sort_ranked_queue(items)
    expected = sorted(items, key=lambda item: item.value)

    assert [item.value for item in result] == [item.value for item in expected]
    assert [item.tag for item in result] == [item.tag for item in expected]
```

Submit exactly that code.
