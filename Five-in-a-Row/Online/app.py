import time
import json
from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, emit


# Define the class of the game to operate on back-end logic
class Game:
    def __init__(self):
        # int number of players (and viewers)
        self.numPlayer = 0
        # int number of lines on the board
        self.numLines = 19
        # int number of offset (not on the board, for simplifying boundary conditions later)
        self.offset = 4
        # bool value, whether a step is valid
        self.isValid = False
        # # bool value, whether black player or white player should play now
        # # (Assume black goes first for every game)
        # self.isBlackTurn = True
        # int value, -1 for white win, 1 for black win and 0 for normal ongoing state
        self.victoryState = 0
        # 2D int array for the logic board, entry -1 for white, 1 for black, 0 for no piece
        # self.map = [[0] * self.numLines] * self.numLines
        self.map = []
        # Attention!
        # This map will be 27 * 27 = (4 + 19 + 4) * (4 + 19 + 4)
        # Hence there will be offset of 4 out lines to be considered in position
        for i in range(self.numLines + self.offset * 2):
            temp = []
            for j in range(self.numLines + self.offset * 2):
                temp.append(0)
            self.map.append(temp)

    # Check whether the input position is legal
    # Fill that position in the map with the correct piece.
    def checkValidAndFill(self, x, y, isBlack):
        # If someone wins the game already
        if self.victoryState != 0:
            return False
        # If the position can not be calculated precisely, please review "index.html"
        if (x == -1) or (y == -1):
            return False
        else:
            # If the position is out the range of the board
            if x < 0 or y < 0 or x >= self.numLines or y >= self.numLines:
                return False
            # If the position is occupied
            elif self.map[x + self.offset][y + self.offset] != 0:
                return False
            # If the position is not occupied yet
            else:
                # If the piece is black or not
                if isBlack == 1:
                    self.map[x + self.offset][y + self.offset] = 1
                else:
                    self.map[x + self.offset][y + self.offset] = -1
                return True

    # Check whether sequences in 8 directions form the goal of "Five-in-a-Row"
    def checkLeftRow(self, x, y):
        if self.map[x][y] == self.map[x - 1][y] == self.map[x - 2][y] == self.map[x - 3][y] == self.map[x - 4][y] == 1:
            self.victoryState = 1
        elif self.map[x][y] == self.map[x - 1][y] == self.map[x - 2][y] == self.map[x - 3][y] == self.map[x - 4][
            y] == -1:
            self.victoryState = -1

    def checkRightRow(self, x, y):
        if self.map[x][y] == self.map[x + 1][y] == self.map[x + 2][y] == self.map[x + 3][y] == self.map[x + 4][y] == 1:
            self.victoryState = 1
        elif self.map[x][y] == self.map[x + 1][y] == self.map[x + 2][y] == self.map[x + 3][y] == self.map[x + 4][
            y] == -1:
            self.victoryState = -1

    def checkUpColumn(self, x, y):
        if self.map[x][y] == self.map[x][y - 1] == self.map[x][y - 2] == self.map[x][y - 3] == self.map[x][y - 4] == 1:
            self.victoryState = 1
        elif self.map[x][y] == self.map[x][y - 1] == self.map[x][y - 2] == self.map[x][y - 3] == self.map[x][
            y - 4] == -1:
            self.victoryState = -1

    def checkDownColumn(self, x, y):
        if self.map[x][y] == self.map[x][y + 1] == self.map[x][y + 2] == self.map[x][y + 3] == self.map[x][y + 4] == 1:
            self.victoryState = 1
        elif self.map[x][y] == self.map[x][y + 1] == self.map[x][y + 2] == self.map[x][y + 3] == self.map[x][
            y + 4] == -1:
            self.victoryState = -1

    def checkLeftUp(self, x, y):
        if self.map[x][y] == self.map[x - 1][y - 1] == self.map[x - 2][y - 2] == self.map[x - 3][y - 3] == \
                self.map[x - 4][y - 4] == 1:
            self.victoryState = 1
        elif self.map[x][y] == self.map[x - 1][y - 1] == self.map[x - 2][y - 2] == self.map[x - 3][y - 3] == \
                self.map[x - 4][y - 4] == -1:
            self.victoryState = -1

    def checkLeftDown(self, x, y):
        if self.map[x][y] == self.map[x - 1][y + 1] == self.map[x - 2][y + 2] == self.map[x - 3][y + 3] == \
                self.map[x - 4][y + 4] == 1:
            self.victoryState = 1
        elif self.map[x][y] == self.map[x - 1][y + 1] == self.map[x - 2][y + 2] == self.map[x - 3][y + 3] == \
                self.map[x - 4][y + 4] == -1:
            self.victoryState = -1

    def checkRightDown(self, x, y):
        if self.map[x][y] == self.map[x + 1][y + 1] == self.map[x + 2][y + 2] == self.map[x + 3][y + 3] == \
                self.map[x + 4][y + 4] == 1:
            self.victoryState = 1
        elif self.map[x][y] == self.map[x + 1][y + 1] == self.map[x + 2][y + 2] == self.map[x + 3][y + 3] == \
                self.map[x + 4][y + 4] == -1:
            self.victoryState = -1

    def checkRightUp(self, x, y):
        if self.map[x][y] == self.map[x + 1][y - 1] == self.map[x + 2][y - 2] == self.map[x + 3][y - 3] == \
                self.map[x + 4][y - 4] == 1:
            self.victoryState = 1
        elif self.map[x][y] == self.map[x + 1][y - 1] == self.map[x + 2][y - 2] == self.map[x + 3][y - 3] == \
                self.map[x + 4][y - 4] == -1:
            self.victoryState = -1

    # Check whether someone is victory
    # and change the game victoryState to finish the game
    def checkVictory(self):
        # Since the map is 19 * 19 and total is 27 * 27
        # We only need to start from Line 4 to Line 22
        for i in range(self.offset, self.numLines + self.offset):
            for j in range(self.offset, self.numLines + self.offset):
                if self.map[i][j] == 0:
                    continue
                self.checkLeftRow(i, j)
                self.checkRightRow(i, j)
                self.checkUpColumn(i, j)
                self.checkDownColumn(i, j)
                self.checkLeftUp(i, j)
                self.checkLeftDown(i, j)
                self.checkRightDown(i, j)
                self.checkRightUp(i, j)
                if self.victoryState == 1 or self.victoryState == -1:
                    break
            if self.victoryState == 1 or self.victoryState == -1:
                break


