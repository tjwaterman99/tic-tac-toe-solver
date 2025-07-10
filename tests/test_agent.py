from pytest import fixture
from model.agent import Agent
from model.qtable import QTable


@fixture
def agent():
    return Agent(player=1, qtable=QTable())


def test_agent_choose_action(agent: Agent):
    assert agent.choose_action([0,0,0,0,0,0,0,0,0])