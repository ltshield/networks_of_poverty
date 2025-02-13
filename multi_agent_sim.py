import matplotlib.pyplot as plt
# import random
from control_group import Control_Group
from support_group import Support_Group

NUM_ROUNDS = 100

EXPENSE_RATE = -40 # keep negative

#TODO: resources increase and expenses too (RATIO) (increase of income increases potential expenses), expenses increases vs original expenses

DUES = 5

#TODO, where settings are right now, the support group can escape loan debt pit and pay off the loans in about 45 round when provided with 39 dollars.
#DUES ARE 5, INVESTMENT VALUE IS 20 (which increases income by 8 per round), and loan interest rate is 1.0125% (about 15% yearly rate)
#is there a mathematical formula to compare all of these variables and predict future activity?

control_group1 = Control_Group(income_rate=50, expense_rate=EXPENSE_RATE)
control_group2 = Control_Group(income_rate=35, expense_rate=EXPENSE_RATE)
support_group = Support_Group(dues=DUES, income_rate=39, expense_rate=EXPENSE_RATE)

rounds = [j for j in range(NUM_ROUNDS)]

for i in range(NUM_ROUNDS):
    control_group1.run_round()
    control_group2.run_round()
    support_group.run_round()

control_group1.plot_money_debt([i for i in range(NUM_ROUNDS)])
control_group2.plot_money_debt([i for i in range(NUM_ROUNDS)])
support_group.plot_money_debt([i for i in range(NUM_ROUNDS)])

plt.show()