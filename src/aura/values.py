class MinMaxValue:
    def __init__(self, value: float, min: float, max: float) -> None:
        self._value = value
        self._min = min
        self._max = max

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        self._value = max(self._min, min(value, self._max))

    @property
    def min(self) -> float:
        return self._min

    @min.setter
    def min(self, value: float) -> None:
        self._min = value
        self._value = max(self._min, self._value)

    @property
    def max(self) -> float:
        return self._max

    @max.setter
    def max(self, value: float) -> None:
        self._max = value
        self._value = min(self._max, self._value)
