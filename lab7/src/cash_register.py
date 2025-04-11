import datetime
import os


class CashRegister:
    def __init__(self):
        self.sales = {}
        self.cash = 500
        self.sale_id=0
        self.status="Closed"

    def activate(self):
        self.status="Active"

    def sell(self, cost, item_id, amount):
        if not self.status == "Active":
            return False

        self.sales[sale_id] = {
            'time_of_sale': datetime.datetime.now(),
            'item_id': item_id,
            'cost': cost,
            'amount': amount
        }
        self.cash += cost * amount
        sale_id += 1
        return True