# Instantiate the game
game = Game()

# Instantiate the Flask object
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO()
socketio.init_app(app)


# Define routes
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/receive_character', methods=['GET'])
def assign_to_client():
    global character_json
    character_json = ''
    if game.numPlayer == 0:
        character_json = {
            'message': '1'
        }
        game.numPlayer += 1
    elif game.numPlayer == 1:
        character_json = {
            'message': '0'
        }
        game.numPlayer += 1
    else:
        character_json = {
            'message': '-1'
        }
        game.numPlayer += 1
    return jsonify(character_json)


@app.route('/send_to_server', methods=['GET'])
def receive_from_client():
    global message_get
    message_get = ''
    message_get = request.args['message']

    # Get the position from the message of clients
    position = message_get.split()
    # print(position)
    # Check the validation of the position and Fill
    game.isValid = game.checkValidAndFill(int(position[0]), int(position[1]), int(position[2]))
    if game.isValid:
        # Check whether someone wins the game
        game.checkVictory()
        # # Black and white will take turn to put on pieces
        # game.isBlackTurn = not game.isBlackTurn

    return "Message received:" + message_get


@app.route('/receive_steps', methods=['GET'])
def send_to_client():
    global message_json
    message_json = {
        'message': ''
    }
    if game.isValid:
        message_json = {
            'message': message_get
        }
    else:
        message_json = {
            'message': "Illegal operation!"
        }
    return jsonify(message_json)


@app.route('/receive_results', methods=['GET'])
def send_results():
    global result_json
    result_json = {
        'message': ''
    }
    if game.victoryState == 1:
        result_json = {
            'message': "Black wins!"
        }
    elif game.victoryState == -1:
        result_json = {
            'message': "White wins!"
        }
    return jsonify(result_json)


@socketio.on('askOtherStep', namespace='/testnamespace')
def give_response(data):
    clientReq = data.get('param')
    # print("Client requested...")
    # Emit the step
    emit('response', {'code': '200', 'msg': message_get})

    # time.sleep(5)



if __name__ == '__main__':
    # app.run(debug=False)
    socketio.run(app, debug=False, host='0.0.0.0', port=5000)
