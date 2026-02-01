from aura.aura import Aura, AuraEvent, CastEvent, Spell, SpellTags
from aura.values import Duration


class WeakenSpell(Spell):
    def __init__(self, reduction: float, duration: float) -> None:
        super().__init__(tags=[SpellTags.DEBUFF])
        self.reduction = max(0, min(reduction, 1))
        self.duration = Duration(duration)

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        return self.duration.update(elapsed_time)

    def modify_event(self, aura: Aura, event: AuraEvent) -> None:
        if isinstance(event, CastEvent):
            spell = event.spell
            spell.scale(1 - self.reduction)

    def scale(self, factor: float) -> None:
        self.reduction *= factor
        self.reduction = max(0, min(self.reduction, 1))
