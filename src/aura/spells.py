from .aura import Spell, Aura


class AmbientMagicRegenSpell(Spell):
    def __init__(self, amount_per_second: float) -> None:
        super().__init__()
        self.amount_per_second: float = amount_per_second

    def update(self, aura: Aura, ellapsed_time: float) -> bool:
        aura.alter_magic(self.amount_per_second * ellapsed_time)
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
            aura.alter_magic(-damage)
            self.elapsed += ellapsed_time

        return self.elapsed >= self.duration


class AirSliceSpell(Spell):
    def __init__(self, damage: float) -> None:
        super().__init__()
        self.damage = damage

    def update(self, aura: Aura, ellapsed_time: float) -> bool:
        aura.alter_magic(-self.damage)
        return True  # Remove after one application
