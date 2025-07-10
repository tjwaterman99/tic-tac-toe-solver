import pickle
from dataclasses import dataclass
import os
import random


from .contracts import State, Action


@dataclass(frozen=True)
class HistoryItem:
    state: State
    action: Action
    player: int


class Engine:
    def __init__(self):
        self.history: list[HistoryItem] = []
        self.finished = False
        self.winner: int | None = None

    @property
    def latest_state(self) -> State:
        if not self.history:
            raise ValueError("No history available.")
        return self.history[-1].state

    def apply_action(self, state: State, action: Action) -> State:
        if state.positions[action.index] != 0:
            raise ValueError(f"Invalid action: position {action.index} already taken.")
        if self.finished:
            raise ValueError("Game is already finished.")
        current_player = self.get_current_player()
        positions = list(state.positions)
        positions[action.index] = current_player
        new_state = State(positions=tuple(positions))
        self.history.append(HistoryItem(state=state, action=action, player=current_player))
        self.set_finished(new_state)
        # print(f"Action applied: {action.index} by player {current_player}. Game Finished: {self.finished}. New state: {new_state}.")
        return new_state

    def get_current_player(self) -> int:
        return 1 if len(self.history) % 2 == 0 else -1

    def set_winner(self, new_state: State):
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]

        for a, b, c in win_conditions:
            if new_state.positions[a] == new_state.positions[b] == new_state.positions[c] != 0:
                self.winner = new_state.positions[a]
                return True

    def set_finished(self, new_state: State):
        self.set_winner(new_state)
        if self.winner is not None:
            self.finished = True
        if all(pos != 0 for pos in new_state.positions):
            self.finished = True


class Policy:
    def __init__(self, exploration_rate: float = 0.5):
        self.actions: dict[State, dict[Action, float]] = {}
        self.exploration_rate = exploration_rate

    def get_allowed_actions(self, state: State) -> list[Action]:
        return [Action(i) for i in range(9) if state.positions[i] == 0]

    def get_action(self, state: State) -> Action:
        if state not in self.actions:
            self.actions[state] = {action: random.random() * 0.01 for action in self.get_allowed_actions(state)}
        if random.random() < self.exploration_rate:
            return random.choice(list(self.actions[state].keys()))
        return max(self.actions[state], key=self.actions[state].get)

    def update_actions(self, engine: Engine):
        reward = 0.02
        for item in reversed(engine.history):
            if item.player == engine.winner:
                self.actions[item.state][item.action] += reward
                reward *= 0.9  # Decrease reward for earlier states
            else:
                self.actions[item.state][item.action] -= 0.01

    def normalize_actions(self):
        for state, actions in self.actions.items():
            for action, value in actions.items():
                if value < 0 :
                    actions[action] = 0
            total_value = max(sum(actions.values()), 1)
            for action, value in actions.items():
                actions[action] = value / total_value

    def save(self, filename: str):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
    
    @classmethod
    def load(cls, filename: str) -> 'Policy':
        with open(filename, 'rb') as f:
            return pickle.load(f)


class Trainer:
    def __init__(self, policy: Policy):
        self.policy = policy

    def train(self):
        state = State()
        engine = Engine()
        while not engine.finished:
            action = self.policy.get_action(state)
            state = engine.apply_action(state, action)
            if engine.finished:
                self.policy.update_actions(engine)


def train():
    policy = Policy(exploration_rate=0.25)
    trainer = Trainer(policy)
    for n in range(1, 500001):
        if n % 1000 == 0:
            print(f"Iteration {n} of 500000")
        trainer.train()
    # Total states seen seems to be 4520
    policy.normalize_actions()
    policy.save('policy.pkl')
    print("Total states seen:", len(trainer.policy.actions))


def predict(board: tuple[int], policy_filename: str) -> int:
    cwd = os.path.dirname(__file__)
    model_path = os.path.join(cwd, policy_filename)
    print("Loading from", model_path)
    policy = Policy.load(model_path)
    policy.exploration_rate = 0.0  # Disable exploration for prediction
    state = State(positions=board)
    action = policy.get_action(state)
    return action.index


if __name__ == "__main__":
    train()
