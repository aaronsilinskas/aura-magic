import pytest
from conftest import AuraFixture


@pytest.fixture
def fixture() -> AuraFixture:
    return AuraFixture()


def test_aura_initialization(fixture: AuraFixture) -> None:
    aura = fixture.aura
    assert aura.current_magic == fixture.max_magic
    assert aura.max_magic == fixture.max_magic
    assert len(aura.spells) == 0


def test_min_magic_limit(fixture: AuraFixture) -> None:
    aura = fixture.aura

    # Try to reduce current magic below min_magic
    aura.alter_magic(-(aura.max_magic - aura.min_magic + 50.0))

    # Current magic should not be allowed to go below min_magic
    assert aura.current_magic == aura.min_magic


def test_max_magic_limit(fixture: AuraFixture) -> None:
    aura = fixture.aura

    # Try to exceed max magic limit
    aura.alter_magic(50.0)

    # Current should not exceed max magic
    assert aura.current_magic == aura.max_magic


# | *Cauterize* - stop all DoTs                                     | *Ignite* - damage over time                                         |
# | --------------------------------------------------------------- | ------------------------------------------------------------------- |
# | *Regen* - heal over time                                        | *Soak* - coats target in water                                      |
# | *Earth shield* - adds 75% resistance for a duration for 3 hits. | *Rock* - blunt damage                                               |
# | *Ice shield* - adds 50% resistance, shatters after 3 hits.      | *Freeze* - spell casting slows                                      |
# | *Haste* - increase spell cast speed                             | *Slice* - sharp damage                                              |
# | *Charge* - increase magic regen speed                           | *Shock* - slows magic regen speed                                   |
# | *Heal* - restores magic to an aura                              | *Flash* - temporarily turn all displays white                       |
# | *Shadow* - hides currently selected spell                       | *Vulnerable* - removes resistance or amplifies next hit             |
# | *Continue* - remove Pause                                       | *Pause* - blocks casting of caster and targets for a short duration |
# | *Absorb* - absorbs the next spell                               | *Weight* - any movement causes damage                               |
