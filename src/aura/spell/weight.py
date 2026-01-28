import math
from aura.aura import Aura, AuraEvent, DamageEvent, SpellTags
from aura.spells import DurationSpell


GRAVITY: float = 9.81  # m/s²


class AccelerationEvent(AuraEvent):
    """Event representing acceleration."""

    def __init__(
        self,
        x_accel: float,
        y_accel: float,
        z_accel: float,
        remove_gravity: bool = True,
    ) -> None:
        super().__init__()
        self.x_accel = x_accel
        self.y_accel = y_accel
        self.z_accel = z_accel

        self._accel_magnitude = math.sqrt(x_accel**2 + y_accel**2 + z_accel**2)
        if remove_gravity:
            # Subtract gravity
            self._accel_magnitude = max(0.0, self._accel_magnitude - GRAVITY)

    @property
    def accel_magnitude(self) -> float:
        return self._accel_magnitude


class WeightSpell(DurationSpell):
    def __init__(
        self, acceleration_threshold: float, damage_per_second: float, duration: float
    ) -> None:
        super().__init__([SpellTags.DEBUFF], duration)
        self.acceleration_threshold = acceleration_threshold
        self.damage_per_second = damage_per_second
        self.movement_detected = False

    def update(self, aura: Aura, elapsed_time: float) -> bool:
        if super().update(aura, elapsed_time):
            return True

        # if movement was detected above threshold, apply damage
        if self.movement_detected:
            damage = self.damage_per_second * min(
                elapsed_time, self.duration - self.duration_elapsed
            )
            aura.handle_event(DamageEvent(damage))

        return False

    def modify_event(self, aura: "Aura", event: AuraEvent) -> None:
        if isinstance(event, AccelerationEvent):
            self.movement_detected = event.accel_magnitude > self.acceleration_threshold
