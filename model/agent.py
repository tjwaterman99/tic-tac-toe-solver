from .contracts import State, Action
from .qtable import QTable


class Agent:
    def __init__(self, player: int, qtable: QTable):
        assert player in (-1, 1), "Player must be -1 or 1"
        self.qtable = qtable
        self.player = player

    def get_random_action(self, board: list[int]) -> Action:
        state = State.from_list(positions=board, next_player=self.player)
        return self.qtable.get_random_action(state)

    def choose_action(self, board: list[int]) -> Action:
        state = State.from_list(positions=board, next_player=self.player)
        return self.qtable.get_best_action(state)

    def get_scores(self, board: list[int]) -> list[tuple[int]]:
        state = State.from_list(board, next_player=self.player)
        values = self.qtable[state]
        positions = [a.position for a in values.actions]
        return list(zip(positions, values.probabilities))
