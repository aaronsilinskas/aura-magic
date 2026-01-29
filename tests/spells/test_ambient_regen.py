import pytest
import random
from aura.spells import AmbientMagicRegenSpell
from conftest import AuraFixture


class RegenFixture(AuraFixture):
    def __init__(self) -> None:
        super().__init__()
        self.starting_magic = self.aura.magic.max.value / 2
        self.set_starting_magic(self.starting_magic)
        self.regen_per_second: float = round(random.uniform(1.0, 5.0))
        self.regen_spell: AmbientMagicRegenSpell = AmbientMagicRegenSpell(
            amount_per_second=self.regen_per_second
        )


@pytest.fixture
def regen_fixture() -> RegenFixture:
    return RegenFixture()


def test_magic_regen_over_time_max(regen_fixture: RegenFixture) -> None:
    aura = regen_fixture.aura

    # Duration to regen a quarter of max magic
    duration = aura.magic.max.value / 4 / regen_fixture.regen_per_second

    aura.add_spell(regen_fixture.regen_spell)
    aura.update(duration)  # Simulate time passing

    assert aura.magic.value == regen_fixture.starting_magic + (
        regen_fixture.regen_per_second * duration
    )
