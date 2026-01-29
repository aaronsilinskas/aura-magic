import pytest
from aura.spells import FreezeSpell
from conftest import AuraFixture


class FreezeFixture(AuraFixture):
    def __init__(self) -> None:
        super().__init__()

        self.freeze_duration: float = 5.0  # seconds
        self.cast_delay_modifier: float = 2.0  # double the cast delay
        self.freeze_spell: FreezeSpell = FreezeSpell(
            duration=self.freeze_duration, cast_delay_modifier=self.cast_delay_modifier
        )


@pytest.fixture
def fixture() -> FreezeFixture:
    return FreezeFixture()


def test_freeze_spell_increases_cast_delay(fixture: FreezeFixture) -> None:
    aura = fixture.aura
    original_delay = aura.cast_delay.base

    aura.add_spell(fixture.freeze_spell)
    aura.update(1.0)  # Update to apply spell effects

    assert aura.cast_delay.value == original_delay * fixture.cast_delay_modifier


def test_freeze_spell_expires_and_restores_cast_delay(fixture: FreezeFixture) -> None:
    aura = fixture.aura
    original_delay = aura.cast_delay

    aura.add_spell(fixture.freeze_spell)

    # Simulate time passing until the spell expires
    aura.update(fixture.freeze_duration + 1.0)

    # cast delay should be restored to original
    assert aura.cast_delay == original_delay


def test_freeze_spell_removal_restores_cast_delay(fixture: FreezeFixture) -> None:
    aura = fixture.aura
    original_delay = aura.cast_delay

    aura.add_spell(fixture.freeze_spell)
    aura.update(1.0)  # Update to apply spell effects

    # Remove the spell before it expires
    aura.remove_spell(fixture.freeze_spell)

    # cast delay should be restored to original
    assert aura.cast_delay == original_delay
