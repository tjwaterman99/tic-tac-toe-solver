from pytest import fixture
from model.contracts import State
from model.qtable import QTable


@fixture
def empty_state() -> State:
    positions = [0,0,0,0,0,0,0,0,0]
    state = State.from_list(positions, next_player=1)
    return state


@fixture
def empty_qtable():
    return QTable()