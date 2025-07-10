from pytest import fixture
from model.qtable import QTable
from model.contracts import State, Action


@fixture
def mock_qtable():
    qtable = QTable()
    states = [
        ([0,0,0,0,0,0,0,0,0], 1),
        ([0,0,0,0,0,0,0,0,0], -1),
        ([1,0,0,0,0,0,0,0,0], -1),
        ([-1,0,0,0,0,0,0,0,0], 1),
    ]
    for pos, player in states:
        state = State.from_list(positions=pos, next_player=player)
        qtable.add_state(state)
    return qtable


def test_qtable_add_state(empty_state, empty_qtable: QTable):
    assert len(empty_qtable.states) == 0
    assert type(empty_state) == State
    assert empty_state not in empty_qtable

    empty_qtable.add_state(empty_state)
    assert len(empty_qtable.states) == 1
    assert empty_state in empty_qtable


def test_qtable_get_random_action(empty_qtable: QTable, empty_state: State):
    assert empty_qtable.get_random_action(empty_state) is not None
    next_state = State.from_list([0,1,0,-1,0,0,0,0,0], next_player=-1)
    assert empty_qtable.get_random_action(next_state)


def test_qtable_value_get_probability(mock_qtable: QTable):
    s = State.from_list([0,0,0,0,0,0,0,0,0], next_player=1)
    p = mock_qtable[s]
    assert p.get_probability(Action(1, player=s.next_player)) == 1 / 9


def test_qtable_value_set_probability(mock_qtable):
    s = State.from_list([0,0,0,0,0,0,0,0,0], next_player=1)
    p = mock_qtable[s]
    action = Action(position=2, player=s.next_player)
    p.set_probability(action=action, value=0.5)
    assert p.get_probability(action) == 0.5
    p.normalize_probabilities()
    assert p.get_probability(action) < 0.5


def test_qtable_value_reward_action(mock_qtable):
    s = State.from_list([0,0,0,0,0,0,0,0,0], next_player=1)
    p = mock_qtable[s]
    action = Action(position=0, player=1)
    old_p = p.get_probability(action)
    p.reward_action(action, adjustment=1.1)
    assert p.get_probability(action) > old_p