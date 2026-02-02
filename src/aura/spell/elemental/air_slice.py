from aura.aura import Aura, DamageEvent, Spell, SpellTags
from aura.spell.elemental.elements import ElementTags


class AirSliceSpell(Spell):
    def __init__(self, damage: float) -> None:
        super().__init__([SpellTags.DEBUFF, ElementTags.AIR])
        self._base_damage = damage
        self.damage = damage

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        aura.process_event(DamageEvent(self.damage))

        return True  # Remove after one application

    def _update_level(self, level: int) -> None:
        self.damage = Spell.scale_to_level(self._base_damage, level)
