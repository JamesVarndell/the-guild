
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

from game import entities, encounters

bp = Blueprint('encounter', __name__)


@bp.route('/encounter', methods=['GET', 'POST'])
def user_encounter():
    
    db = get_db()

    encounter = encounters.UserEncounter(db, g.user['id'])

    if request.method == 'POST':
        if request.form.get('refresh'):
            encounter.end()
            encounter.start()

    if request.method == 'POST':
        attack = request.form.get('attack')
        heal = request.form.get('heal')
        if heal:
            encounter.heal()
            encounter.attack(encounter.enemy, encounter.character, additive=True)
        elif attack:
            encounter.combat()
        print(encounter.state)
        return redirect(url_for('encounter.user_encounter'))

    template = 'encounters/combat.html'

    if encounter.character.vitality <= 0:
        encounter.result_text = 'You lose!'
        template = 'encounters/end.html'
    elif encounter.enemy.vitality <= 0:
        encounter.result_text = 'You win!'
        template = 'encounters/end.html'

    return render_template(template, encounter=encounter)


@bp.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r
