from pytest import fixture
from model.engine import Engine


@fixture
def engine():
    return Engine(starting_player=1)


def test_engine(engine: Engine):
    assert engine.current_state.next_player == 1
    assert not engine.finished
    assert not engine.winner

    engine.play(0, 1)
    assert len(engine.history) == 2
    assert engine.current_state.positions[0] == 1
    assert not engine.finished
    assert not engine.winner

    engine.play(3, -1)
    assert len(engine.history) == 3
    assert engine.current_state.positions[3] == -1
    assert not engine.finished
    assert not engine.winner

    engine.play(1, 1)
    engine.play(4, -1)
    engine.play(2, 1)
    assert engine.finished
    assert engine.winner == 1


def test_engine_draw(engine: Engine):
    engine.play(0, 1)
    engine.play(1, -1)
    engine.play(2, 1)
    engine.play(3, -1)
    engine.play(4, 1)
    engine.play(5, -1)
    engine.play(7, 1)
    engine.play(6, -1)
    engine.play(8, 1)    
    assert engine.finished
    assert engine.winner is None
    assert engine.draw
