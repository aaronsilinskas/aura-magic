from aura.values import MinMaxValue, ValueModifiers, ValueWithModifiers


class Spell:
    """Base class for all spells."""

    def __init__(self, tags: list[str]) -> None:
        self.name: str = self.__class__.__name__.replace("Spell", "")
        self._tags: list[str] = tags

    @property
    def tags(self):
        return iter(self._tags)

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
        """Modify an incoming event if needed, will only be called for active spells."""
        pass


class SpellTags:
    SHIELD = "SHIELD"
    BUFF = "BUFF"
    DEBUFF = "DEBUFF"


class AuraEvent:
    """Base class for events affecting the aura."""

    def __init__(self) -> None:
        self._canceled: bool = False

    @property
    def is_canceled(self) -> bool:
        return self._canceled

    @is_canceled.setter
    def is_canceled(self, value: bool) -> None:
        self._canceled = value


class DamageEvent(AuraEvent):
    """Event representing damage taken."""

    def __init__(self, amount: float) -> None:
        """Initializes a damage event with a specific amount."""
        super().__init__()
        self.amount = max(0, amount)


class HealEvent(AuraEvent):
    """Event representing healing received."""

    def __init__(self, amount: float) -> None:
        """Initializes a heal event with a specific amount."""
        super().__init__()
        self.amount = max(0, amount)


class CastEvent(AuraEvent):
    """Event representing a spell cast attempt."""

    def __init__(self, spell: Spell) -> None:
        """Initializes a cast event."""
        super().__init__()
        self.spell = spell


class Spells:
    """A collection manager for Spell objects."""

    def __init__(self, spells: list[Spell]) -> None:
        self._spells: list[Spell] = spells

    def get_by_name(self, name: str) -> list[Spell]:
        """Finds a spell by its name."""
        return [spell for spell in self._spells if spell.name == name]

    def get_by_tag(self, tag: str) -> list[Spell]:
        """Finds spells by a specific tag."""
        return [spell for spell in self._spells if tag in spell.tags]

    def __len__(self) -> int:
        return len(self._spells)

    def __iter__(self):
        return iter(self._spells)


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
        self._spell_list: list[Spell] = []
        self._spells = Spells(self._spell_list)
        self._cast_delay = ValueWithModifiers(base_value=cast_delay)

    def add_spell(self, spell: Spell) -> None:
        """Adds a spell to the aura and starts it.

        Args:
            spell: The spell to add.
        """
        self._spell_list.append(spell)
        spell.start(self)

    def remove_spell(self, spell: Spell) -> None:
        """Removes a spell from the aura and stops it.

        Args:
            spell: The spell to remove.
        """
        self._spell_list.remove(spell)
        spell.stop(self)

    def handle_event(self, event: AuraEvent) -> None:
        """Processes an incoming event through all active spells.

        If an event is canceled by a spell, it is not applied to the magic value.

        Args:
            event: The incoming event to process.
        """
        for spell in self.spells:
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
        self._cast_delay.update(elapsed_time)

        spells_to_remove = []
        for spell in self.spells:
            should_remove = spell.update(self, elapsed_time)
            if should_remove:
                spells_to_remove.append(spell)
        for spell in spells_to_remove:
            self.remove_spell(spell)

    @property
    def spells(self) -> Spells:
        """Returns the active spells collection."""
        return self._spells

    @property
    def cast_delay(self) -> ValueWithModifiers:
        """Returns the current cast delay including modifiers."""
        return self._cast_delay
