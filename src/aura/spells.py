from aura.values import ValueModifier
from .aura import DamageEvent, DurationSpell, HealEvent, Spell, Aura, AuraEvent


class AmbientMagicRegenSpell(Spell):
    def __init__(self, amount_per_second: float) -> None:
        super().__init__()
        self.amount_per_second: float = amount_per_second

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        heal_amount = self.amount_per_second * elapsed_time
        aura.handle_event(HealEvent(heal_amount))

        return False  # Don't remove this spell


class IgniteSpell(DurationSpell):
    def __init__(self, damage_per_second: float, duration: float) -> None:
        super().__init__(duration)
        self.damage_per_second = damage_per_second

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        damage = self.damage_per_second * min(
            elapsed_time, self.duration - self.duration_elapsed
        )
        aura.handle_event(DamageEvent(damage))

        return super().update(aura, elapsed_time)


class AirSliceSpell(Spell):
    def __init__(self, damage: float) -> None:
        super().__init__()
        self.damage = damage

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        aura.handle_event(DamageEvent(self.damage))

        return True  # Remove after one application


class EarthShieldSpell(DurationSpell):
    """Resists incoming damage for a number of hits or duration."""

    def __init__(self, reduction: float, max_hits: int, duration: float) -> None:
        super().__init__(duration)

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
        super().__init__(duration)

        self.cast_delay_modifier = cast_delay_modifier
        self._modifier = ValueModifier(self.cast_delay_modifier, duration=self.duration)

    def start(self, aura: Aura) -> None:
        aura.cast_delay_modifiers.add(self._modifier)

    def stop(self, aura: Aura) -> None:
        aura.cast_delay_modifiers.remove(self._modifier)


class IceShieldSpell(DurationSpell):
    """Resists incoming damage for a number of hits or duration. Casts Freeze when max hits exceeded."""

    def __init__(self, reduction: float, max_hits: int, duration: float) -> None:
        super().__init__(duration)

        self.reduction = max(0, min(reduction, 1))
        self.max_hits = max_hits
        self.hits_taken = 0
        self.freeze_cast = False

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
        if self.freeze_cast:
            return  # Already cast
        self.freeze_cast = True

        # TODO Cast the Freeze spell
