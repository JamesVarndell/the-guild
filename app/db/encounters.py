
import yaml
import json


ROWS = [
    'name',
    'image',
    'text',
    'area',
    'weight',
    'options',
    'enemy__name',
]

def init(db):
    with open('data/rooms/caves/encounters/rat.yml', 'r') as f:
        enemy_data = yaml.safe_load(f)
        values = []
        for row in ROWS:
            value = enemy_data.get(row)
            if isinstance(value, (list, dict)):
                value = json.dumps(value)
            values.append(value)
        db.execute(
            f"INSERT INTO encounters ({', '.join(ROWS)}) "
            f"VALUES ({', '.join(['?']*len(ROWS))})",
            values,
        )
    db.commit()