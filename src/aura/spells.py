from aura.values import ValueModifier
from .aura import DamageEvent, HealEvent, Spell, Aura, AuraEvent


class AmbientMagicRegenSpell(Spell):
    def __init__(self, amount_per_second: float) -> None:
        super().__init__()
        self.amount_per_second: float = amount_per_second

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        heal_amount = self.amount_per_second * elapsed_time
        aura.handle_event(HealEvent(heal_amount))

        return False  # Don't remove this spell


class IgniteSpell(Spell):
    def __init__(self, damage_per_second: float, duration: float) -> None:
        super().__init__()
        self.damage_per_second = damage_per_second
        self.duration = duration
        self.elapsed = 0.0

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        if self.elapsed < self.duration:
            damage = self.damage_per_second * min(
                elapsed_time, self.duration - self.elapsed
            )
            aura.handle_event(DamageEvent(damage))
            self.elapsed += elapsed_time

        return self.elapsed >= self.duration


class AirSliceSpell(Spell):
    def __init__(self, damage: float) -> None:
        super().__init__()
        self.damage = damage

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        aura.handle_event(DamageEvent(self.damage))

        return True  # Remove after one application


class EarthShieldSpell(Spell):
    """Resists incoming damage for a number of hits or duration."""

    def __init__(self, reduction: float, max_hits: int, duration: float) -> None:
        super().__init__()
        self.reduction = max(0, min(reduction, 1))
        self.max_hits = max_hits
        self.hits_taken = 0
        self.duration = duration
        self.elapsed = 0.0

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        self.elapsed += elapsed_time
        if self._expired():
            return True  # Remove the spell

        return False

    def modify_event(self, aura: Aura, event: AuraEvent) -> None:
        if isinstance(event, DamageEvent) and not self._expired():
            event.amount *= 1 - self.reduction
            self.hits_taken += 1

    def _expired(self) -> bool:
        return self.hits_taken >= self.max_hits or self.elapsed >= self.duration


class FreezeSpell(Spell):
    """Increases the delay between spell casts for a duration."""

    def __init__(self, duration: float, cast_delay_modifier: float) -> None:
        super().__init__()
        self.duration = duration
        self.cast_delay_modifier = cast_delay_modifier
        self.elapsed = 0.0
        self._modifier = ValueModifier(self.cast_delay_modifier, duration=self.duration)

    def start(self, aura: Aura) -> None:
        aura.cast_delay_modifiers.add(self._modifier)

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        self.elapsed += elapsed_time
        if self.elapsed >= self.duration:
            return True  # Remove the spell

        return False

    def stop(self, aura: Aura) -> None:
        aura.cast_delay_modifiers.remove(self._modifier)


class IceShieldSpell(Spell):
    """Resists incoming damage for a number of hits or duration. Casts Freeze when max hits exceeded."""

    def __init__(self, reduction: float, max_hits: int, duration: float) -> None:
        super().__init__()
        self.reduction = max(0, min(reduction, 1))
        self.max_hits = max_hits
        self.hits_taken = 0
        self.duration = duration
        self.elapsed = 0.0
        self.freeze_cast = False

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        self.elapsed += elapsed_time

        # Cast Freeze spell when max hits exceeded
        if self.hits_taken >= self.max_hits and not self.freeze_cast:

            # TODO cast the freeze spell

            self.freeze_cast = True

        if self._expired():
            return True  # Remove the spell

        return False

    def modify_event(self, aura: Aura, event: AuraEvent) -> None:
        if isinstance(event, DamageEvent) and not self._expired():
            event.amount *= 1 - self.reduction
            self.hits_taken += 1

    def _expired(self) -> bool:
        return self.hits_taken >= self.max_hits or self.elapsed >= self.duration
