import pytest
from aura.spells import EarthShieldSpell, AirSliceSpell
from conftest import AuraFixture


class EarthShieldFixture(AuraFixture):
    def __init__(self) -> None:
        super().__init__()
        self.damage_reduction = 0.75  # 75% damage reduction
        self.shield_spell = EarthShieldSpell(reduction=self.damage_reduction)
        self.damage = self.aura.max_magic / 2  # Damage 1/2 of magic
        self.damage_spell = AirSliceSpell(damage=self.damage)
        self.damage_after_shield = self.damage * (1 - self.damage_reduction)


@pytest.fixture
def shield_fixture() -> EarthShieldFixture:
    return EarthShieldFixture()


def test_earth_shield_resistance(shield_fixture: EarthShieldFixture) -> None:
    aura = shield_fixture.aura

    aura.add_spell(shield_fixture.shield_spell)
    aura.add_spell(shield_fixture.damage_spell)
    aura.add_spell(shield_fixture.damage_spell)
    aura.update(0.1)  # Trigger damage

    assert aura.current_magic == pytest.approx(
        aura.max_magic - (shield_fixture.damage_after_shield * 2)
    )


# test after hit count
# test after duration
