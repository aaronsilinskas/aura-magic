from aura.aura import Aura, Spell, SpellTags
from aura.spell.elements import ElementTags
from aura.spell.pause import PauseSpell


class UnpauseSpell(Spell):
    """Removes the Pause effect from the target Auras immediately."""

    def __init__(self) -> None:
        super().__init__([SpellTags.BUFF, ElementTags.TIME])

    def start(self, aura: Aura) -> None:
        pause_spells = aura.spells.get_by_class(PauseSpell)
        for spell in pause_spells:
            aura.remove_spell(spell)

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        return True  # Remove immediately after application
