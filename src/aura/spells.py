from aura.caster import CastType, Caster
from aura.spell.elements import ElementTags
from aura.values import ValueModifier
from .aura import DamageEvent, HealEvent, Spell, Aura, AuraEvent, SpellTags


class DurationSpell(Spell):
    """A spell with a specific duration."""

    def __init__(self, tags: list[str], duration: float) -> None:
        super().__init__(tags)
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


class AmbientMagicRegenSpell(Spell):
    def __init__(self, amount_per_second: float) -> None:
        super().__init__([SpellTags.BUFF])
        self.amount_per_second: float = amount_per_second

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        heal_amount = self.amount_per_second * elapsed_time
        aura.handle_event(HealEvent(heal_amount))

        return False  # Don't remove this spell


class IgniteSpell(DurationSpell):
    def __init__(self, damage_per_second: float, duration: float) -> None:
        super().__init__([SpellTags.DEBUFF, ElementTags.FIRE], duration)
        self.damage_per_second = damage_per_second

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        damage = self.damage_per_second * min(
            elapsed_time, self.duration - self.duration_elapsed
        )
        aura.handle_event(DamageEvent(damage))

        return super().update(aura, elapsed_time)


class AirSliceSpell(Spell):
    def __init__(self, damage: float) -> None:
        super().__init__([SpellTags.DEBUFF, ElementTags.AIR])
        self.damage = damage

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        aura.handle_event(DamageEvent(self.damage))

        return True  # Remove after one application


class EarthShieldSpell(DurationSpell):
    """Resists incoming damage for a number of hits or duration."""

    def __init__(self, reduction: float, max_hits: int, duration: float) -> None:
        super().__init__(
            [SpellTags.BUFF, SpellTags.SHIELD, ElementTags.EARTH], duration
        )

        self.reduction = max(0, min(reduction, 1))
        self.max_hits = max_hits
        self.hits_taken = 0

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        if super().update(aura, elapsed_time):
            return True

        return self.hits_taken >= self.max_hits

    def modify_event(self, aura: Aura, event: AuraEvent) -> None:
        if self.is_expired or self.hits_taken >= self.max_hits:
            return

        if isinstance(event, DamageEvent):
            event.amount *= 1 - self.reduction
            self.hits_taken += 1


class FreezeSpell(DurationSpell):
    """Increases the delay between spell casts for a duration."""

    def __init__(self, duration: float, cast_delay_modifier: float) -> None:
        super().__init__([SpellTags.DEBUFF, ElementTags.ICE], duration)

        self.cast_delay_modifier = cast_delay_modifier
        self._modifier = ValueModifier(self.cast_delay_modifier, duration=self.duration)

    def start(self, aura: Aura) -> None:
        aura.cast_delay_modifiers.add(self._modifier)

    def stop(self, aura: Aura) -> None:
        aura.cast_delay_modifiers.remove(self._modifier)


class IceShieldSpell(DurationSpell):
    """Resists incoming damage for a number of hits or duration. Casts Freeze when max hits exceeded."""

    def __init__(
        self,
        reduction: float,
        max_hits: int,
        duration: float,
        freeze_spell: FreezeSpell,
        caster: Caster,
    ) -> None:
        super().__init__([SpellTags.BUFF, SpellTags.SHIELD, ElementTags.ICE], duration)

        self.reduction = max(0, min(reduction, 1))
        self.max_hits = max_hits
        self._freeze_spell = freeze_spell
        self._caster = caster

        self.hits_taken = 0
        self._freeze_cast = False

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        if super().update(aura, elapsed_time):
            return True

        # Cast Freeze spell when max hits exceeded
        if self.hits_taken >= self.max_hits:
            self._cast_freeze(aura)
            return True

        return False

    def modify_event(self, aura: Aura, event: AuraEvent) -> None:
        if self.is_expired or self.hits_taken >= self.max_hits:
            return

        if isinstance(event, DamageEvent):
            event.amount *= 1 - self.reduction
            self.hits_taken += 1

    def _cast_freeze(self, aura: Aura) -> None:
        if self._freeze_cast:
            return  # Already cast
        self._freeze_cast = True

        self._caster.cast_spell(
            self._freeze_spell, cast_type=CastType.AREA_OF_EFFECT
        )  # Cast type can be arbitrary here


class VulnerableSpell(DurationSpell):
    """Removes shields or if no shields were active, increases damage taken for a duration."""

    def __init__(self, damage_multiplier: float, duration: float) -> None:
        super().__init__([SpellTags.DEBUFF, ElementTags.DARK], duration)
        self.damage_multiplier: float = max(1.0, damage_multiplier)
        self.shield_spells_removed: bool = False

    def start(self, aura: Aura) -> None:
        shield_spells = aura.spells.get_by_tag(SpellTags.SHIELD)
        for spell in shield_spells:
            aura.remove_spell(spell)

        self.shield_spells_removed = len(shield_spells) > 0

    def modify_event(self, aura: Aura, event: AuraEvent) -> None:
        if not self.shield_spells_removed and isinstance(event, DamageEvent):
            event.amount *= self.damage_multiplier


class ChargeSpell(DurationSpell):
    def __init__(self, healing_multiplier: float, duration: float) -> None:
        super().__init__([SpellTags.BUFF, ElementTags.LIGHTNING], duration)
        self.healing_multiplier = healing_multiplier

    def modify_event(self, aura: Aura, event: AuraEvent) -> None:
        if isinstance(event, HealEvent):
            event.amount *= self.healing_multiplier
