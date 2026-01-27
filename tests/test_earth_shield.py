import random
import pytest
from aura.spells import EarthShieldSpell, AirSliceSpell
from conftest import AuraFixture


class EarthShieldFixture(AuraFixture):
    def __init__(self) -> None:
        super().__init__()
        self.damage_reduction = 0.75  # 75% damage reduction
        self.max_hits = random.randint(3, 5)
        self.duration = random.uniform(5.0, 10.0)
        self.shield_spell = EarthShieldSpell(
            reduction=self.damage_reduction,
            max_hits=self.max_hits,
            duration=self.duration,
        )
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


def test_earth_shield_expiry_by_hits(shield_fixture: EarthShieldFixture) -> None:
    aura = shield_fixture.aura

    aura.add_spell(shield_fixture.shield_spell)

    # Apply damage equal to shield hits
    for _ in range(shield_fixture.max_hits):
        aura.add_spell(shield_fixture.damage_spell)
        aura.update(0.1)  # Trigger damage

    # Final update to process removals because earth spell is processed before damage spell
    aura.update(0.1)

    assert (
        shield_fixture.shield_spell not in aura.spells
    ), "Earth Shield should expire after max_hits"


def test_earth_shield_no_resistance_after_expiry(
    shield_fixture: EarthShieldFixture,
) -> None:
    aura = shield_fixture.aura

    aura.add_spell(shield_fixture.shield_spell)

    # Ellapse time past duration to expire shield
    aura.update(shield_fixture.duration + 1)

    assert (
        shield_fixture.shield_spell not in aura.spells
    ), "Earth Shield should expire after duration"
