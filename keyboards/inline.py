from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# клавиатура главного меню
start_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👤 Мой профиль", callback_data="profile"),
            InlineKeyboardButton(text="📊 Статистика", callback_data="stats"),
        ],
        [
            InlineKeyboardButton(text="📖 Информация (FAQ)", callback_data="info"),
        ],
        [
            InlineKeyboardButton(text="➕ Сдать аккаунты", callback_data="work"),
        ],
    ]
)


# билдер клавиатуры меню профиля
def profile_key(is_wallet: bool):
    builder = InlineKeyboardBuilder()
    if is_wallet is True:
        text = "👛 Изменить кошелек"
    else:
        text = "👛 Подключить кошелек"

    # Первая строка с двумя кнопками
    builder.row(
        InlineKeyboardButton(text=text, callback_data="profile_wallet"),
        InlineKeyboardButton(text="🌐 Адрес", callback_data="profile_address")
    )

    # Вторая строка с одной кнопкой
    builder.row(
        InlineKeyboardButton(text="💰 Cистема оплаты", callback_data="profile_methode")
    )

    # Третья строка с одной кнопкой
    builder.row(
        InlineKeyboardButton(text="💠 Реферальная система", callback_data="profile_referral")
    )

    # Четвертая строка с одной кнопкой "‹ Назад"
    builder.row(
        InlineKeyboardButton(text="‹ Назад", callback_data="start")
    )

    # Возвращаем объект разметки клавиатуры
    return builder.as_markup()


# билдер админки
def admin_panel_key(position: int):
    builder = InlineKeyboardBuilder()
    if position == 0:
        text = "▶️ Запустить чекер"
    else:
        text = "Чекер работает"
    builder.row(
        InlineKeyboardButton(text=f"{text}", callback_data=f"admin_run_{position}"),
    )

    builder.row(
        InlineKeyboardButton(text=f"📅 Дата последнего запуска", callback_data=f"admin_date"),
    )

    builder.row(
        InlineKeyboardButton(text=f"📥 Пополнить приложение", callback_data=f"admin_payin"),
        InlineKeyboardButton(text=f"📤 Выплата", callback_data=f"admin_payout"),
    )

    builder.row(
        InlineKeyboardButton(text=f"🔍 Найти воркера", callback_data=f"admin_find"),
    )

    return builder.as_markup()


def payout_key():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Подтвердить", callback_data="payout_confirm"),
    builder.button(text="Отмена", callback_data="adminmenu"),

    builder.adjust(2)
    return builder.as_markup()

def control_worker(userid: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="🌀 Обнулить", callback_data=f"workerzero_{userid}"),
    builder.button(text="🚫 Забанить", callback_data=f"workerban_{userid}"),
    builder.button(text="⚖️ Разбан", callback_data=f"workerunban_{userid}"),
    builder.button(text="‹ Назад", callback_data=f"adminmenu"),
    builder.adjust(3)
    return builder.as_markup()

def accept_zero(userid: int, balance: float):
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Подтвердить", callback_data=f"confirmzero_{userid}_{balance}"),
    builder.button(text="Отмена", callback_data=f"adminmenu"),
    builder.adjust(2)
    return builder.as_markup()

def accept_ban(userid: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Подтвердить", callback_data=f"confirmban_{userid}"),
    builder.button(text="Отмена", callback_data=f"adminmenu"),
    builder.adjust(2)
    return builder.as_markup()

def sub_key():
    builder = InlineKeyboardBuilder()
    builder.button(text="Подписаться", url="https://t.me/+CZ6onm92v080ZjU0"),
    builder.adjust(1)
    return builder.as_markup()


def confirm_wallet_key():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Добавить", callback_data=f"confirm_wallet"),
    builder.button(text="Отмена", callback_data=f"profile"),
    builder.adjust(2)
    return builder.as_markup()


def methode_key(choice: int):
    builder = InlineKeyboardBuilder()
    if choice == 0:
        button_one = "· За просмотры ·"
        button_two = "  За Лиды  "
    else:
        button_one = "  За просмотры  "
        button_two = "· За Лиды ·"

    builder.button(text=f"{button_one}", callback_data=f"methode_views"),
    builder.button(text=f"{button_two}", callback_data=f"methode_leads"),
    builder.button(text="‹ Назад", callback_data=f"profile"),
    builder.adjust(2)
    return builder.as_markup()

def confirm_checking():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔍 Отправить на проверку", callback_data=f"check"),
    builder.button(text="‹ Назад", callback_data=f"work"),
    builder.adjust(2)
    return builder.as_markup()

def cancel_key(param: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="Отмена", callback_data=f"{param}"),
    builder.adjust(1)
    return builder.as_markup()


def back_key(param: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="‹ Назад", callback_data=f"{param}"),
    builder.adjust(1)
    return builder.as_markup()


def exit_key(param: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="Выйти", callback_data=f"{param}"),
    builder.adjust(1)
    return builder.as_markup()
