
import random

from game._database import DatabaseManager


class Entity(DatabaseManager):

    def roll_initiative(self):
        """Generate an initiative rank to determine turn order in battle."""
        roll = random.randint(1, 20)
        if roll > 1:
            roll += self.attributes.speed
        return roll

    def roll_damage(self):
        """Generate a damage output value in battle."""
        damage = random.randint(1, 6)
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
