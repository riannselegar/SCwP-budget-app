import math


class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=''):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def check_funds(self, amount):
        return False if amount > self.get_balance() else True

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        else:
            return False

    def __str__(self):
        printing = str(self.name).center(30, '*') + '\n'

        for item in self.ledger:
            printing += str(item['description'])[:23].ljust(23) + "{:.2f}".format(round(item['amount'], 2))[:7].rjust(
                7) + '\n'

        printing += "Total: " + "{:.2f}".format(round(sum(item['amount'] for item in self.ledger), 2))

        return printing.rstrip()


def create_spend_chart(categories):
    title = "Percentage spent by category\n"

    spentValues = []
    for item in categories:
        soma = round(sum(i['amount'] for i in item.ledger if i['amount'] < 0), 2)
        spentValues.append({'cat': item.name, 'value': soma})

    totalGasto = sum(item['value'] for item in spentValues)

    percentageByCategory = list(math.floor(x['value'] / totalGasto * 10) for x in spentValues)
    percentages = list(range(100, -1, -10))
    yAxis = []

    for n in percentages:
        line = str(n).rjust(3) + "|"
        for i in percentageByCategory:
            if i*10 >= n:
                line += "o".center(3)
            else:
                line += " ".center(3)
        line += " "
        yAxis.append(line)

    xAxis = ("".rjust(len(percentageByCategory)*3+1, "-")).rjust(len(yAxis[0]))

    categoryNames = list(cat.name for cat in categories)
    maxLenName = max(categoryNames, key=len)


    namesAxis = []
    for i in range(len(maxLenName)):
        line = "".ljust(4)
        for name in categoryNames:
            if i < len(name):
                line += name[i].center(3)
            else:
                line += ''.center(3)
        line += " "
        namesAxis.append(line)

    chart = title + '\n'.join(yAxis) + '\n' + xAxis + '\n' + '\n'.join(namesAxis)

    return chart
