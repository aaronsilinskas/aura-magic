from .aura import Spell, Aura, AuraEvent
from .spells import AmbientMagicRegenSpell, IgniteSpell

__all__ = ["Spell", "Aura", "AmbientMagicRegenSpell", "IgniteSpell"]

def main() -> None:
    print("Hello from aura!")
