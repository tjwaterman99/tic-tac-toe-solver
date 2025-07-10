# tic-tac-toe-solver

> https://tictactoe.tjwaterman.com/

A reinforcement-learning based tic-tac-toe solver.

## Prequisites

Install python3.11 (or any modern version of Python will probably work), as well as the AWS SAM cli.

```
brew install aws-sam-cli
python3.11 -m venv .venv
.venv/bin/activate
pip install pytest
```

## Train

```
python -m model
```

## Test

```
sam local invoke -e events/event.json
```

Or run the test suite.

```
python -m pytest
```

Or start the local webserver and query it.

```
sam local start-api
http post http://127.0.0.1:3000/predict board:="[1,0,-1,1,-1,0,0,0,0]" player:="1"
```

## eploy

Ensure your AWS credentials are present.

```
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
```

```
sam deploy
```

## predict

```
pipx install httpie
http post https://tic-tac-toe-solver.tjwaterman.com/predict board:="[1,0,-1,1,-1,0,0,0,0]" player:="1"
```
