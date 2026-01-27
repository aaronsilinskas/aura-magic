from aura.values import MinMaxValue, ValueModifier


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
        m.max_base = 5
        assert m.value == 5

    def test_setting_value_within_bounds(self):
        m = MinMaxValue(value=10, min=0, max=20)
        m.value = 15
        assert m.value == 15

    def test_add_max_modifier(self):
        m = MinMaxValue(value=10, min=0, max=20)
        m.max_modifiers.add(ValueModifier(multiplier=2.0, duration=10.0))
        assert m.max == 40.0

    def test_max_modifier_clamps_value(self):
        m = MinMaxValue(value=10, min=0, max=20)
        m.max_modifiers.add(ValueModifier(multiplier=2.0, duration=10.0))
        m.value = 50
        assert m.value == 40.0

    def test_removed_max_modifier_clamps_value(self):
        m = MinMaxValue(value=10, min=0, max=20)
        mod = ValueModifier(multiplier=2.0, duration=10.0)
        m.max_modifiers.add(mod)
        m.value = 40
        m.max_modifiers.remove(mod)
        assert m.max == 20.0
        assert m.value == 20.0
