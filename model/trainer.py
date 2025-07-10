import random
from .engine import Engine
from .agent import Agent


class Trainer:
    def __init__(self, agent1: Agent, agent2: Agent):
        assert agent1.player != agent2.player, "Can not have two agents with the same player id"
        self.agent1 = agent1
        self.agent2 = agent2

    def play_game(self):
        starting_player = random.choice([self.agent1.player, self.agent2.player])
        engine = Engine(starting_player=starting_player)
        while not engine.finished:
            if engine.current_state.next_player == self.agent1.player:
                agent = self.agent1
            else:
                agent = self.agent2
            action = agent.get_random_action(board=list(engine.current_state.positions))
            engine.play(action.position, agent.player)
        return engine

    def reward_agent(self, agent: Agent, engine: Engine):
        for action, state in zip(engine.actions, engine.history[:-1]):
            if action.player != agent.player:
                continue
            if agent.player == engine.winner:
                agent.qtable[state].reward_action(action, adjustment=1.25)
            elif agent.player == engine.loser:
                agent.qtable[state].reward_action(action, adjustment=0.75)
            else:
                agent.qtable[state].reward_action(action, adjustment=1.0)
    
    def train(self, num_games: 5):
        for n in range(num_games):
            if n % 5000 == 0:
                print("Iteration",  n , "of", num_games, f"({round(100 * n / num_games, 3)}%)")
            engine = self.play_game()
            self.reward_agent(agent=self.agent1, engine=engine)
            self.reward_agent(agent=self.agent2, engine=engine)
