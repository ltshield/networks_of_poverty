from agent import Agent
import matplotlib.pyplot as plt

NUM_CONTROL_AGENTS = 5

class Control_Group:
    def __init__(self, income_rate, expense_rate):
        self.agents = [Agent(income_rate=income_rate, expense_rate=expense_rate) for i in range(NUM_CONTROL_AGENTS)]
    
    def run_round(self):
        for agent in self.agents:
            agent.run_round()
            agent.money_history.append(agent.money)
            agent.debt_history.append(agent.debt)

    def plot_money_debt(self, num_rounds):
        for agent in self.agents:
            plt.plot(num_rounds, agent.money_history, marker='o', color = "red", linestyle='-', label="Money at end of round")
            plt.plot(num_rounds, agent.debt_history, marker='s', color = "red", linestyle='--', label="Debt at end of round")