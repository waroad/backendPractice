from datetime import datetime
from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None
list1 = []
app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        print("oops", request.get_json(),datetime.utcnow())
        dict_t = request.get_json()
        list1.append([dict_t['adr'], dict_t['content'], datetime.utcnow()])
        socketio.emit('my_response', {'data': request.get_json()['content'], 'node': request.get_json()['adr'],
                                      'time': str(datetime.utcnow())})
    return render_template('index1.html', async_mode=socketio.async_mode)


# @socketio.event
# def my_event(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']})
#

if __name__ == '__main__':
    socketio.run(app)
