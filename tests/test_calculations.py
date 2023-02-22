from app.calculations import add_nums, subtract_nums, multiply_nums, divide_nums, BankAccount, InsufficientFunds
import pytest

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

# Able to test a range of data
@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (-7, 1, -6),
    (0, 5, 5)
])
def test_add(num1, num2, expected):
    # test add function
    assert True # I do nothing
    # assert will cause an error if "asserts True"
    # assert False # I will stop the code
    assert expected == add_nums(num1,num2)

def test_subtract():
    assert subtract_nums(9, 4) == 5

def test_multiply():
    assert multiply_nums(4, 3) == 12

def test_divide():
    assert divide_nums(20, 4) == 5

def test_bank_set_initial_amt(bank_account):
    assert bank_account.balance == 50

def test_bank_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_withdraw(bank_account):
    bank_account.withdraw(10)
    assert bank_account.balance == 40

def test_bank_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 5) == 55

@pytest.mark.parametrize("deposited, withdrawn, expected", [
    (200, 100, 100),
    (500, 50, 450),
    (1200, 800, 400)
])
def test_bank_transaction(zero_bank_account, deposited, withdrawn, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawn)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(zero_bank_account):
    # Tell pytest that exception is expected
    # Specific type of exception to make sure we're getting the right exceptioin
    with pytest.raises(InsufficientFunds):
        zero_bank_account.withdraw(100)





