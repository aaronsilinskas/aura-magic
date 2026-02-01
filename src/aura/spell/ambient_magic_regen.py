from aura.aura import Aura, HealEvent, Spell, SpellTags


class AmbientMagicRegenSpell(Spell):
    def __init__(self, amount_per_second: float) -> None:
        super().__init__([SpellTags.BUFF])
        self.amount_per_second: float = amount_per_second

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        heal_amount = self.amount_per_second * elapsed_time
        aura.process_event(HealEvent(heal_amount))

        return False  # Don't remove this spell

    def scale(self, factor: float) -> None:
        self.amount_per_second *= factor
