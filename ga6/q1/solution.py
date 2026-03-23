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
