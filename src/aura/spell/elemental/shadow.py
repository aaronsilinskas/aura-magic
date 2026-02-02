from aura.aura import Aura, Spell, SpellTags
from aura.spell.elemental.elements import ElementTags
from aura.values import Duration


class ShadowSpell(Spell):
    """A spell that temporarily turns the selected spell visual indicators black until the duration expires."""

    def __init__(self, duration: float) -> None:
        super().__init__([SpellTags.DEBUFF, ElementTags.DARK])
        self._base_duration = duration
        self.duration = Duration(duration)  # in seconds

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        return self.duration.update(elapsed_time)5

    def _update_level(self, level: int) -> None:
        self.duration.length = Spell.LEVEL_SCALER.scale_value(
            self._base_duration, level
        )
