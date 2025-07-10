import os
from typing import Optional
from dataclasses import asdict
from model.trainer import Trainer
from model.agent import Agent
from model.qtable import QTable


DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qtable.json')


def train(num_games = int(500e3), output=DEFAULT_MODEL_PATH):
    qtable = QTable()
    agent1 = Agent(qtable=qtable, player=1)
    agent2 = Agent(qtable=qtable, player=-1)
    trainer = Trainer(agent1=agent1, agent2=agent2)
    trainer.train(num_games=num_games)

    print("Number of Games", num_games)
    print("States visited", len(qtable))
    qtable.save(output)
    return qtable


def predict(board: list[int], player: int, params=DEFAULT_MODEL_PATH, qtable: Optional[QTable]=None) -> dict:
    qtable = qtable or QTable.from_json(params)
    agent = Agent(player=player, qtable=qtable)
    action = agent.choose_action(board)
    scores = agent.get_scores(board)
    res = asdict(action)
    res['scores'] = scores
    res['board'] = board
    res['player'] = player
    return res
