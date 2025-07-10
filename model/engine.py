from .contracts import State, Action


WINNING_POSITIONS = [
    # Rows
    (0, 1, 2),  # Top row
    (3, 4, 5),  # Middle row
    (6, 7, 8),  # Bottom row
    
    # Columns
    (0, 3, 6),  # Left column
    (1, 4, 7),  # Middle column
    (2, 5, 8),  # Right column
    
    # Diagonals
    (0, 4, 8),  # Top-left to bottom-right
    (2, 4, 6),  # Top-right to bottom-left
]


class Engine:

    def __init__(self, starting_player: int):
        self.history: list[State] = [State.from_list([0,0,0,0,0,0,0,0,0], next_player=starting_player)]
        self.actions: list[Action] = list()
        self.finished = False
        self.winner = None

    @property
    def loser(self):
        if self.winner:
            return self.winner * -1

    @property
    def current_state(self):
        return self.history[-1]
    
    @property
    def draw(self) -> bool:
        return self.finished and not self.winner

    def play(self, position: int, player: int):
        assert not self.finished, "Can not play after a game is finished"
        assert player in (-1, 1), f"Player must be -1 or 1, got {player}"
        assert player == self.current_state.next_player, f"It is the turn of {self.current_state.next_player}, not {player}"
        assert position in range(9), f"Position must be a value between 0 and 8, got {position}"
        assert position in self.current_state.available_positions(), f"Can not play position {position}, available positions: {self.current_state.available_positions()}"
        positions = list(self.current_state.positions)
        positions[position] = player
        state = State.from_list(positions=positions, next_player=player * -1)
        self.history.append(state)
        self.actions.append(Action(position=position, player=player))
        self.set_finished()
        return state

    def set_finished(self):
        if not any(p==0 for p in self.current_state.positions):
            self.finished = True
            return
        for pos in WINNING_POSITIONS:
            p0, p1, p2 = self.current_state.positions[pos[0]], self.current_state.positions[pos[1]], self.current_state.positions[pos[2]]
            if p0 == p1 == p2 and p1 != 0:
                self.winner = p0
                self.finished = True
                break
