import pytest
from aura.spells import AirSliceSpell
from conftest import AuraFixture


class SliceFixture(AuraFixture):
    def __init__(self) -> None:
        super().__init__()
        # Deal one-third of max magic as damage
        self.slice_damage: float = self.aura.max_magic // 3
        self.slice_spell: AirSliceSpell = AirSliceSpell(damage=self.slice_damage)


@pytest.fixture
def slice_fixture() -> SliceFixture:
    return SliceFixture()


def test_air_slice_instant_damage(slice_fixture: SliceFixture) -> None:
    aura = slice_fixture.aura

    aura.add_spell(slice_fixture.slice_spell)
    aura.update(0.1)  # Any time passing should trigger the instant damage

    assert aura.current_magic == aura.max_magic - slice_fixture.slice_damage
    # Spell should be removed after dealing damage
    assert slice_fixture.slice_spell not in aura.spells


def test_air_slice_multiple_hits(slice_fixture: SliceFixture) -> None:
    aura = slice_fixture.aura

    # Add two slice spells
    slice_spell_1 = AirSliceSpell(damage=slice_fixture.slice_damage)
    slice_spell_2 = AirSliceSpell(damage=slice_fixture.slice_damage)

    aura.add_spell(slice_spell_1)
    aura.add_spell(slice_spell_2)
    aura.update(0.1)

    # Both spells should deal damage
    assert aura.current_magic == aura.max_magic - (slice_fixture.slice_damage * 2)
    assert len(aura.spells) == 0  # Both spells should be removed
