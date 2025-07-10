from model.api import predict


def test_predict():
    res = predict(board=[0,0,0,0,0,0,0,0,0], player=1)
    assert res['position'] == 4


def test_predict_chooses_winning_actions():
    res = predict(board=[1,1,0,-1,-1,0,0,0,0], player=1)
    assert res['position'] == 2

    res = predict(board=[1,1,0,-1,-1,0,0,0,0], player=-1)
    assert res['position'] == 5

    res = predict(board=[1,0,-1, 0,-1,1, 0,0,0], player=-1)
    assert res['position'] == 6