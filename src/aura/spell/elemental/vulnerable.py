from aura.aura import Aura, AuraEvent, DamageEvent, Spell, SpellTags
from aura.spell.elemental.elements import ElementTags
from aura.values import Duration


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
