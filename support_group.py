from agent import Agent
import numpy as np
import random
import matplotlib.pyplot as plt
from loans import Loan
from income import IncomeNode

NUM_CONTROL_AGENTS = 5
INVESTMENT_INCOME_VALUE_PER_ROUND = 8
LOAN_VALUE = 20

# divide yearly interest rate by 12 (each round is a month)
INTEREST_RATE = 1.0125

class Support_Group:
    def __init__(self, dues, income_rate, expense_rate):
        self.agents = [Agent(income_rate=random.randint(45,75), expense_rate=expense_rate, group_type="SUPPORT", communal_pool=self) for i in range(NUM_CONTROL_AGENTS)]
        self.dues = dues
        self.communal_money = 0
        self.communal_money_history = []
        self.round_num = 0

    def run_round(self):
        for agent in self.agents:
            agent.run_round()
        
        # after round 4 of collecting money, random agents can be selected to take out investment loans that will help them increase their income to escape the conditions of poverty
        if self.round_num >= 4:
            self.allocate_loans()

        self.round_num += 1
        self.communal_money_history.append(self.communal_money)

    def plot_money_debt(self, num_rounds):
        num_agents = len(self.agents)
        number_rounds = len(num_rounds)

        agent_money_history = np.zeros((num_agents,number_rounds))

        for i, agent in enumerate(self.agents):
            agent_money_history[i, :] = agent.money_history
        
        money_median = np.median(agent_money_history, axis=0)
        money_q1 = np.percentile(agent_money_history, 25, axis=0)
        money_q3 = np.percentile(agent_money_history, 75, axis=0)

        # print(len(num_rounds))
        # print(len(self.communal_money_history))

        plt.scatter(num_rounds, self.communal_money_history, label="Communal Money", color="greenyellow")
        plt.plot(num_rounds, money_median, label="Median Money", color="green")
        plt.fill_between(num_rounds, money_q1, money_q3, color='green', alpha=0.3, label="Interquartile Range (Q1–Q3)")
        plt.legend()
    
    def allocate_loans(self):
        if self.communal_money >= LOAN_VALUE:
            # how do we select the agents to get the money? should it be weighted by the ones closest to debt? 
            # this weights agents to get the agent with the smallest income-expenses ratio?
            agent_to_get_loan = random.choices([agent for agent in self.agents if not agent.has_loan], weights=[1/(max(agent.money-agent.debt,0.01)) for agent in self.agents if not agent.has_loan], k=1)[0]

            # for agent in self.agents:
            #     print(f"Agent {agent.id} has 1/self-money-self.debt of {1/(agent.money-agent.debt)}")
            # print(f"{agent_to_get_loan.id} should get the loan.")

            agent_to_get_loan.has_loan = True
            self.communal_money -= LOAN_VALUE
            agent_to_get_loan.incomes.append(IncomeNode(value=INVESTMENT_INCOME_VALUE_PER_ROUND))
            agent_to_get_loan.loan = Loan(loan_value= LOAN_VALUE, interest_rate=INTEREST_RATE)

