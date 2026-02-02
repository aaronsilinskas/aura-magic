from aura.aura import Aura, AuraEvent, DamageEvent, Spell, SpellTags
from aura.caster import CastType, Caster
from aura.spell.elemental.elements import ElementTags
from aura.spell.elemental.freeze import FreezeSpell
from aura.values import Counter, Duration


class IceShieldSpell(Spell):
    """Resists incoming damage for a number of hits or duration. Casts Freeze in an AOE
    when max hits is exceeded."""

    def __init__(
        self,
        reduction: float,
        max_hits: int,
        duration: float,
        freeze_spell: FreezeSpell,
        caster: Caster,
    ) -> None:
        super().__init__([SpellTags.BUFF, SpellTags.SHIELD, ElementTags.ICE])

        self.duration = Duration(duration)
        self._base_reduction = max(0, min(reduction, 1))
        self.reduction = max(0, min(reduction, 1))
        self.hits = Counter(max=max_hits)
        self._freeze_spell = freeze_spell
        self._caster = caster

        self._freeze_cast = False

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        if self.duration.update(elapsed_time):
            return True

        # Cast Freeze spell when max hits exceeded
        if self.hits.is_max:
            self._cast_freeze()
            return True

        return False

    def modify_event(self, aura: Aura, event: AuraEvent) -> None:
        if self.duration.is_expired or self.hits.is_max:
            return

        if isinstance(event, DamageEvent):
            event.amount *= 1 - self.reduction
            self.hits.increment()

    def _cast_freeze(self) -> None:
        if self._freeze_cast:
            return  # Already cast
        self._freeze_cast = True

        self._caster.cast_spell(
            self._freeze_spell, cast_type=CastType.AREA_OF_EFFECT
        )  # Cast type can be arbitrary here

    def _update_level(self, level: int) -> None:
        self.reduction = Spell.LEVEL_SCALER.scale_percentage(
            self._base_reduction, level
        )
