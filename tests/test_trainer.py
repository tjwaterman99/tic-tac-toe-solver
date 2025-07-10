from pytest import fixture
from model.trainer import Trainer
from model.agent import Agent
from model.qtable import QTable


@fixture
def trainer():
    qtable = QTable()
    agent1 = Agent(qtable=qtable, player=1)
    agent2 = Agent(qtable=qtable, player=-1)
    trainer = Trainer(agent1=agent1, agent2=agent2)
    return trainer


def test_trainer_play_game(trainer: Trainer):
    for n in range(100):
        game = trainer.play_game()
        assert game.finished


def test_trainer_train(trainer: Trainer):
    trainer.train(num_games=5)
    print(trainer.agent1.qtable.states)
