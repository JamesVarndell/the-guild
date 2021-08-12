
import numpy as np
from collections import namedtuple

from . import Entity, skills


class Character(Entity):

    TABLE = 'characters'
    PRIMARY_KEY = 'user__id'
    TYPE = 'character'

    def gain_xp(self, skill, xp):
        self.skills[skill] += xp

    @property
    def skill_levels(self):
        """Translate skill experience to levels."""
        levels = {
            k: np.digitize([v], skills.XP_BINS).item()
            for k, v in self.skills.items()
        }
        return namedtuple('Levels', levels)(**levels)