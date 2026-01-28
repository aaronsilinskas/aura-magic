import random

import pytest
from aura.aura import DamageEvent, HealEvent, SpellTags
from aura.spells import DurationSpell, VulnerableSpell
from conftest import AuraFixture


class VulnerableFixture(AuraFixture):
    def __init__(self) -> None:
        super().__init__()
        self.damage_multiplier = 2.0  # 200% damage taken
        self.duration = round(random.uniform(5.0, 10.0))
        self.vulnerable_spell = VulnerableSpell(
            damage_multiplier=self.damage_multiplier, duration=self.duration
        )
        self.damage_amount = self.max_magic / 4  # damage by 25%


@pytest.fixture
def fixture() -> VulnerableFixture:
    return VulnerableFixture()


def test_vulnerable_removes_shield_spells(fixture: VulnerableFixture) -> None:
    aura = fixture.aura

    # Add non-shield and shield spells
    non_shield_spell = DurationSpell(tags=[SpellTags.BUFF], duration=10.0)
    shield_spell = DurationSpell(tags=[SpellTags.SHIELD], duration=10.0)
    shield_spell_2 = DurationSpell(tags=[SpellTags.SHIELD], duration=10.0)
    aura.add_spell(non_shield_spell)
    aura.add_spell(shield_spell)
    aura.add_spell(shield_spell_2)

    assert aura.spells.get_by_tag(SpellTags.SHIELD) == [shield_spell, shield_spell_2]

    # Add the vulnerable spell
    aura.add_spell(fixture.vulnerable_spell)

    # Shield spell should be removed
    assert aura.spells.get_by_tag(SpellTags.SHIELD) == []
    assert list(aura.spells) == [non_shield_spell, fixture.vulnerable_spell]


def test_vulnerable_amplifies_damage_when_no_shields_removed(
    fixture: VulnerableFixture,
) -> None:
    aura = fixture.aura
    initial_magic = aura.magic.value

    vulnerable_damage_amount = fixture.damage_amount * fixture.damage_multiplier

    # No shield spells active
    aura.add_spell(fixture.vulnerable_spell)

    aura.handle_event(DamageEvent(fixture.damage_amount))

    assert aura.magic.value == initial_magic - vulnerable_damage_amount


def test_vulnerable_does_not_amplify_damage_when_shields_removed(
    fixture: VulnerableFixture,
) -> None:
    aura = fixture.aura
    initial_magic = aura.magic.value

    # Shield spell active to be removed
    shield_spell = DurationSpell(tags=[SpellTags.SHIELD], duration=10.0)
    aura.add_spell(shield_spell)

    aura.add_spell(fixture.vulnerable_spell)

    aura.handle_event(DamageEvent(fixture.damage_amount))

    assert aura.magic.value == initial_magic - fixture.damage_amount


def test_vulnerable_not_applied_to_healing(fixture: VulnerableFixture) -> None:
    aura = fixture.aura
    heal_amount = aura.magic.max / 4  # heal by 25%
    fixture.set_starting_magic(fixture.max_magic - heal_amount * 2)
    initial_magic = aura.magic.value

    # No shield spells active
    aura.add_spell(fixture.vulnerable_spell)

    aura.handle_event(HealEvent(heal_amount))  # Healing event

    assert aura.magic.value == initial_magic + heal_amount


def test_vulnerable_removed_after_expiry(fixture: VulnerableFixture) -> None:
    aura = fixture.aura

    aura.add_spell(fixture.vulnerable_spell)
    aura.update(fixture.duration + 1)

    assert fixture.vulnerable_spell not in aura.spells
