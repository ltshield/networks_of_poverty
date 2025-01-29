# TODO: implement loaning system with interest rates (predatory and supportive) to help with expenses
# as if expenses need to be paid that round!

class Loan:
    def __init__(self, loan_value, interest_rate):
        self.loan_value = loan_value
        self.interest_rate = interest_rate

    def appreciate(self):
        self.loan_value *= self.interest_rate
