from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Scribble
from . import db
import json

inscriptionviews = Blueprint('inscriptionviews', __name__)


@inscriptionviews.route('/', methods=['GET', 'POST'])
@login_required
def Home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Scribble is too short!', category='error')
        else:
            new_scribble = Scribble(data=note, user_id=current_user.id)
            db.session.add(new_scribble)
            db.session.commit()
            flash('Scribble added successfully!', category='success')

    return render_template("Home.html", user=current_user)


@inscriptionviews.route('/delete-inscription', methods=['POST'])
def delete_inscription():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Scribble.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
