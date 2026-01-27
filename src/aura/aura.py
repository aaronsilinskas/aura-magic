from aura.values import MinMaxValue


class Spell:
    def __init__(self) -> None:
        self.name: str = self.__class__.__name__.replace("Spell", "")

    def update(self, aura: "Aura", ellapsed_time: float) -> bool:
        """Update the spell. Return True if the spell should be removed from the aura."""
        raise NotImplementedError()

    def modify_event(self, aura: Aura, event: AuraEvent) -> None:
        """Modify an incoming event if needed."""
        pass


class AuraEvent:

    def __init__(self) -> None:
        self.cancelled: bool = False


class DamageEvent(AuraEvent):
    def __init__(self, amount: float) -> None:
        super().__init__()
        self.amount = amount


class HealEvent(AuraEvent):
    def __init__(self, amount: float) -> None:
        super().__init__()
        self.amount = amount


class Aura:

    def __init__(self, min_magic: float, max_magic: float, cast_delay: float) -> None:
        """Initialize the Aura with magic bounds and cast delay.

        Args:
            min_magic: The minimum value the magic attribute can reach.
            max_magic: The maximum value the magic attribute can reach.
            cast_delay: The base cast delay in seconds.
        """
        self.magic = MinMaxValue(value=max_magic, min=min_magic, max=max_magic)
        self._spells: list[Spell] = []
        self._cast_delay: float = cast_delay

    def add_spell(self, spell: Spell) -> None:
        self._spells.append(spell)

    def handle_event(self, event: AuraEvent) -> None:
        for spell in self._spells:
            spell.modify_event(self, event)
            if event.cancelled:
                return

        self._apply_event(event)

    def _apply_event(self, event: AuraEvent) -> None:
        if isinstance(event, DamageEvent):
            self.magic.value -= event.amount
        elif isinstance(event, HealEvent):
            self.magic.value += event.amount

    def update(self, elapsed_time: float) -> None:
        spells_to_remove = []
        for spell in self._spells:
            should_remove = spell.update(self, elapsed_time)
            if should_remove:
                spells_to_remove.append(spell)
        for spell in spells_to_remove:
            self._spells.remove(spell)

    @property
    def spells(self) -> list[Spell]:
        return self._spells
