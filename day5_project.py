class BankAcount:

    def __init__(self, account_holder, account_number, balance):
        self.account_holder = account_holder
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        if amount < 0:
            print("amount cannot be negative")
        else:
            self.balance = self.balance + amount
            print(f"Deposited:{amount} . New_Amount:{self.balance}")
            
    def withdraw(self, amount):

        if amount > self.balance:
            print("Insufficient balance")
        else:
            self.balance = self.balance - amount
            print(f"Withdrawn {amount}. New balance: {self.balance}")
    def display_balance(self):
        print(f"Final balance of {self.account_holder} is {self.balance}")



account1 = BankAcount("Vibhav", 123456, 50000)
account2 = BankAcount("Priya", 8910112, 25000)
account1.deposit(5000)
account1.withdraw(2000)
account2.withdraw(100000)
account1.display_balance()
account2.display_balance()