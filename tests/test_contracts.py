from pytest import fixture
from model.contracts import State, Action
from model.qtable import QTable, QTableValue


def test_states_with_different_players():
    positions = [0,0,0,0,0,0,0,0,0]
    state1 = State.from_list(positions, next_player=1)
    state2 = State.from_list(positions, next_player=-1)
    assert state1 != state2


def test_state_available_positions(empty_state: State):
    assert len(empty_state.available_positions()) == 9

    positions = [1,0,0,0,0,0,0,0,0]
    state = State.from_list(positions, next_player=1)
    assert state.positions == tuple(positions)
    assert len(state.available_positions()) == 8, state.available_positions()
    assert 0 not in state.available_positions(), state.available_positions()


