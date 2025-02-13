"""
This was because I was interested in seeing if there was any
kind of formulaic relationship between the variables in 
determining final wealth.

Learned about the shap and seaborn libraries, got to use a model
from sklearn, and got to use a genetic algorithm library to
try and find an equation to explain their relationship.

As we see, the simulation, at least where I have it now,
is more greatly influenced by the loan values and the interest
rates than anything else. (By a landslide). Which makes sense
given that those values are what result in an exponential growth
curve and therefore divergent behavior.
"""
import sys
import os

# This is because I am placing the data analytics in a subdirectory but still
# need to access the files in the host directory

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from agent import Agent
import numpy as np
import random
from loans import Loan
from income import IncomeNode

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import seaborn as sns # library to visualize results
import shap # explainable AI library

"""
Uncomment this if you want to try out the genetic algorithm
that will try to match the results to a function.

# from gplearn.genetic import SymbolicRegressor
"""

np.random.seed(42) # so we get repeatable results

NUM_SAMPLES = 5000
NUM_AGENTS = 5
NUM_ROUNDS = 20

"""
Original Values For Image in Directory:
Initial Income: 10-100
Initial Expenses: 5-90
Due Amounts: 1-10
Loan Amount: 5-20
Interest Rate: 0.01-0.3 (+1)
Investment Return/Round: 1-30
"""

initial_income = np.random.uniform(35,45, NUM_SAMPLES)
initial_expenses = np.random.uniform(40,40, NUM_SAMPLES)
due_amounts = np.random.uniform(5,5, NUM_SAMPLES)
loan_amount = np.random.uniform(1,20,NUM_SAMPLES)
interest_rate = np.random.uniform(0.01,0.40, NUM_SAMPLES)
investment_return = np.random.uniform(1,10, NUM_SAMPLES)

wealths:list[int] = []

for i in range(NUM_SAMPLES):
    INVESTMENT_INCOME_VALUE_PER_ROUND = investment_return[i]
    LOAN_VALUE = loan_amount[i]

    # divide yearly interest rate by 12 (each round is a month)
    INTEREST_RATE = interest_rate[i]/12

    class Support_Group2:
        def __init__(self, dues, income_rate, expense_rate):
            self.agents = [Agent(income_rate=income_rate, expense_rate=expense_rate, group_type="SUPPORT", communal_pool=self) for i in range(NUM_AGENTS)]
            self.dues = dues
            self.communal_money = 0
            self.round_num = 0

        def run_round(self):
            for agent in self.agents:
                agent.run_round()
            
            # after round 4 of collecting money, random agents can be selected to take out investment loans that will help them increase their income to escape the conditions of poverty
                if self.round_num >= 4:
                    self.allocate_loans()

                self.round_num += 1
        
        def allocate_loans(self):
            if self.communal_money >= LOAN_VALUE:

                # how do we select the agents to get the money? should it be weighted by the ones closest to debt? 
                # this weights agents to get the agent with the smallest income-expenses ratio?
                if len([agent for agent in self.agents if not agent.has_loan]) != 0:
                    agent_to_get_loan = random.choices([agent for agent in self.agents if not agent.has_loan], weights=[1/(max(agent.money-agent.debt+1,0.01)) for agent in self.agents if not agent.has_loan], k=1)[0]
                    agent_to_get_loan.has_loan = True
                    self.communal_money -= LOAN_VALUE
                    agent_to_get_loan.incomes.append(IncomeNode(value=INVESTMENT_INCOME_VALUE_PER_ROUND))
                    agent_to_get_loan.loan = Loan(loan_value= LOAN_VALUE, interest_rate=INTEREST_RATE)

    support_group = Support_Group2(dues=due_amounts[i], income_rate=initial_income[i], expense_rate=initial_expenses[i])
    support_group.agents = [Agent(initial_income[i], initial_expenses[i], "SUPPORT", communal_pool=support_group) for i in range(NUM_AGENTS)]
    for i in range(NUM_ROUNDS):
        support_group.run_round()
    richest_agent = max(support_group.agents, key=lambda agent: agent.money)
    mean_wealth = np.mean([agent.money for agent in support_group.agents])
    wealths.append(mean_wealth)

print(len(wealths))
print(wealths[0:10])

# Put into a df
df = pd.DataFrame({
    "initial_income": initial_income,
    "initial_expenses": initial_expenses,
    "loan_amount": loan_amount,
    "interest_rate": interest_rate,
    "investment_return": investment_return,
    "final_wealth": wealths
})

X = df.drop(columns=["final_wealth"])
y = df["final_wealth"]

"""
I am using a random forest regressor because its said to generalize
better to given data. It takes subsets of the data provided and 
creates a regression tree off of it and then averages the outputs of
each of the trees to provide its best guess. Because I'm not looking
at the trees themselves persay, I'm not really worried about readability.
"""
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# How is model doing?
print("\nModel Performance:")
print("MAE:", mean_absolute_error(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred)) # larger errors are larger
print("R² Score:", r2_score(y_test, y_pred)) # measure how model explains variance

# Shap library readout of feature importance
explainer = shap.Explainer(model, X_train)
shap_values = explainer(X_test)
shap.summary_plot(shap_values, X_test)

# Plot of individual data points' final wealth vs initial
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df["initial_income"], y=df["final_wealth"], alpha=0.5)
plt.axhline(0, color="red", linestyle="--", label="Wealth = 0")
plt.xlabel("Initial Income")
plt.ylabel("Final Wealth")
plt.title("Initial Income vs. Final Wealth")
plt.legend()
plt.show()

"""

GENETIC ALGORITHM FOR FORMULA

gp = SymbolicRegressor(population_size=5000, generations=20, function_set=('add', 'sub', 'mul', 'div', 'log', 'sqrt'),
                       metric='mean absolute error', verbose=1, random_state=42)
gp.fit(X, y)
print("Discovered formula:", gp._program)

"""