from aura.caster import CastType, Caster
from aura.spell.elements import ElementTags
from aura.values import Counter, Duration, ValueModifier
from .aura import DamageEvent, HealEvent, Spell, Aura, AuraEvent, SpellTags


class AmbientMagicRegenSpell(Spell):
    def __init__(self, amount_per_second: float) -> None:
        super().__init__([SpellTags.BUFF])
        self.amount_per_second: float = amount_per_second

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        heal_amount = self.amount_per_second * elapsed_time
        aura.handle_event(HealEvent(heal_amount))

        return False  # Don't remove this spell


class IgniteSpell(Spell):
    def __init__(self, damage_per_second: float, duration: float) -> None:
        super().__init__([SpellTags.DEBUFF, ElementTags.FIRE])
        self.duration = Duration(duration)
        self.damage_per_second = damage_per_second

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        damage = self.damage_per_second * min(elapsed_time, self.duration.remaining)
        aura.handle_event(DamageEvent(damage))

        return self.duration.update(elapsed_time)


class AirSliceSpell(Spell):
    def __init__(self, damage: float) -> None:
        super().__init__([SpellTags.DEBUFF, ElementTags.AIR])
        self.damage = damage

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        aura.handle_event(DamageEvent(self.damage))

        return True  # Remove after one application


class EarthShieldSpell(Spell):
    """Resists incoming damage for a number of hits or duration."""

    def __init__(self, reduction: float, max_hits: int, duration: float) -> None:
        super().__init__([SpellTags.BUFF, SpellTags.SHIELD, ElementTags.EARTH])
        self.duration = Duration(duration)
        self.reduction = max(0, min(reduction, 1))
        self.hits = Counter(max=max_hits)

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        if self.duration.update(elapsed_time):
            return True

        return self.hits.is_max

    def modify_event(self, aura: Aura, event: AuraEvent) -> None:
        if self.duration.is_expired or self.hits.is_max:
            return

        if isinstance(event, DamageEvent):
            event.amount *= 1 - self.reduction
            self.hits.increment()


class FreezeSpell(Spell):
    """Increases the delay between spell casts for a duration."""

    def __init__(self, duration: float, cast_delay_modifier: float) -> None:
        super().__init__([SpellTags.DEBUFF, ElementTags.ICE])
        self.duration = Duration(duration)
        self.cast_delay_modifier = cast_delay_modifier
        self._modifier = ValueModifier(
            self.cast_delay_modifier, duration=self.duration.length
        )

    def start(self, aura: Aura) -> None:
        aura.cast_delay.modifiers.add(self._modifier)

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        return self.duration.update(elapsed_time)

    def stop(self, aura: Aura) -> None:
        aura.cast_delay.modifiers.remove(self._modifier)


class IceShieldSpell(Spell):
    """Resists incoming damage for a number of hits or duration. Casts Freeze when max hits exceeded."""

    def __init__(
        self,
        reduction: float,
        max_hits: int,
        duration: float,
        freeze_spell: FreezeSpell,
        caster: Caster,
    ) -> None:
        super().__init__([SpellTags.BUFF, SpellTags.SHIELD, ElementTags.ICE])

        self.duration = Duration(duration)
        self.reduction = max(0, min(reduction, 1))
        self.hits = Counter(max=max_hits)
        self._freeze_spell = freeze_spell
        self._caster = caster

        self._freeze_cast = False

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        if self.duration.update(elapsed_time):
            return True

        # Cast Freeze spell when max hits exceeded
        if self.hits.is_max:
            self._cast_freeze()
            return True

        return False

    def modify_event(self, aura: Aura, event: AuraEvent) -> None:
        if self.duration.is_expired or self.hits.is_max:
            return

        if isinstance(event, DamageEvent):
            event.amount *= 1 - self.reduction
            self.hits.increment()

    def _cast_freeze(self) -> None:
        if self._freeze_cast:
            return  # Already cast
        self._freeze_cast = True

        self._caster.cast_spell(
            self._freeze_spell, cast_type=CastType.AREA_OF_EFFECT
        )  # Cast type can be arbitrary here


class VulnerableSpell(Spell):
    """Removes shields or if no shields were active, increases damage taken for a duration."""

    def __init__(self, damage_multiplier: float, duration: float) -> None:
        super().__init__([SpellTags.DEBUFF, ElementTags.DARK])
        self.duration = Duration(duration)
        self.damage_multiplier: float = max(1.0, damage_multiplier)
        self.shield_spells_removed: bool = False

    def start(self, aura: Aura) -> None:
        shield_spells = aura.spells.get_by_tag(SpellTags.SHIELD)
        for spell in shield_spells:
            aura.remove_spell(spell)

        self.shield_spells_removed = len(shield_spells) > 0

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        return self.duration.update(elapsed_time)

    def modify_event(self, aura: Aura, event: AuraEvent) -> None:
        if not self.shield_spells_removed and isinstance(event, DamageEvent):
            event.amount *= self.damage_multiplier


class ChargeSpell(Spell):
    def __init__(self, healing_multiplier: float, duration: float) -> None:
        super().__init__([SpellTags.BUFF, ElementTags.LIGHTNING])
        self.duration = Duration(duration)
        self.healing_multiplier = healing_multiplier

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        return self.duration.update(elapsed_time)

    def modify_event(self, aura: Aura, event: AuraEvent) -> None:
        if isinstance(event, HealEvent):
            event.amount *= self.healing_multiplier
