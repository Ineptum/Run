import flask
from flask_socketio import SocketIO, emit, send, join_room, leave_room
import socket
from threading import Thread

app = flask.Flask(__name__)
socketio = SocketIO(app)
# create an INET, STREAMing socket
sock = socket.socket()
# bind the socket to a public host, and a well-known port

sock.bind(('', 8000))
# become a server socket
sock.listen(1)


conn, addr = sock.accept()

event_number = 0

print('СConnected')


# file = open('log.txt', 'w')
# file.close()
handle_log = []
event_number = 0
last_check = 0


@socketio.on('message')
def handleMessage(msg):
    global event_number
    global handle_log
    event_number += 1
    print('Message: ' + msg)
    conn.send(msg.encode())
    print('sent')


@app.route('/socket')
def socket():
    return socket.gethostname()


@app.route('/files')
def files():
    with open('log.txt', 'r') as file:
        return file.read()


@app.route('/changes')
def changes():
    global event_number
    global last_check
    global handle_log
    if event_number == last_check:
        return ""

    else:
        last_check = event_number
        handle_log = handle_log[last_check - event_number:]
        return ''.join(handle_log)


@app.route('/user1', methods=['POST', 'GET'])
def user1():
    print('ЕБАНГУТЬСЯ')
    try:
        if flask.request.method == 'GET':
            return flask.render_template('user11.html')
        elif flask.request.method == 'POST':
            # log_file.write('22\n')
            return 'ну ладно'
    except Exception as e:
        return str(e)


@app.route('/user2', methods=['POST', 'GET'])
def user2():
    print('И ВТОРОЙ ТОЖЕ')
    try:
        if flask.request.method == 'GET':
            return flask.render_template('user2.html')
        elif flask.request.method == 'POST':
            # log_file.write('22\n')
            return 'ну ладно'
    except Exception as e:
        return str(e)


@app.route('/restart')
def restart():
    event_number = 0
    handle_log = []
    return "ok"


@app.route('/connect')
def connect():
    return flask.render_template('user11.html')


def fun1(h, p):
    socketio.run(app, host=h, port=p)


var1 = Thread(target=fun1, args=('0.0.0.0', 5000))
var2 = Thread(target=fun1, args=('0.0.0.0', 5001))


if __name__ == '__main__':
    var1.start()
    var2.start()
