from typing import Callable


class ValueModifier:
    """Applies a temporary multiplier to a value."""

    def __init__(self, multiplier: float, duration: float) -> None:
        """Initializes the modifier with a multiplier and duration.

        Args:
            multiplier: The factor by which the value is multiplied.
            duration: The time in seconds the modifier lasts.
        """
        self._multiplier = multiplier
        self._duration = duration
        self._duration_elapsed = 0.0

    def update(self, elapsed_time: float) -> bool:
        """Updates the elapsed time.

        Args:
            elapsed_time: The time passed since the last update.

        Returns:
            True if the modifier has expired, False otherwise.
        """
        self._duration_elapsed += elapsed_time
        return self._duration_elapsed >= self._duration

    @property
    def multiplier(self) -> float:
        """Returns the multiplier."""
        return self._multiplier

    @property
    def duration(self) -> float:
        """Returns the total duration."""
        return self._duration

    @property
    def duration_elapsed(self) -> float:
        """Returns the time elapsed since the modifier started."""
        return self._duration_elapsed


class ValueModifiers:
    """Manages a collection of ValueModifiers and notifies a callback when the list changes."""

    def __init__(self, modifiers_changed: Callable) -> None:
        """Initializes the manager with a callback for list changes.

        Args:
            modifiers_changed: A callable to invoke when modifiers are added or removed.
        """
        self._modifiers: list[ValueModifier] = []
        self._modifiers_changed = modifiers_changed

    def add(self, modifier: ValueModifier) -> None:
        """Adds a modifier to the list and triggers the callback.

        Args:
            modifier: The modifier to add.
        """
        self._modifiers.append(modifier)
        self._modifiers_changed()

    def remove(self, modifier: ValueModifier) -> None:
        """Removes a modifier from the list and triggers the callback.

        Args:
            modifier: The modifier to remove.
        """
        self._modifiers.remove(modifier)
        self._modifiers_changed()

    def update(self, elapsed_time: float) -> None:
        """Updates all modifiers, removing expired ones and triggering the callback if changes occurred.

        Args:
            elapsed_time: The time passed since the last update.
        """
        modifiers_to_remove = []
        for modifier in self._modifiers:
            # If update returns True, the modifier has expired
            if modifier.update(elapsed_time):
                modifiers_to_remove.append(modifier)

        for modifier in modifiers_to_remove:
            self._modifiers.remove(modifier)

        if len(modifiers_to_remove) > 0:
            self._modifiers_changed()

    def modify(self, base_value: float) -> float:
        """Applies all active modifiers to a base value.

        Args:
            base_value: The value to modify.

        Returns:
            The modified value.
        """
        modified_value = base_value
        for modifier in self._modifiers:
            modified_value *= modifier.multiplier

        return modified_value

    @property
    def modifiers(self) -> list[ValueModifier]:
        """Returns the list of current modifiers."""
        return self._modifiers


class MinMaxValue:
    """A value clamped between a minimum and a dynamic maximum."""

    def __init__(self, value: float, min: float, max: float) -> None:
        """Initializes the value with a clamped starting value.

        Args:
            value: The starting value.
            min: The minimum allowed value.
            max: The base maximum allowed value.
        """
        self._value = value
        self._min = min
        self._max_base = max
        self._max_modifier = ValueModifiers(self._clamp_value)

    def _clamp_value(self) -> None:
        """Clamps the current value between min and max."""
        self._value = max(self.min, min(self._value, self.max))

    @property
    def value(self) -> float:
        """Returns the current clamped value."""
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        """Sets the value, clamping it between min and max.

        Args:
            value: The value to set.
        """
        self._value = value
        self._clamp_value()

    @property
    def min(self) -> float:
        """Returns the minimum allowed value."""
        return self._min

    @min.setter
    def min(self, value: float) -> None:
        """Updates the minimum allowed value and clamps the current value if necessary.

        Args:
            value: The new minimum value.
        """
        self._min = value
        self._clamp_value()

    @property
    def max_base(self) -> float:
        """Returns the base maximum value."""
        return self._max_base

    @max_base.setter
    def max_base(self, value: float) -> None:
        """Updates the base maximum value and clamps the current value to the modified max.

        Args:
            value: The new base maximum value.
        """
        self._max_base = value
        self._clamp_value()

    @property
    def max(self) -> float:
        """Returns the current maximum, considering active modifiers."""
        return self._max_modifier.modify(self._max_base)

    @property
    def max_modifiers(self) -> ValueModifiers:
        """Returns the manager for maximum modifiers."""
        return self._max_modifier
