import json
import random
from dataclasses import dataclass, asdict, field
from model.contracts import State, Action


@dataclass
class QTableValue:
    state: State
    actions: list[Action]
    probabilities: list[float]

    def get_random_action(self) -> Action:
        return random.choice(self.actions)
    
    def get_best_action(self) -> Action:
        best_action = None
        highest_p = 0
        for k, v in zip(self.actions, self.probabilities):
            if best_action is None:
                best_action = k
                highest_p = v
            else:
                if v > highest_p:
                    best_action = k
                    highest_p = v
        return best_action

    def get_probability(self, action: Action):
        index = self.actions.index(action)
        return self.probabilities[index]

    def set_probability(self, action: Action, value: float):
        assert value > 0, f"Can not set probability lower than 0"
        index = self.actions.index(action)
        self.probabilities[index] = value
        return self.probabilities[index]

    def normalize_probabilities(self):
        total_p = sum(self.probabilities)
        new_p = [round(p / total_p, 3) for p in self.probabilities]
        self.probabilities = new_p

    def reward_action(self, action: Action, adjustment: float):
        assert action in self.actions, f"{action} is not valid for {self.state}"
        current_probability = self.get_probability(action)
        new_probability = max(0, current_probability * adjustment)
        self.set_probability(action, new_probability)
        self.normalize_probabilities()
        return self.probabilities


@dataclass
class QTable:
    states: dict[State, QTableValue] = field(default_factory=dict)

    def __len__(self):
        return len(self.states)

    def __getitem__(self, item: State):
        return self.states[item]
    
    def __contains__(self, item: State):
        assert type(item) == State, f"Can not search QTable for item of type {type(item)}"
        return item in self.states

    def add_state(self, state: State) -> QTableValue:
        if state not in self.states:
            actions = [Action(p, player=state.next_player) for p in state.available_positions()]
            probabilities = [1 / len(actions) for _ in range(len(actions))]
            self.states[state] = QTableValue(state, actions=actions, probabilities=probabilities)
        return self.states[state]

    def get_random_action(self, state: State):
        if state not in self:
            self.add_state(state)
        qtable_value = self[state]
        return qtable_value.get_random_action()
    
    def get_best_action(self, state: State):
        if state not in self:
            return self.get_random_action(state)
        values = self[state]
        return values.get_best_action()

    def to_list(self):
        return [asdict(v) for v in self.states.values()]
    
    def to_json(self):
        return json.dumps(self.to_list())
    
    def save(self, fp: str):
        with open(fp, 'w') as fh:
            json.dump(self.to_list(), fh)

    @classmethod
    def from_json(cls, path: str):
        with open(path, 'r') as fh:
            data = json.load(fh)
        states = dict()
        for row in data:
            raw_state = row['state']
            raw_actions = row['actions']
            probabilities = row['probabilities']
            state = State.from_list(positions=raw_state['positions'], next_player=raw_state['next_player'])
            actions = list()
            for action in raw_actions:
                action = Action(position=action['position'], player=action['player'])
                actions.append(action)
            qtable_value = QTableValue(state=state, actions=actions, probabilities=probabilities)
            states[state] = qtable_value
        return cls(states=states)
