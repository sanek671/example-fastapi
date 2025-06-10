import pytest
from app.calc import add, subtract, multiply, divide, BankAccount, InsufficientFunds


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, result", [
    (3, 2, 5),
    (7, 8, 15),
    (45, 64, 109)
])
def test_add(num1, num2, result):
    assert add(num1, num2) == result


def test_subtract():
    assert subtract(7, 3) == 4


def test_multiply():
    assert multiply(8, 3) == 24


def test_divide():
    assert divide(25, 5) == 5


def test_bank_set_init_amount(bank_account):
    # bank_account = BankAccount(50)
    assert bank_account.balance == 50


def test_bank_defoult_amount(zero_bank_account):
    # bank_account = BankAccount()
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    # bank_account = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):
    # bank_account = BankAccount(50)
    bank_account.deposit(20)
    assert bank_account.balance == 70


def test_collect_interest(bank_account):
    # bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


@pytest.mark.parametrize("deposited, withdrew, result", [
    (500, 200, 300),
    (50, 10, 40),
    (1500, 500, 1000)
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, result):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == result


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
