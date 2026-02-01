import pytest
from aura.aura import DamageEvent, HealEvent
from aura.spell.elemental.charge import ChargeSpell
from conftest import AuraFixture


class ChargeFixture(AuraFixture):
    def __init__(self) -> None:
        super().__init__()
        self.aura.magic.value = self.max_magic / 4  # Start at 25% magic
        self.healing_multiplier = 1.5  # 150% healing
        self.duration = 10.0
        self.charge_spell = ChargeSpell(
            healing_multiplier=self.healing_multiplier,
            duration=self.duration,
        )


@pytest.fixture
def fixture() -> ChargeFixture:
    return ChargeFixture()


def test_charge_amplifies_healing(fixture: ChargeFixture) -> None:
    aura = fixture.aura
    initial_magic = aura.magic.value
    original_heal_amount = fixture.max_magic / 4  # heal by 25%
    charged_heal_amount = original_heal_amount * fixture.healing_multiplier

    aura.add_spell(fixture.charge_spell)

    aura.process_event(HealEvent(original_heal_amount))

    assert aura.magic.value == initial_magic + charged_heal_amount


def test_charge_does_not_amplify_damage(fixture: ChargeFixture) -> None:
    aura = fixture.aura
    initial_magic = aura.magic.value
    damage_amount = fixture.max_magic / 10  # damage by 10%

    aura.add_spell(fixture.charge_spell)

    aura.process_event(DamageEvent(damage_amount))

    assert aura.magic.value == initial_magic - damage_amount


def test_charge_expires_after_duration(fixture: ChargeFixture) -> None:
    aura = fixture.aura

    aura.add_spell(fixture.charge_spell)

    # Update the aura past the duration of the charge spell
    aura.update(fixture.duration + 1)

    # The charge spell should be expired and removed
    assert fixture.charge_spell not in aura.spells


def test_charge_scale(fixture: ChargeFixture) -> None:
    scale_factor = 2.0
    original_multiplier = fixture.healing_multiplier

    fixture.charge_spell.scale(scale_factor)

    assert fixture.charge_spell.healing_multiplier == original_multiplier * scale_factor
