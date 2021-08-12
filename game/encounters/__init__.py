
import json
import random
from collections import namedtuple

from game._database import DatabaseManager
from game.entities import Entity, characters, enemies


class Encounter(DatabaseManager):

    TABLE = 'encounters'

    @property
    def enemy(self):
        enemy_id = self.db.execute(
            f'SELECT id FROM {enemies.Enemy.TABLE} WHERE name = ?', (self.enemy__name,)
        ).fetchone()['id']
        enemy = enemies.Enemy(self.db, enemy_id)
        return enemy


class EncounterEnemy(Entity):

    TABLE = 'encountered_enemy'
    PRIMARY_KEY = 'user__id'

    @property
    def _raw_enemy(self):
        return enemies.Enemy(self.db, self.enemy__id)

    def __getattr__(self, key):
        try:
            value = super().__getattr__(key)
        except AttributeError:
            value = getattr(self._raw_enemy, key)
        return value


class UserEncounter(DatabaseManager):

    TABLE = 'user_encounter'
    PRIMARY_KEY = 'user__id'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.area = 'caves'

        self._enemy = None
        self._character = None

        self.result_text = None

        if self.data is None:
            self.start()

    @property
    def encounter(self):
        return Encounter(self.db, self.encounter__id)

    @property
    def encounter_state(self):
        return namedtuple('State', self.state)(**self.state)

    @property
    def character(self):
        if self._character is None:
            self._character = characters.Character(self.db, self.id)
        return self._character

    @property
    def enemy(self):
        return EncounterEnemy(self.db, self.id)

    def attack(self, attacker, defender, buffs=dict(), additive=False):
        if attacker.TYPE == 'character':
            attacker_buffs, defender_buffs = buffs, dict()
        else:
            attacker_buffs, defender_buffs = dict(), buffs

        damage = None
        evade = defender.roll_evasion(attacker, buffs=defender_buffs)
        if not evade:
            damage = attacker.roll_damage(buffs=attacker_buffs)
            defender.vitality -= damage
        
        state = {
            'type': 'combat',
            'first': attacker.TYPE,
            'second': None,
            'first_damage': damage,
            'second_damage': None,
        }
        if additive:
            state = {**self.state, **state}

        self.update('state', state)
        return state

    def heal(self, additive=False):
        self.character.vitality += 20
        state = {
            'heal': 20,
        }
        if additive:
            state = {**self.state, **state}
        self.update('state', state)
        return state

    def combat(self, stance=None, additive=False):

        buffs = dict()
        n_attacks = 1
        if stance is not None:
            stance_data = self.character.stances[stance]
            buffs = stance_data.get('buffs', dict())
            n_attacks = stance_data.get('n_attacks', 1)

        first, second = self.character, self.enemy
        if self.enemy.roll_initiative() > self.character.roll_initiative(buffs):
            first, second = self.enemy, self.character

        first_damage = self.attack(first, second, buffs=buffs)['first_damage']
        if first.TYPE == 'character' and n_attacks > 1:
            first_damage = [first_damage]
            for _ in range(n_attacks-1):
                first_damage.append(self.attack(first, second, buffs=buffs)['first_damage'])
        if second.vitality > 0:
            second_damage = self.attack(second, first, buffs=buffs)['first_damage']
            if second.TYPE == 'character' and n_attacks > 1:
                second_damage = [second_damage]
                for _ in range(n_attacks-1):
                    second_damage.append(self.attack(second, first, buffs=buffs)['first_damage'])
        else:
            second = None
            second_damage = None

        first = first.TYPE
        if second is not None:
            second = second.TYPE
        
        state = {
            'type': 'combat',
            'first': first,
            'second': second,
            'first_damage': first_damage,
            'second_damage': second_damage,
        }
        if additive:
            state = {**self.state, **state}

        self.update('state', state)
        return state

    def start(self, text=None):
        pool = self.db.execute(
            f'SELECT * FROM {Encounter.TABLE} WHERE area = ?', (self.area,)
        ).fetchall()
        ids, weights = zip(*((item['id'], item['weight']) for item in pool))
        encounter_id = random.choices(ids, weights=weights)[0]
        encounter = Encounter(self.db, encounter_id)

        self.db.execute(
            f'INSERT INTO {UserEncounter.TABLE} '
            f'(user__id, encounter__id, text, image, state, options, turns)'
            f'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (
                self.id,
                encounter_id,
                text or encounter.text,
                encounter.image,
                json.dumps(dict()),
                encounter.options,
                0,
            )
        )
        if encounter.enemy__name is not None:
            max_vitals = {f'max_{k}': v for k, v in encounter.enemy.vitals.items()}
            vitals = {**encounter.enemy.vitals, **max_vitals}
            self.db.execute(
                f'INSERT INTO {EncounterEnemy.TABLE} '
                f'(user__id, enemy__id, vitals, buffs, effects)'
                f'VALUES (?, ?, ?, ?, ?)',
                (
                    self.id,
                    encounter.enemy.id,
                    json.dumps(vitals),
                    encounter.enemy.buffs,
                    encounter.enemy.effects,
                )
            )
        self.db.commit()

    def end(self):
        self.db.execute(f'DELETE FROM {self.TABLE} WHERE {self.PRIMARY_KEY} = ?', (self.id,))
        if self.enemy is not None:
            self.db.execute(
                f'DELETE FROM {EncounterEnemy.TABLE} WHERE {EncounterEnemy.PRIMARY_KEY} = ?',
                (self.id,)
            )
        self.db.commit()
