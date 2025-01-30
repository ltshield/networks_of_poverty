# import random

from income import IncomeNode
from expense import ExpenseNode
# from loans import Loan

STARTING_MONEY_VAL = 0

class Agent:
    def __init__(self, income_rate, expense_rate):
        self.id = 0

        # TODO: randomization for expense nodes (maybe for value of income nodes?)
        self.incomes: list[IncomeNode] = [IncomeNode(value=income_rate)]
        self.expenses: list[ExpenseNode] = [ExpenseNode(cost=expense_rate)]
        
        # self.expenses: list[ExpenseNode] = []

        self.money: int = STARTING_MONEY_VAL

        self.in_poverty: bool = False

        # if agent already has a loan, cannot take out another one
        self.has_loan = False
        # agent's loan is their debt
        self.debt = None
        
        self.money_history = []
        self.debt_history = []

        self.expense_history = []
    
    def run_round(self):

        # collect money from income streams
        for income in self.incomes:
            self.money += income.value

        for expense in self.expenses:
            self.money += expense.cost