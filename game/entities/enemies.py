
import random

from . import Entity


class Enemy(Entity):

    TABLE = 'enemies'
    TYPE = 'enemy'

    def roll_evasion(self, attacker, buffs=dict()):
        accuracy_mod = buffs.get('attributes', dict()).get('accuracy', 0)
        evade = (
            (random.randint(1, 6) + self.attributes.deftness) >
            (random.randint(1, 12) + attacker.attributes.accuracy + accuracy_mod)
        )
        return evade