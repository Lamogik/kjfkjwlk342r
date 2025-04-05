from aiogram.fsm.state import State, StatesGroup

# состояния бота, которые сохраняют входящие сообщения для дальнейшей обработки
class AddWallet(StatesGroup):
    wallet = State()

class AddAccounts(StatesGroup):
    strings = State()
    confirm_strings = State()

class TestPay(StatesGroup):
    amount = State()
    address = State()

class AdminFind(StatesGroup):
    username = State()

class AdminZeroWorker(StatesGroup):
    userid = State()

class AdminBalanceApp(StatesGroup):
    enter_payin = State()