class Account:
    MINIMUM = 0

    def __init__(self, name, balance=0):
        self.__account_name: str = name
        self.__account_balance: float = balance
        self.set_balance(self.__account_balance)

    def get_balance(self):
        return self.__account_balance

    def get_name(self):
        return self.__account_name

    def set_balance(self, amount):
        self.__account_balance = amount

        if self.get_balance() < self.MINIMUM:
            self.__account_balance = self.MINIMUM

    def set_name(self, name):
        self.__account_name = name

    def deposit(self, amount):
        if amount <= 0:
            return False
        else:
            self.set_balance(self.get_balance() + amount)
            return True

    def withdraw(self, amount):
        if 0 >= amount or amount > self.get_balance() - self.MINIMUM:
            return False
        else:
            self.set_balance(self.get_balance() - amount)
            return True