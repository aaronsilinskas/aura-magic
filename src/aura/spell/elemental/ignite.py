from aura.aura import Aura, DamageEvent, Spell, SpellTags
from aura.spell.elemental.elements import ElementTags
from aura.values import Duration


class IgniteSpell(Spell):
    def __init__(self, damage_per_second: float, duration: float) -> None:
        super().__init__([SpellTags.DEBUFF, ElementTags.FIRE])
        self.duration = Duration(duration)
        self.damage_per_second = damage_per_second

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        damage = self.damage_per_second * min(elapsed_time, self.duration.remaining)
        aura.process_event(DamageEvent(damage))

        return self.duration.update(elapsed_time)
