import pytest
from aura.aura import DamageEvent, HealEvent
from conftest import AuraFixture


@pytest.fixture
def fixture() -> AuraFixture:
    return AuraFixture()


def test_aura_initialization(fixture: AuraFixture) -> None:
    aura = fixture.aura
    assert aura.magic.value == fixture.max_magic
    assert aura.magic.max == fixture.max_magic
    assert len(aura.spells) == 0


def test_magic_min_limit(fixture: AuraFixture) -> None:
    aura = fixture.aura

    # Try to reduce current magic below magic.min
    damage_past_min = aura.magic.value - aura.magic.min + 50.0
    aura.handle_event(DamageEvent(damage_past_min))

    # Current magic should not be allowed to go below magic.min
    assert aura.magic.value == aura.magic.min


def test_magic_max_limit(fixture: AuraFixture) -> None:
    aura = fixture.aura

    # Try to exceed max magic limit
    heal_past_max = aura.magic.max * 10
    aura.handle_event(HealEvent(heal_past_max))

    # Current should not exceed max magic
    assert aura.magic.value == aura.magic.max


# Spell casting a debuff spell - *Ice shield* - adds 50% resistance, shatters after 3 hits
# Cast delay adjustment -  *Freeze* - increase delay between spellcasts
# Increases HealEvent -  *Charge* - increase magic regen speed
# | *Shock* - slows magic regen speed
# | *Flash* - temporarily turn all displays white
# | *Shadow* - hides currently selected spell
# Need spell tags to support filtering - *Vulnerable* - removes shields or amplifies next hit
# | *Continue* - remove Pause
# Greatly increase cast delay | *Pause* - blocks casting of caster and targets for a short duration |
# How to intercept an entire spell before combo etc? | *Absorb* - absorbs the next debuff spell
# Add custom event (movement) | *Weight* - any movement causes damage                               |
