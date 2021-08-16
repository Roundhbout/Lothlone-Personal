import sys

from ..Common.user import User


class LocalUser(User):
    def __init__(self, username, input_stream=sys.stdin, output_stream=sys.stdout):
        super().__init__(username)
        self.input_stream = input_stream
        self.output_stream = output_stream

    def get_id(self):
        return self.id
    
    def get_username(self):
        return self.username

    def set_id(self, id):
        self.id = id

    def player_update(self, update):
        self.update = update
        self.output_stream.write(str(self.update) + '\n\n')

    def get_move(self):
        while True:
            try:
                self.output_stream.write(self.username + "'s turn!\n")
                self.output_stream.write('Current Position: ' + str(self.update.position) + '\n')
                self.output_stream.write('Enter Move: \n')
                move_input = self.input_stream.readline()
                if move_input == '\n':
                    return None
                move_input = move_input.split(',')
                row = int(move_input[0].strip())
                col = int(move_input[1].strip())
                return row, col
            except ValueError:
                self.output_stream.write('Please enter move in "row, col" where row and col are integers\n')
            except IndexError:
                self.output_stream.write('Two coordinates required in "row, col" format\n')

    def set_response(self, move, result):
        self.last_move = move
        self.result = result
        if result == 'OK':
            return
        elif result == 'Key':
            event = 'found the key'
        elif result == 'Eject':
            event = 'was expelled'
        elif result == 'Exit':
            event = 'exited'
        self.output_stream.write('Player ' + self.username + " " + str(self.result) + "\n")
    
    def start_level(self, level_num, player_list):
        message = "Starting level {} with players: {}\n".format(level_num + 1, ", ".join(player_list))
        self.output_stream.write(message)

    def end_level(self, key, exits, ejects):
        message = "Level over!\n{} found the key!\nThe following players exited: {}\nThe following players were ejected: {}\n".format(key, ", ".join(exits), ", ".join(ejects))
        self.output_stream.write(message)
        
    def end_game(self, score_list):
        message_list = ["Game Over!", "Leaderboard:"]
        for p in score_list:
            playerscore = "{} : Exits: {}, Ejects: {}, Keys: {}".format(p["name"], p["exits"], p["ejects"], p["keys"])
            message_list.append(playerscore)
        self.output_stream.write("\n".join(message_list))

    def set_end_result(self, message):
        self.output_stream.write(message)
