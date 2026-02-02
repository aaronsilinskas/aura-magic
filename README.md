# Aura

A magical aura manipulation library for managing spells, buffs, debuffs, and magic resources in Python.

## Overview

Aura is a flexible spell system designed for games or applications that need to manage dynamic magical effects. It provides a robust framework for handling spell interactions, event-driven modifications, and resource management.

## Core Features

### Aura System

- **Magic Resource Management**: Track and manage a magic pool with configurable min/max bounds
- **Spell Collection**: Active spell management with querying by name, tag, or type
- **Event Processing**: Handle damage, healing, spell casting, and spell modification events
- **Cast Delay System**: Configurable casting delays with modifier support
- **Event Listeners**: Subscribe to aura events for external integrations

### Spell System

#### Spell Lifecycle

- **Start/Stop Hooks**: Initialize and cleanup spell effects
- **Update Loop**: Time-based spell updates with automatic removal
- **Level Scaling**: Configurable spell potency based on level (1+)
- **Event Modification**: Spells can intercept and modify aura events

#### Spell Tags

- **BUFF**: Beneficial effects
- **DEBUFF**: Harmful effects
- **SHIELD**: Damage reduction effects

#### Level Scaling

- **Value Scaling**: Linear scaling for damage, healing, and rates (default: +25% per level)
- **Percentage Scaling**: Incremental scaling for percentages (default: +5% per level)
- Customizable via `SpellLevelScaler` coefficients

### Elemental Spells

#### Damage Spells

- **Slice** (Air): Instant damage
- **Rock** (Earth): Instant damage
- **Ignite** (Fire): Damage over time
- **Weight** (Gravity): Damage over time triggered by movement

#### Healing Spells

- **Heal** (Light): Instant healing
- **Regen** (Water): Healing over time
- **Charge** (Lightning): Amplifies healing effectiveness

#### Shield Spells

- **EarthShield** (Earth): Damage reduction for a number of hits or duration
- **IceShield** (Ice): Damage reduction that casts Freeze in AOE when broken

#### Control & Debuff Spells

- **Freeze** (Ice): Increases cast delay
- **Pause** (Time): Prevents spell casting and multiplies cast delay
- **Shock** (Lightning): Reduces healing by percentage
- **Weaken** (Water): Reduces level of cast spells
- **Vulnerable** (Dark): Removes shields or amplifies damage

#### Buff Spells

- **Haste** (Air): Reduces cast delay by percentage
- **Absorb** (Gravity): Absorbs debuff spells

#### Utility Spells

- **Unpause** (Time): Removes pause effects
- **Warmth** (Fire): Removes water/ice debuffs
- **Flash** (Light): Visual indicator effect (white)
- **Shadow** (Dark): Visual indicator effect (black)

### Spell Combinations

Dynamic spell combining system that detects and transforms spell combinations:

- **Combust**: Combines multiple Ignite spells into a more powerful Ignite
- **Invigorate**: Three or more Regen spells temporarily increase max magic

### Value System

Flexible value management with modifier support:

- **MinMaxValue**: Bounded values with min/max constraints
- **ValueWithModifiers**: Base values with multiplicative modifiers
- **ValueModifier**: Time-limited or permanent value multipliers
- **Duration**: Time tracking with expiration
- **Counter**: Bounded counter with max value tracking

### Element Types

Ten distinct magical elements:

- Fire (Red), Water (Blue), Earth (Yellow)
- Air (Purple), Ice (Green), Lightning (Orange)
- Light (White), Dark (Black)
- Time (Black/White Dots), Gravity (Gray Shades)

### Event System

Comprehensive event types for spell interactions:

- **DamageEvent**: Damage application with modification support
- **HealEvent**: Healing application with modification support
- **CastEvent**: Spell casting attempts (can be canceled)
- **AddSpellEvent**: Spell addition (can be canceled)
- **RemoveSpellEvent**: Spell removal tracking
- **AccelerationEvent**: Movement-based triggers (for Weight spell)

Additional custom events such as **AccelerationEvent** can be created for additional input to the Aura.

### Caster System

Abstract spell casting framework:

- **Cast Types**: LINE, CONE, AREA_OF_EFFECT
- Extensible for different casting implementations such as infrared LEDs or wireless transmission.

## Installation

```bash
# Using uv (recommended)
uv pip install -e .

# Development installation
uv pip install -e ".[dev]"
```

## Testing

Comprehensive test suite covering all spell types and interactions:

```bash
uv run pytest
```

With coverage:

```bash
uv run pytest --cov=aura
```

## Requirements

- Python >= 3.14

## Example Usage

```python
from aura.aura import Aura, SpellTags
from aura.spell.elemental.ignite import IgniteSpell
from aura.spell.elemental.heal import HealSpell
from aura.spell.elemental.elements import ElementTags

# Create an aura with 100 max magic and 1 second cast delay
aura = Aura(min_magic=0, max_magic=100, cast_delay=1.0)

# Add a damage over time spell
ignite = IgniteSpell(damage_per_second=5.0, duration=10.0)
aura.add_spell(ignite)

# Increase spell level for more damage
ignite.level = 3  # 75% more damage

# Update the aura (typically called each frame)
aura.update(elapsed_time=0.1)

# Add instant healing
heal = HealSpell(healing=25.0)
aura.add_spell(heal)
aura.update(elapsed_time=0.1)

# Query active spells
fire_spells = aura.spells.get_by_tag(ElementTags.FIRE)
buffs = aura.spells.get_by_tag(SpellTags.BUFF)
```

## Architecture

The library is organized into several key modules:

- `aura.py`: Core Aura and Spell system
- `values.py`: Value and modifier system
- `caster.py`: Spell casting abstraction
- `spell/elemental/`: Elemental spell implementations
- `spell/combo/`: Spell combination system

## License

See project metadata for licensing information.

## Author

Aaron Silinskas (aaron@mindwidgets.com)
