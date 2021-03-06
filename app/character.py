
import json


DEFAULT_CHARACTER = lambda user_id: {
    'user__id': user_id,
    'vitals': json.dumps({
        'vitality': 40,
        'max_vitality': 40,
        'energy': 40,
        'max_energy': 40,
        'willpower': 40,
        'max_willpower': 40,
    }),
    'attributes': json.dumps({
        'speed': 3,
        'brawn': 3,
        'deftness': 3,
        'endurance': 3,
        'accuracy': 3,
    }),
    'skills': json.dumps({
        'botany': 0,
        'fishing': 0,
    }),
    'buffs': json.dumps({
        'vitals': {
            'vitality': 0,
            'energy': 0,
            'willpower': 0,
        },
        'attributes': {
            'speed': 0,
            'brawn': 0,
            'deftness': 0,
            'endurance': 0,
            'accuracy': 0,
        },
        'skills': {
            'botany': 0,
            'fishing': 0,
        },
    }),
    'abilities': json.dumps([]),
    'stances': json.dumps({
        'water': {
            'buffs': {
                'attributes': {
                    'speed': 1,
                    'deftness': 1,
                    'brawn': -1,
                },
            },
            'n_attacks': 2,
        },
        'stone': {
            'buffs': {
                'attributes': {
                    'speed': -2,
                    'brawn': 2,
                    'accuracy': 2,
                },
            },
        },
    }),
    'effects': json.dumps([]),
    'inventory': json.dumps([]),
    'body': json.dumps({}),
}


def create(user_id, db):
    character = DEFAULT_CHARACTER(user_id)
    db.execute(
        f"INSERT INTO characters ({', '.join(character)}) "
        f"VALUES ({', '.join(['?']*len(character))})",
        list(character.values()),
    )
    db.commit()