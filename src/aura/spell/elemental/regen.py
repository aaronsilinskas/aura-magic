from aura.aura import Aura, Spell, SpellTags
from aura.spell.elemental.elements import ElementTags
from aura.values import Duration


class RegenSpell(Spell):
    """A spell that provides magic regeneration over time."""

    def __init__(self, regen_rate: float, duration: float):
        """Initialize a RegenSpell.

        Args:
            regen_rate: The rate of magic regeneration per second.
            duration: The duration of the spell in seconds.
        """
        super().__init__(tags=[SpellTags.BUFF, ElementTags.WATER])
        self._base_regen_rate = regen_rate
        self.regen_rate = regen_rate
        self.duration = Duration(duration)

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        regen_amount = self.regen_rate * min(elapsed_time, self.duration.remaining)
        aura.magic.value += regen_amount

        return self.duration.update(elapsed_time)

    def _update_level(self, level: int) -> None:
        self.regen_rate = Spell.scale_to_level(self._base_regen_rate, level)
