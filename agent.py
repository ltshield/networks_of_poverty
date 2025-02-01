import random

from income import IncomeNode
from expense import ExpenseNode
# from loans import Loan

STARTING_MONEY_VAL = 0

class Agent:
    def __init__(self, income_rate, expense_rate, group_type, communal_pool=None):
        self.id = random.randint(0,1000)
        self.group_type = group_type

        self.communal_pool = communal_pool

        # TODO: randomization for expense nodes (maybe for value of income nodes?)
        self.incomes: list[IncomeNode] = [IncomeNode(value=income_rate)]
        self.expenses: list[ExpenseNode] = [ExpenseNode(cost=expense_rate)]
        
        # self.expenses: list[ExpenseNode] = []

        self.money: int = STARTING_MONEY_VAL

        self.in_poverty: bool = False

        # if agent already has a loan, cannot take out another one
        self.has_loan = False
        self.loan = 0
        # agent's loan is their debt
        self.debt = 0
        
        self.money_history = []
        self.debt_history = []

        self.expense_history = []
    
    def run_round(self):

        if self.group_type == "CONTROL":
            self.run_round_control()
        
        elif self.group_type == "SUPPORT":
            self.run_round_support()

        else:
            print("Error, unknown group type.")

    def run_round_support(self):
        
        # collect money from income streams
        for income in self.incomes:
            self.money += income.value

        # pay support group money
        self.money -= 5
        self.communal_pool.communal_money += 5

        for expense in self.expenses:
            self.money += expense.cost
        
        if self.has_loan:
            if self.money > self.loan.loan_value:
                self.money -= self.loan.loan_value
                self.has_loan = False
                self.loan = None
            elif self.money == self.loan.loan_value:
                self.money = 0
                self.has_loan = False
                self.loan = None
            elif self.money < self.loan.loan_value:
                self.loan.loan_value -= self.money
                self.loan.appreciate()
                self.money = 0
        
        self.money_history.append(self.money)
        self.debt_history.append(self.debt)
    
    def run_round_control(self):
        
        for income in self.incomes:
            self.money += income.value

        for expense in self.expenses:
            self.money += expense.cost
        
        self.money_history.append(self.money)
        self.debt_history.append(self.debt)