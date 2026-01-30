from aura.aura import Aura, AuraEvent, HealEvent, Spell, SpellTags
from aura.spell.elemental.elements import ElementTags
from aura.values import Duration


class ChargeSpell(Spell):
    def __init__(self, healing_multiplier: float, duration: float) -> None:
        super().__init__([SpellTags.BUFF, ElementTags.LIGHTNING])
        self.duration = Duration(duration)
        self.healing_multiplier = healing_multiplier

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        return self.duration.update(elapsed_time)

    def modify_event(self, aura: Aura, event: AuraEvent) -> None:
        if isinstance(event, HealEvent):
            event.amount *= self.healing_multiplier
