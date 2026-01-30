from aura.aura import Aura, Spell, SpellTags
from aura.spell.elemental.elements import ElementTags
from aura.spell.elemental.pause import PauseSpell


class UnpauseSpell(Spell):
    """Removes the Pause effect from the target Auras immediately."""

    def __init__(self) -> None:
        super().__init__([SpellTags.BUFF, ElementTags.TIME])

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        pause_spells = aura.spells.get_by_class(PauseSpell)
        for spell in pause_spells:
            aura.remove_spell(spell)

        return True  # Remove immediately after application
