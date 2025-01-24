import random
from income import IncomeNode
from expense import ExpenseNode

STARTING_MONEY_VAL = 20

# if self.money is under this threshold agent is identified as in poverty
POVERTY_THRESHOLD = 0

# out of 100. ie 20 == 20% chance
EXPENSE_CHANCE = 40

# for testing purposes (make sure it is negative)
INITIAL_DEBT = -10

class Agent:
    def __init__(self):
        self.id = 0

        # TODO: randomization for expense nodes (maybe for value of income nodes?)
        self.incomes: list[IncomeNode] = [IncomeNode()]
        # self.expenses: list[ExpenseNode] = []

        self.money: int = STARTING_MONEY_VAL

        self.in_poverty: bool = False
        self.debt: int = INITIAL_DEBT
    
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
            self.money -= new_expense.cost
            print(f"Random expense! Cost Agent {self.id} {new_expense.cost} dollars!")
        
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
for i in range(5):
    agent1.run_round()
    # if agent1.in_poverty:
    #     break
