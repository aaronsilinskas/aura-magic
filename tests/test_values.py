import pytest
from aura.values import MinMaxValue


class TestMinMaxValue:
    def test_initialization(self):
        m = MinMaxValue(value=10, min=0, max=20)
        assert m.value == 10
        assert m.min == 0
        assert m.max == 20

    def test_clamping_below_min(self):
        m = MinMaxValue(value=10, min=0, max=20)
        m.value = -5
        assert m.value == 0

    def test_clamping_above_max(self):
        m = MinMaxValue(value=10, min=0, max=20)
        m.value = 25
        assert m.value == 20

    def test_clamping_min_update(self):
        m = MinMaxValue(value=10, min=0, max=20)
        m.min = 15
        assert m.value == 15

    def test_clamping_max_update(self):
        m = MinMaxValue(value=10, min=0, max=20)
        m.max = 5
        assert m.value == 5

    def test_setting_value_within_bounds(self):
        m = MinMaxValue(value=10, min=0, max=20)
        m.value = 15
        assert m.value == 15
