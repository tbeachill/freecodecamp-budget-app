class Category:

    def __init__(self, category):
        self.category = category
        self.ledger = []

    def __str__(self):
        # Return a string with a category title line consisting of 30 characters, surrounded by asterisks
        # then return a list of items in the ledger, with the first 23 chars of the description and amounts
        # right-aligned with 2 decimal places. Then display a total amount.

        star_number = int( (30 - len(str(self.category))) / 2 )
        title_string = "*" * star_number + str(self.category) + "*" * star_number
        ledger_string = ""
        total = 0

        for entry in self.ledger:
            amount = entry["amount"]
            desc = entry["description"]

            if len(desc) > 23:
                ledger_string = ledger_string + entry["description"][:23] + f"{amount:>7.2f}\n"
            else:
                desc = desc + (" " * (23 - len(desc)))
                ledger_string = ledger_string + desc + f'{amount:>7.2f}\n'

            total += amount

        return title_string + "\n" + ledger_string + "Total: " + f"{total:.2f}"

    def deposit(self, amount, description = ""):
        # append the deposit to the ledger with a description and the deposit amount

        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description = ""):
        # withdraw funds if there is enough in the budget

        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False

    def get_balance(self):
        # get the current balance by adding up the total of the transactions in the ledger

        balance = 0
        for entry in self.ledger:
            balance += entry["amount"]

        return balance

    def transfer(self, amount, category):
        # transfer balance from the self object to another specified object

        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to " + str(category.category))
            category.deposit(amount, "Transfer from " + str(self.category))
            return True
        else:
            return False

    def check_funds(self, amount):
        # check if the amount specified is available

        if amount > self.get_balance():
            return False
        else:
            return True


def create_spend_chart(categories):
    # create an ascii spending bar chart for percentage of total spending from each category

    spent_dict = {}
    total_spent = 0

    # calculate the amount spent in each category and an overall total spent
    for cat in categories:
        cat_total = 0
        for entry in cat.ledger:
            if entry["amount"] < 0:
                cat_total += abs(entry["amount"])
                total_spent += abs(entry["amount"])

        spent_dict[cat.category] = cat_total
    
    # calculate percentage spent for each category and round down to nearest 10
    for key, value in spent_dict.items():
        spent_dict[key] = int(round( value / total_spent, 2) * 100)
    
    out_string = "Percentage spent by category" # title string

    # add percentage labels
    max_len = 0
    i = 100
    while i >= 0:
        out_string = out_string + "\n" + f"{i:>3}" + "| "

        # add "o" for bars
        for cat in categories:
            if spent_dict[cat.category] >= i:
                out_string = out_string + "o  "
            else:
                out_string = out_string + "   "

            if max_len < len(cat.category):
                max_len = len(cat.category)

        i -= 10
    
    out_string = out_string + "\n    " + ( (len(categories) * 3) + 1) * "-" + "\n     " # x axis

    # bar labels
    i = 0
    while i < max_len:
        for cat in categories:
            if i < len(cat.category):
                out_string = out_string + cat.category[i] + "  "
            else:
                out_string = out_string + "   "
        
        i += 1
        if i < max_len:
            out_string = out_string + "\n     "

    return out_string