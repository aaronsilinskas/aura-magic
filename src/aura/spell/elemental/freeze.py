from aura.aura import Aura, Spell, SpellTags
from aura.spell.elemental.elements import ElementTags
from aura.values import Duration, ValueModifier


class FreezeSpell(Spell):
    """Increases the delay between spell casts for a duration."""

    def __init__(self, duration: float, cast_delay_modifier: float) -> None:
        super().__init__([SpellTags.DEBUFF, ElementTags.ICE])
        self.duration = Duration(duration)
        self.cast_delay_modifier = cast_delay_modifier
        self._modifier = ValueModifier(
            self.cast_delay_modifier, duration=self.duration.length
        )

    def start(self, aura: Aura) -> None:
        aura.cast_delay.modifiers.add(self._modifier)

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        return self.duration.update(elapsed_time)

    def stop(self, aura: Aura) -> None:
        aura.cast_delay.modifiers.remove(self._modifier)

    def scale(self, factor: float) -> None:
        self.cast_delay_modifier *= factor
        self._modifier.multiplier = self.cast_delay_modifier
