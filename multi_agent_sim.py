import matplotlib.pyplot as plt
from control_group import Control_Group
from support_group import Support_Group

NUM_ROUNDS = 10

INCOME_RATE_W_SAVING = 50
UNHEALTHY_INCOME_RATE_WO_SAVING = 40
EXPENSE_RATE = -40 # keep negative

DUES = 5

control_group = Control_Group(income_rate=UNHEALTHY_INCOME_RATE_WO_SAVING, expense_rate=EXPENSE_RATE)
support_group = Support_Group(dues=DUES, income_rate=INCOME_RATE_W_SAVING, expense_rate=EXPENSE_RATE)

rounds = [j for j in range(NUM_ROUNDS)]

for i in range(NUM_ROUNDS):

    control_group.run_round()
    support_group.run_round()

control_group.plot_money_debt([i for i in range(NUM_ROUNDS)])
support_group.plot_money_debt([i for i in range(NUM_ROUNDS)])

# plt.legend()

plt.show()