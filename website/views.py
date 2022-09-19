from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from pynput.keyboard import Key, Listener
import logging
import threading
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session

views = Blueprint('views', __name__)


#Redirect the default link to "index.html", but need to be logged in first.
@views.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("index.html", user=current_user)

#Chat room function
@views.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if(request.method=='POST'):
        username = request.form['username']
        room = request.form['room']
        #Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session = session)
    else:
        if(session.get('username') is not None):
            return render_template('chat.html', session = session)
        else:
            return redirect(url_for('views.index'))


