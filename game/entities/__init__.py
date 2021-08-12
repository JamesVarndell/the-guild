
import random

from game._database import DatabaseManager


class Entity(DatabaseManager):

    def roll_initiative(self, buffs=dict()):
        """Generate an initiative rank to determine turn order in battle."""
        speed_mod = buffs.get('attributes', dict()).get('speed', 0)
        roll = random.randint(1, 20)
        if roll > 1:
            roll += self.attributes.speed + speed_mod
        return roll

    def roll_damage(self, buffs=dict()):
        """Generate a damage output value in battle."""
        brawn_mod = buffs.get('attributes', dict()).get('brawn', 0)
        damage = random.randint(1, 6) + self.attributes.brawn + brawn_mod
        return damage

    @property
    def vitality(self):
        """Convenience property for quick access to vitality."""
        return self.vitals.vitality
    
    @vitality.setter
    def vitality(self, value):
        self.vitals['vitality'] = max(0, min(value, self.vitals.max_vitality))

    @property
    def energy(self):
        """Convenience property for quick access to energy."""
        return self.vitals.energy
    
    @energy.setter
    def energy(self, value):
        self.vitals['energy'] = max(0, min(value, self.vitals.max_energy))

    @property
    def willpower(self):
        """Convenience property for quick access to willpower."""
        return self.vitals.willpower
    
    @willpower.setter
    def willpower(self, value):
        self.vitals['willpower'] = max(0, min(value, self.vitals.max_willpower))
