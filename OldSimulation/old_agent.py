import random
import matplotlib.pyplot as plt

from income import IncomeNode
from expense import ExpenseNode
from loans import Loan

"""
In control group, never save money.
In experimental group, excess money goes to communal pool.

The only way out of poverty is investment? Creating more resource nodes?
How do you decide which agents get resource nodes?

Poverty occurs when income == expenses.
Set expense rate with possible variability at random.

Control group should steadily decrease while experimental increases.

Set amount donated to pool every round. ($2)

One round can be one week/one month. Account for interest rates as necessary. (18-24% healthy interest rate for investment loans)
- How much should ROI be so that the investments are worth it and result in linear growth of balance over time.

For now, control and experimental group will have same income/expenses, but only experimental will save money and donate to pool for loans that will help them invest
to increase their income. In theory their balance should increase over time while control's will stay the same.

Implement loan sharks farther down the road.
"""

NUM_ROUNDS = 10

STARTING_MONEY_VAL = 20

# if self.money is under this threshold agent is identified as in poverty
POVERTY_THRESHOLD = 0

# out of 100. ie 20 == 20% chance
EXPENSE_CHANCE = 40

# for testing purposes (make sure it is negative)
INITIAL_DEBT = 0

# loan rates
PREDATORY_RATE = 1.50
HEALTHY_RATE = 1.15

class Agent:
    def __init__(self):
        self.id = 0

        # TODO: randomization for expense nodes (maybe for value of income nodes?)
        self.incomes: list[IncomeNode] = [IncomeNode()]
        # self.expenses: list[ExpenseNode] = []

        self.money: int = STARTING_MONEY_VAL

        self.in_poverty: bool = False
        self.debt: int = INITIAL_DEBT

        # if agent already has a loan, cannot take out another one
        self.has_loan = False
        self.loan = None

        self.expense_history = []
    
    def run_round(self):
        print(f"Agent ID: {self.id}")
        print(f"Money at start of round: {self.money}")

        # collect money from income streams
        for income in self.incomes:
            print(f"Collected {income.value} income.")
            self.money += income.value

        # 15% chance each round to get a random expense
        rand_expense = random.randint(0,100)
        if rand_expense <= EXPENSE_CHANCE:
            new_expense: ExpenseNode = ExpenseNode()
            self.expense_history.append(new_expense.cost)

            # if not enough money to pay expense, take out a loan.
            print(f"Has loan? {self.has_loan}")
            if self.money < abs(new_expense.cost) and not self.has_loan:
                new_expense.cost += self.money
                self.money = 0
                print("Taking out a loan.")
                self.has_loan = True
                self.loan = Loan(loan_value=new_expense.cost, interest_rate=PREDATORY_RATE)
                print("LOAN RATE: ", self.loan.loan_value)

            # try to pay expense first, then pay loan, then debt
            else:
                self.money += new_expense.cost
                print(f"Random expense! Cost Agent {self.id} {new_expense.cost} dollars!")
        else:
            self.expense_history.append(None)

        if self.has_loan and self.money > 0:
            difference = self.loan.loan_value + self.money
            # if difference is negative, not enough to pay off loan
            if difference < 0:
                self.loan.loan_value += self.money
                self.money = 0
            # if difference is positive, enough money to pay off
            elif difference > 0:
                self.money += self.loan.loan_value
                self.loan = None
                self.has_loan = False
            # no longer has loan
            elif difference == 0:
                self.money = 0
                self.loan = None
                self.has_loan = False

        # if loan was not paid off, appreciate it here
        if self.has_loan:
            print(f"Loan left to pay pre-appreciation: {self.loan.loan_value}")
            self.loan.appreciate()
            print(f"Loan left to pay post-appreciation: {self.loan.loan_value}")


        """
        TODO: if has loan, should they pay expense first and then loan?
        if has loan, should I just account for the loan in the debt section?
        when graphing I think loans should be included in the graphed debt
        """
        

        # take leftover money (if any) and try to pay off debt
        if self.debt != 0 and self.money > 0:
            print(f"Agent's debt is currently: {self.debt}")
            print(f"Available money is currently: {self.money}")
            # if they have enough and more to cover the debt, pay it off
            if abs(self.debt) < self.money:
                print("Paid off debt in full.")
                print(f"Had {self.money}, debt was {self.debt}, so has {self.money+self.debt} left.")
                differ: int = self.money + self.debt
                self.debt = 0
                self.money = differ
            # if equal to leftover money, set both equal to zero
            elif abs(self.debt) == self.money:
                print("Paid off debt in full with no money leftover.")
                self.money = 0
                self.debt = 0
            # if they do not have enough to pay it off, pay some
            elif abs(self.debt) > self.money:
                self.debt += self.money
                self.money = 0
        
        # if money available is less than the poverty threshold, in poverty
        if self.money < POVERTY_THRESHOLD:
            print("Not enough money to cover expenses... Now in poverty.")
            self.in_poverty = True
            self.debt += self.money

            # reinitialize money at 0
            self.money = 0
        
        print(f"Money at end of this round: {self.money}")
        print(f"Debt at end of this round: {self.debt}\n")

agent1 = Agent()
money = []
debt = []
rounds = [j for j in range(NUM_ROUNDS)]

for i in range(NUM_ROUNDS):
    agent1.run_round()
    money.append(agent1.money)
    if agent1.has_loan:
        debt.append(agent1.debt+agent1.loan.loan_value)
        print(agent1.debt+agent1.loan.loan_value)
    else:
        debt.append(agent1.debt)
        print(agent1.debt)

plt.plot(rounds, money, marker='o', linestyle='-', label="Money at end of round")
plt.plot(rounds, debt, marker='s', linestyle='--', label="Debt at end of round")
plt.scatter(rounds, agent1.expense_history, facecolors="none", edgecolors="red", s=200, linewidth=2, label="Expense Value")

plt.legend()

plt.show()
