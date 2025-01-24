import random

MIN_INCOME_VAL = 10
MAX_INCOME_VAL = 40

class IncomeNode:
    def __init__(self):
        self.value = random.randint(MIN_INCOME_VAL, MAX_INCOME_VAL)