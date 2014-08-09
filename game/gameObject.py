from game.constants import GameConstants


class Game(object):
    def __init__(self):
        self.player1_game_field = [None for _ in range(GameConstants.field_size)]
        self.player2_game_field = [None for _ in range(GameConstants.field_size)]

    def clear_all_game_fields(self):
        self.player1_game_field = []
        self.player2_game_field = []

    def remove_dead(self):
        """Удаляет все карты у которых is_alive==False с игрового поля
        """
        #player 1
        for i, el in enumerate(self.player1_game_field):
            #if element exist and is dead
            if el is not None and not el.is_alive:
                self.player1_game_field[i] = None
        #player 2
        for i, el in enumerate(self.player2_game_field):
            if el is not None and not el.is_alive:
                self.player2_game_field[i] = None