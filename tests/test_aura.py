import random
import pytest
from aura.aura import Aura, DamageEvent, HealEvent, Spell
from aura.values import ValueModifier
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


def test_update_triggers_magic_value_update(fixture: AuraFixture) -> None:
    aura = fixture.aura
    modifier = ValueModifier(1.0, duration=0.1)
    aura.magic.max_modifiers.add(modifier)

    # Update the aura to trigger modifier expiry
    aura.update(1.0)

    assert len(aura.magic.max_modifiers) == 0


def test_update_triggers_cast_delay_update(fixture: AuraFixture) -> None:
    aura = fixture.aura
    modifier = ValueModifier(0.5, duration=0.1)
    aura.cast_delay_modifiers.add(modifier)

    # Update the aura to trigger modifier expiry
    aura.update(1.0)

    assert len(aura.cast_delay_modifiers) == 0


class LifecycleTrackingSpell(Spell):
    """Tracks spell updates for testing purposes."""

    def __init__(self) -> None:
        super().__init__()
        self.started = False
        self.update_elapsed_time = None
        self.stopped = False

    def start(self, aura: Aura) -> None:
        super().start(aura)
        self.started = True

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        self.update_elapsed_time = elapsed_time
        return False

    def stop(self, aura: Aura) -> None:
        super().stop(aura)
        self.stopped = True


def test_add_spell_calls_start(fixture: AuraFixture) -> None:
    aura = fixture.aura
    test_spell = LifecycleTrackingSpell()

    assert test_spell.started is False

    aura.add_spell(test_spell)

    assert test_spell.started is True


def test_update_calls_spell_update(fixture: AuraFixture) -> None:
    aura = fixture.aura
    test_spell = LifecycleTrackingSpell()
    elapsed_time = random.uniform(0.5, 2.0)

    aura.add_spell(test_spell)

    assert test_spell.update_elapsed_time is None

    aura.update(elapsed_time)

    assert test_spell.update_elapsed_time == elapsed_time


def test_remove_spell_calls_stop(fixture: AuraFixture) -> None:
    aura = fixture.aura
    test_spell = LifecycleTrackingSpell()

    aura.add_spell(test_spell)

    assert test_spell.stopped is False

    aura.remove_spell(test_spell)

    assert test_spell.stopped is True
