import random

from aura import Aura


class AuraFixture:
    def __init__(self) -> None:
        self.min_magic: float = -1 * random.uniform(100.0, 200.0)
        self.max_magic: float = random.uniform(100.0, 200.0)
        self.aura: Aura = Aura(min_magic=self.min_magic, max_magic=self.max_magic)

    def set_starting_magic(self, value: float) -> None:
        self.aura.alter_magic(value - self.aura.current_magic)
