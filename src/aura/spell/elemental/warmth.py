from aura.aura import Aura, Spell, SpellTags
from aura.spell.elemental.elements import ElementTags


class WarmthSpell(Spell):
    """Remove debuffs from the water and ice elements.
    
    Level scaling: No scaling (instant removal effect).
    """

    def __init__(self) -> None:
        super().__init__([SpellTags.BUFF])

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        water_debuffs = aura.spells.get_by_tag(ElementTags.WATER, SpellTags.DEBUFF)
        ice_debuffs = aura.spells.get_by_tag(ElementTags.ICE, SpellTags.DEBUFF)

        for spell in water_debuffs + ice_debuffs:
            aura.remove_spell(spell)

        return True  # Remove immediately after application

    def _update_level(self, level: int) -> None:
        pass  # No scaling for instant removal spell
