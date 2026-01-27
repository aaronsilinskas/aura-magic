from .aura import DamageEvent, HealEvent, Spell, Aura, AuraEvent


class AmbientMagicRegenSpell(Spell):
    def __init__(self, amount_per_second: float) -> None:
        super().__init__()
        self.amount_per_second: float = amount_per_second

    def update(self, aura: Aura, ellapsed_time: float) -> bool:
        heal_amount = self.amount_per_second * ellapsed_time
        aura.handle_event(HealEvent(heal_amount))

        return False  # Don't remove this spell


class IgniteSpell(Spell):
    def __init__(self, damage_per_second: float, duration: float) -> None:
        super().__init__()
        self.damage_per_second = damage_per_second
        self.duration = duration
        self.elapsed = 0.0

    def update(self, aura: Aura, ellapsed_time: float) -> bool:
        if self.elapsed < self.duration:
            damage = self.damage_per_second * min(
                ellapsed_time, self.duration - self.elapsed
            )
            aura.handle_event(DamageEvent(damage))
            self.elapsed += ellapsed_time

        return self.elapsed >= self.duration


class AirSliceSpell(Spell):
    def __init__(self, damage: float) -> None:
        super().__init__()
        self.damage = damage

    def update(self, aura: Aura, ellapsed_time: float) -> bool:
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

    def update(self, aura: Aura, ellapsed_time: float) -> bool:
        self.elapsed += ellapsed_time
        if self._expired():
            return True  # Remove the spell

        return False

    def modify_event(self, aura: Aura, event: AuraEvent) -> None:
        if isinstance(event, DamageEvent) and not self._expired():
            event.amount *= 1 - self.reduction
            self.hits_taken += 1

    def _expired(self) -> bool:
        return self.hits_taken >= self.max_hits or self.elapsed >= self.duration
