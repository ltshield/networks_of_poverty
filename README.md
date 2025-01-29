# networks_of_poverty
**What is it?**
This is a project to simulate the monetary trends of populations who suffer from predatory lending when living close to the poverty line. We hope that this simulation will enable researchers to explore the feasibility of an intervention for real-life populations in situations akin to the one represented here. It is not intended to serve as conclusive evidence of said intervention's effectiveness or as an irrefutable indicator of the results of its real-world application.

**How does it work?**
Agents are connected to resource/income nodes that provide them with a steady source of income each round. The range of quantities for this income is decided by the user and is randomly selected at the initialization of the program. However, that income will remain the same for the duration of the simulation.

The user can also determine the potential for a random expense (of value randomly determined between min/max values decided by the user) to occur in the agent's life each round that will detract from their saved money. 

User also has control over number of rounds and the interest rates of loans.

Money is allocated in the following order:
- Agent gets income from resource node.
- Randomization decides if agent suffers an expense.
    - If an agent does not have sufficient money to pay off the expense and the agent does not have a loan, the agent will pay as much of the expense as it can and then will pull out a loan which will appreciate from that round onward.
    - If an agent does not have sufficient money to pay off the expense and already has a loan, said leftover expense will be added to their debt.
    - If an agent has sufficient funds to pay off the expense immediately, they do so.
- If the agent still has money left over, it will try to pay off the loan value with remaining money.
- If the agent still has money left over after paying off the loan, the leftover money is then applied to any outstanding debt.
- If there is money left over from all of that, it is simply saved by the agent.

The agent's experience is then graphed. (Debt and loans are combined in the legend and expense costs are circled at their value.)

**Helpful Tips When Altering Code:**
Debt and loans are both saved as negative values.

**Future Work:**
- Support group implementation.
    - Agents pay "dues" to the support group first each round.
    - Helpful loaning (less predatory rates)
    - First few rounds no money is lent from support group.
    - Logic for giving out communal money:
        - investments/help paying for expenses/paying off debt/paying off predatory loans
- Network visualization
- Effective graphing for data analysis
    - IQR