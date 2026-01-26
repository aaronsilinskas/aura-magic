import pytest
from aura.aura import Aura, AuraEvent, Spell
from aura.spells import AirSliceSpell
from conftest import AuraFixture


# class EarthShieldModifier(SpellModifier):
#     """Modifier that reduces incoming damage by 75% for a number of hits or duration."""

#     def modify_damage(self, damage: float) -> float:
#         if self.hits_remaining > 0:
#             self.hits_remaining -= 1
#             return damage * 0.25  # Reduce damage by 75%
#         return damage

#     def update(self, ellapsed_time: float) -> bool:
#         self.duration_remaining -= ellapsed_time
#         return self.duration_remaining <= 0 or self.hits_remaining <= 0


class EarthShieldSpell(Spell):
    """Resists incoming damage for a number of hits or duration."""

    def __init__(self, reduction: float) -> None:
        super().__init__()
        self.reduction = reduction

    def update(self, aura: Aura, ellapsed_time: float) -> bool:

        return False

    def modify_event(self, aura: Aura, event: AuraEvent) -> bool:

        return False


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

    assert aura.current_magic == aura.max_magic - (
        shield_fixture.damage_after_shield * 2
    )


# test after hit count
# test after duration
