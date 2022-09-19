from website import create_app
from pynput.keyboard import Key, Listener
import logging
from flask import Blueprint, Flask, render_template, request, flash, jsonify, session
from flask_login import login_required, current_user
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session


#creates app
app = create_app()

socketio = SocketIO(app, manage_session=False)

@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)

#runs app
if __name__ == '__main__':
    socketio.run(app, debug = True)





