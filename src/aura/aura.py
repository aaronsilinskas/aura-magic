class Spell:
    def __init__(self) -> None:
        self.name: str = self.__class__.__name__.replace("Spell", "")

    def update(self, aura: "Aura", ellapsed_time: float) -> bool:
        """Update the spell. Return True if the spell should be removed from the aura."""
        raise NotImplementedError()

    def modify_event(self, aura: Aura, event: AuraEvent) -> bool:
        """Modify an incoming event. Return True if the spell should be removed from the aura."""
        return False


class AuraEvent:
    
    pass


class Aura:

    def __init__(self, min_magic: float, max_magic: float) -> None:
        self._current_magic: float = max_magic
        self._max_magic: float = max_magic
        self._min_magic: float = min_magic
        self._spells: list[Spell] = []

    def add_spell(self, spell: Spell) -> None:
        self._spells.append(spell)

    def alter_magic(self, delta: float) -> None:
        """Update current magic by delta amount (positive to increase, negative to decrease), clamped to min/max."""
        self._current_magic = max(self._min_magic, min(self._current_magic + delta, self._max_magic))

    def update(self, elapsed_time: float) -> None:
        spells_to_keep = []
        for spell in self._spells:
            should_remove = spell.update(self, elapsed_time)
            if not should_remove:
                spells_to_keep.append(spell)
        self._spells = spells_to_keep

    @property
    def current_magic(self) -> float:
        return self._current_magic

    @property
    def min_magic(self) -> float:
        return self._min_magic

    @min_magic.setter
    def min_magic(self, value: float) -> None:
        self._min_magic = value

    @property
    def max_magic(self) -> float:
        return self._max_magic

    @max_magic.setter
    def max_magic(self, value: float) -> None:
        self._max_magic = value

    @property
    def spells(self) -> list[Spell]:
        return self._spells
