from aura.values import MinMaxValue, ValueModifiers


class Spell:
    def __init__(self) -> None:
        """Initializes the Spell. Sets the name based on the class name."""
        self.name: str = self.__class__.__name__.replace("Spell", "")

    def start(self, aura: "Aura") -> None:
        """Called when the spell is added to the aura. Can be used to set up initial state."""
        pass

    def update(self, aura: "Aura", elapsed_time: float) -> bool:
        """Update the spell. Return True if the spell should be removed from the aura."""
        raise NotImplementedError()

    def stop(self, aura: "Aura") -> None:
        """Called when the spell is removed from the aura. Can be used to clean up state."""
        pass

    def modify_event(self, aura: Aura, event: AuraEvent) -> None:
        """Modify an incoming event if needed."""
        pass


class DurationSpell(Spell):
    def __init__(self, duration: float) -> None:
        """Initializes a spell with a specific duration."""
        super().__init__()
        self._duration = duration
        self._elapsed = 0.0

    def update(self, aura: "Aura", elapsed_time: float) -> bool:
        self._elapsed += elapsed_time
        return self.is_expired

    @property
    def duration(self) -> float:
        """The total duration of the spell."""
        return self._duration

    @property
    def duration_elapsed(self) -> float:
        """The time elapsed since the spell started."""
        return self._elapsed

    @property
    def duration_remaining(self) -> float:
        """The time remaining until the spell expires."""
        return max(0.0, self._duration - self._elapsed)

    @property
    def is_expired(self) -> bool:
        """Whether the spell has expired."""
        return self._elapsed >= self._duration


class AuraEvent:

    def __init__(self) -> None:
        """Initializes the AuraEvent."""
        self._canceled: bool = False

    @property
    def is_canceled(self) -> bool:
        return self._canceled

    @is_canceled.setter
    def is_canceled(self, value: bool) -> None:
        self._canceled = value


class DamageEvent(AuraEvent):
    def __init__(self, amount: float) -> None:
        """Initializes a damage event with a specific amount."""
        super().__init__()
        self.amount = max(0, amount)


class HealEvent(AuraEvent):
    def __init__(self, amount: float) -> None:
        """Initializes a heal event with a specific amount."""
        super().__init__()
        self.amount = max(0, amount)


class Aura:
    """Manages the active spells and magic level of an entity.

    Handles incoming events (damage/healing) and updates spells over time.
    """

    def __init__(self, min_magic: float, max_magic: float, cast_delay: float) -> None:
        """Initialize the Aura with magic bounds and cast delay.

        Args:
            min_magic: The minimum value the magic attribute can reach.
            max_magic: The maximum value the magic attribute can reach.
            cast_delay: The base cast delay in seconds.
        """
        self.magic = MinMaxValue(value=max_magic, min=min_magic, max=max_magic)
        self._spells: list[Spell] = []
        self._cast_delay_base: float = cast_delay
        self._cast_delay_modifiers: ValueModifiers = ValueModifiers()

    def add_spell(self, spell: Spell) -> None:
        """Adds a spell to the aura and starts it.

        Args:
            spell: The spell to add.
        """
        self._spells.append(spell)
        spell.start(self)

    def remove_spell(self, spell: Spell) -> None:
        """Removes a spell from the aura and stops it.

        Args:
            spell: The spell to remove.
        """
        self._spells.remove(spell)
        spell.stop(self)

    def handle_event(self, event: AuraEvent) -> None:
        """Processes an incoming event through all active spells.

        If an event is canceled by a spell, it is not applied to the magic value.

        Args:
            event: The incoming event to process.
        """
        for spell in self._spells:
            spell.modify_event(self, event)
            if event.is_canceled:
                return

        self._apply_event(event)

    def _apply_event(self, event: AuraEvent) -> None:
        """Applies the event to the magic value.

        Args:
            event: The event to apply.
        """
        if isinstance(event, DamageEvent):
            self.magic.value -= event.amount
        elif isinstance(event, HealEvent):
            self.magic.value += event.amount

    def update(self, elapsed_time: float) -> None:
        """Updates the aura state, magic, and spells.

        Args:
            elapsed_time: The time passed since the last update.
        """
        self.magic.update(elapsed_time)
        self._cast_delay_modifiers.update(elapsed_time)

        spells_to_remove = []
        for spell in self._spells:
            should_remove = spell.update(self, elapsed_time)
            if should_remove:
                spells_to_remove.append(spell)
        for spell in spells_to_remove:
            self._spells.remove(spell)

    @property
    def spells(self) -> list[Spell]:
        """Returns the list of active spells."""
        return self._spells

    @property
    def cast_delay_base(self) -> float:
        """Returns the base cast delay."""
        return self._cast_delay_base

    @cast_delay_base.setter
    def cast_delay_base(self, value: float) -> None:
        """Sets the base cast delay."""
        self._cast_delay_base = value

    @property
    def cast_delay(self) -> float:
        """Returns the current cast delay including modifiers."""
        return self._cast_delay_modifiers.modify(self._cast_delay_base)

    @property
    def cast_delay_modifiers(self) -> ValueModifiers:
        """Returns the cast delay modifiers."""
        return self._cast_delay_modifiers
