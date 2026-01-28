from aura.aura import Spell


class Caster:

    def cast_spell(self, spell: Spell) -> None:
        """Casts a spell."""
        raise NotImplementedError("cast_spell must be implemented by subclasses.")
