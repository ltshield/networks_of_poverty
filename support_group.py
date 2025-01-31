from agent import Agent
import numpy as np
import random
import matplotlib.pyplot as plt

NUM_CONTROL_AGENTS = 5

class Support_Group:
    def __init__(self, dues, income_rate, expense_rate):
        self.agents = [Agent(income_rate=random.randint(45,75), expense_rate=expense_rate) for i in range(NUM_CONTROL_AGENTS)]
        self.dues = dues
        self.communal_money = []

    def run_round(self):
        for agent in self.agents:
            agent.run_round()

    def plot_money_debt(self, num_rounds):
        num_agents = len(self.agents)
        number_rounds = len(num_rounds)

        agent_money_history = np.zeros((num_agents,number_rounds))

        for i, agent in enumerate(self.agents):
            agent_money_history[i, :] = agent.money_history
        
        money_median = np.median(agent_money_history, axis=0)
        money_q1 = np.percentile(agent_money_history, 25, axis=0)
        money_q3 = np.percentile(agent_money_history, 75, axis=0)

        plt.plot(num_rounds, money_median, label="Median Money", color="green")
        plt.fill_between(num_rounds, money_q1, money_q3, color='green', alpha=0.3, label="Interquartile Range (Q1–Q3)")