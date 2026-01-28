import random

from aura import Aura
from aura.aura import DamageEvent, Spell
from aura.caster import Caster


class AuraFixture:
    def __init__(self) -> None:
        self.min_magic: float = -1 * round(random.uniform(100.0, 200.0))
        self.max_magic: float = round(random.uniform(100.0, 200.0))
        self.cast_delay: float = round(random.uniform(3.0, 5.0))
        self.aura: Aura = Aura(
            min_magic=self.min_magic,
            max_magic=self.max_magic,
            cast_delay=self.cast_delay,
        )

    def set_starting_magic(self, value: float) -> None:
        self.aura.handle_event(DamageEvent(self.aura.magic.value - value))


class SpellTrackingCaster(Caster):
    def __init__(self) -> None:
        self.cast_spells = []

    def cast_spell(self, spell: Spell) -> None:
        self.cast_spells.append(spell)
