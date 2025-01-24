import random

MIN_EXPENSE_VAL = 50
MAX_EXPENSE_VAL = 100

class ExpenseNode:
    def __init__(self):
        self.cost = random.randint(MIN_EXPENSE_VAL, MAX_EXPENSE_VAL)