def add_nums(num1: int, num2: int):
    return num1 + num2

def subtract_nums(num1: int, num2: int):
    return num1 - num2

def multiply_nums(num1: int, num2: int):
    return num1 * num2

def divide_nums(num1: int, num2: int):
    return num1 / num2

# How to define our own exception
class InsufficientFunds(Exception):
    pass

class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds("Insufficient funds in account")

        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1