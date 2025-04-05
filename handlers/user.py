import aiohttp
from datetime import datetime, time
import time as time1
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext


from cryptopay import CryptoPay, TESTNET
from cryptopay.types import Invoice

# импорты пактов
from keyboards.inline import *
from settings import *
from utils.states import *
from filters.admin_filter import IsAdmin
from tt_selenium_check import get_views_with_selenium
from settings import settings
from main import db

router = Router()

# сообщение на команду /start и на кнопку back to menu
@router.message(CommandStart())
async def start_bot(message: Message,
                    bot: Bot,
                    state: FSMContext):
    await state.clear()
    await db.connect()
    if await db.get("SELECT userid from bannedUsers WHERE userid = ?", [message.from_user.id, ]) is None:
        await db.close()
        start_params = message.text.split()
        if len(start_params) > 1:
            referral_code = start_params[1]
            await db.addUser(message.from_user.id, message.from_user.username, 0.0, " ", 0, 0, 0, 0, 0, 0.0, 0.0)
            await db.addRefUser(message.from_user.id, message.from_user.username, referral_code)
            await message.answer(f"""🏠 Главное меню:""", reply_markup=start_key)
        else:
            await db.addUser(message.from_user.id, message.from_user.username, 0.0, " ", 0, 0, 0, 0, 0, 0.0, 0.0)
            await message.answer(f"""🏠 Главное меню:""", reply_markup=start_key)
    else:
        await db.close()
        await message.answer("""🔒 У тебя нет доступа к боту. Свяжись с администрацией проекта
    
|  Причина: <b><i>заблокирован</i></b>""", parse_mode="HTML")


@router.callback_query(F.data.startswith("start"))
async def start_bot_call(callback: CallbackQuery):
    await callback.message.edit_text(f"""🏠 Главное меню:""", reply_markup=start_key)
    await callback.answer()

@router.callback_query(F.data == "profile")
async def profile_menu(callback: CallbackQuery):
    result = await db.prfilie_info_selector(callback.from_user.id)
    print(result)
    print(type(result))

    if str(result[4]) == " " or str(result[4]) == "None":
        wallet_status = "не подключен"
        is_wallet = False
    else:
        wallet_status = "подключен"
        is_wallet = True

    if int(result[5]) == 0:
        cash_methode = "за просмотры"
    else:
        cash_methode = "за Лиды"

    await callback.message.edit_text(f"""👤 Твой профиль:
    
|  ID: <code>{callback.from_user.id}</code>
|  Аккаунтов на проверке: <b><i>{result[7]}</i></b>
|  Аккаунтов выплачено: <b><i>{result[8]}</i></b>
|  Кол-во лидов: <b><i>{result[11]}</i></b>
|  Баланс: <b><i>{result[3]} $</i></b>

⚙️ Параметры:

|  Кошелек: <b><i>{wallet_status}</i></b>
|  Система оплаты: <b><i>{cash_methode}</i></b>

🔗 Ссылка для ворка: <code>https://t.me/avito_mobot?start={result[10]}</code>""", parse_mode="HTML", reply_markup=profile_key(is_wallet))
    await callback.answer()

# обработка кнопок меню "Мой профиль"
@router.callback_query(F.data.startswith("profile_"))
async def profile_keys_handler(callback: CallbackQuery,
                               state: FSMContext):
    menu = callback.data.split("_")[1]
    if menu == "wallet":
        await state.set_state(AddWallet.wallet)
        await callback.message.edit_text("👛 Введи адрес кошелька:\n\n<b>⚠️ Убедись что указанный адрес принимает USDT в сети BEP20</b>", parse_mode="HTML", reply_markup=cancel_key("profile"))
    elif menu == "methode":
        await state.clear()
        methode = await db.methode_picker(callback.from_user.id)
        print(methode)
        await callback.message.edit_text("💰 Выбери систему оплаты для начисления средств:", reply_markup=methode_key(int(methode)))
    elif menu == "referral":
        await state.clear()
        bot_url = "https://t.me/AMNEZIA_ROBOT?start="
        referral_code = await db.refUrl_picker(callback.from_user.id)
        await callback.message.edit_text(f"""💠 Реферальная система: <b><i>получай 10% от прибыли c каждого приглашенного пользователя</i></b>

Твоя ссылка: <code>{bot_url + referral_code}</code>""", parse_mode="HTML", reply_markup=back_key("profile"))

    elif menu == "address":
        await state.clear()
        result = await db.wallet_selector(callback.from_user.id)
        if result == " " or result == "None":
            await callback.answer("Нет активного кошелька", show_alert=True)
        else:
            await callback.message.edit_text(f"*🌐 Адрес: *||{result}||", parse_mode="MarkdownV2", reply_markup=back_key("profile"))

    await callback.answer()


@router.message(AddWallet.wallet)
async def get_wallet(message: Message,
                     state: FSMContext):
    await state.update_data(wallet=message.text)
    await message.answer(f"<b>⚠ Подтвердаешь <code>{message.text}</code> в качестве кошелька для авто-выплат?</b>", parse_mode="HTML", reply_markup=confirm_wallet_key())


@router.callback_query(AddWallet.wallet)
async def confirm_wallet(callback: CallbackQuery,
                         state: FSMContext):
    data = await state.get_data()
    wallet = data.get("wallet")
    print(wallet)
    await db.wallet_updater(callback.from_user.id, wallet)

    result = await db.prfilie_info_selector(callback.from_user.id)
    wallet_status = "подключен"

    if int(result[5]) == 0:
        cash_methode = "за просмотры"
    else:
        cash_methode = "за Лиды"

    await state.clear()
    await callback.message.edit_text(fr"""👤 Твой профиль:

|  ID: <code>{callback.from_user.id}</code>
|  Аккаунтов на проверке: <b><i>{result[7]}</i></b>
|  Аккаунтов выплачено: <b><i>{result[8]}</i></b>
|  Кол-во лидов: <b><i>{result[11]}</i></b>
|  Баланс: <b><i>{result[3]} $</i></b>

⚙️ Параметры:

|  Кошелек: <b><i>{wallet_status}</i></b>
|  Система оплаты: <b><i>{cash_methode}</i></b>

🔗 Ссылка для ворка: <code>https://t.me/avito_mobot?start={result[10]}</code>""", parse_mode="HTML", reply_markup=profile_key(True))
    await callback.answer("Кошелек успешно подключен", show_alert=True)

@router.callback_query(F.data.startswith("methode_"))
async def profile_keys_handler(callback: CallbackQuery):
    await db.methode_switcher(callback.from_user.id)
    methode = await db.methode_picker(callback.from_user.id)
    await callback.message.edit_text("💰 Выбери систему оплаты для начисления средств:", reply_markup=methode_key(int(methode)))
    await callback.answer()


@router.callback_query(F.data == "stats")
async def profile_menu(callback: CallbackQuery):
    ref_count = await db.get_referral_count(callback.from_user.id)
    total_count_of_accs = await db.totalCountAcc_picker(callback.from_user.id)
    await callback.message.edit_text(f"""📊 Статистика:

|  Всего аккаунтов добавлено: <b><i>{total_count_of_accs}</i></b>
|  Кол-во рефералов: <b><i>{ref_count}</i></b>""", parse_mode="HTML", reply_markup=back_key("start"))


@router.callback_query(F.data == "info")
async def profile_menu(callback: CallbackQuery):
    await callback.message.edit_text(f"""📖 Информация:

Здесь будет общая информация о проекте, а также ответы на часто задаваемые вопросы. Ссылки на ресурсы""", parse_mode="HTML", reply_markup=back_key("start"))


@router.callback_query(F.data == "work")
async def profile_menu(callback: CallbackQuery,
                       state: FSMContext):
    if await db.payout_status_picker(settings.bots.admin_id) == 0:
        await state.set_state(AddAccounts.strings)
        await callback.message.edit_text(f"""🕵️‍♂️ Сдать аккаунты:
    
<b>Укажи @username аккаунта. Если аккаунтов несколько - указывай каждый тег с новой строки</b>""", parse_mode="HTML", reply_markup=back_key("start"))
    else:
        await callback.answer("Бот работает над процессом выплат. Пожалуйста подожди", show_alert=True)

@router.message(AddAccounts.strings)
async def profile_menu(message: Message,
                       state: FSMContext):
    await state.set_state(AddAccounts.confirm_strings)

    tags = message.text.splitlines()
    valid_tags = []
    string = ""

    for item in tags:
        if item.startswith("@") is True:
            valid_tags.append(item)

    valid_len = len(valid_tags)
    valid_tags = list(dict.fromkeys(valid_tags))
    await state.update_data(confirm_str=valid_tags)

    for item in valid_tags:
        string += f"\n{item}"

    await message.answer(f"""✉️ Отправить Tik-Tok аккаунт(ы) на модерацию:
    
|  Всего строк: <b><i>{len(tags)}</i></b>
|  Валидных тегов: <b><i>{len(valid_tags)}</i></b>
|  Дублей очищено: <b><i>{valid_len - len(valid_tags)}</i></b>


📒 Список аккаунтов: <b><i>({len(valid_tags)})</i></b>{string}""", parse_mode="HTML", reply_markup=confirm_checking())


@router.callback_query(AddAccounts.confirm_strings)
async def profile_menu(callback: CallbackQuery,
                       state: FSMContext):
    tik_tok_url = "https://www.tiktok.com/"
    data = await state.get_data()
    strings = data.get("confirm_str")
    result = 0
    print(strings)

    for item in strings:
        url = tik_tok_url + item
        print(url)
        count = await db.addTtAccount(callback.from_user.id, item, url, 0, 0, 0, 0)
        result = result + count
    await state.clear()
    await callback.message.edit_text(f"🚰 Аккаунтов успешно добавлено: <b><i>{result}</i></b>", parse_mode="HTML", reply_markup=exit_key("start"))
    await callback.answer()

    """A D M I N  P A N E L"""

cp = CryptoPay(token=settings.bots.crpt_token, api_server=TESTNET)


@router.message(Command("admin"), IsAdmin([settings.bots.admin_id, 6748143864]))
async def admin_panel(message: Message,
                      state: FSMContext):
    await state.clear()
    await db.addAdmin(message.from_user.id, 0, 0, "нет")
    await message.answer("""<b><i>🤑 Приветствую тебя, Админ!</i></b>""", parse_mode="HTML", reply_markup=admin_panel_key(0))


@router.callback_query(F.data == "adminmenu", IsAdmin([settings.bots.admin_id, 6748143864]))
async def admin_panel(callback: CallbackQuery,
                      state: FSMContext):
    await state.clear()
    await callback.message.edit_text("""<b><i>🤑 Приветствую тебя, Админ!</i></b>""", parse_mode="HTML", reply_markup=admin_panel_key(0))
    await callback.answer()


@router.callback_query(F.data.startswith("admin_"))
async def admin_key_handler(callback: CallbackQuery,
                            state: FSMContext,
                            bot: Bot):
    await state.clear()
    command = callback.data.split("_")[1]
    if command == "run":
        current_time = datetime.now()
        current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        await db.last_check_date_updater(callback.from_user.id, current_time)
        await db.checker_status_updater(callback.from_user.id)
        status = await db.checker_status_picker(callback.from_user.id)
        await callback.message.edit_text("""<b><i>🤑 Приветствую тебя, Админ!</i></b>""", parse_mode="HTML", reply_markup=admin_panel_key(status))
        if status == 1:
            user_list = await db.moderatedAccUser_picker()
            print(user_list)
            worker_data = [t[0] for t in user_list]
            for worker in worker_data:
                tt_acc_list = await db.moderatedAccList_picker(worker)
                tt_url_data = [t[0] for t in tt_acc_list]
                for tt_url in tt_url_data:
                    time1.sleep(5)
                    count_of_views = get_views_with_selenium(tt_url)
                    await db.count_of_views_updater(tt_url, count_of_views)
                    balance_per_acc = float(count_of_views) * 0.001
                    await db.checker_balance_updater(int(worker), balance_per_acc)
            await db.checker_status_updater(callback.from_user.id)
            status = await db.checker_status_picker(callback.from_user.id)
            await callback.message.edit_text("""<b><i>🤑 Приветствую тебя, Админ!</i></b>""", parse_mode="HTML",
                                             reply_markup=admin_panel_key(status))

    elif command == "payin":
        await state.set_state(AdminBalanceApp.enter_payin)
        await callback.message.edit_text("""<b><i>📥 Пополнить приложение</i></b>
        
|  Валюта пополнения <b><i>USDT</i></b>
        
<b><i>✏️ Введи сумму инвойса на пополнение приложения целым (99) или дробным числом (99.99)</i></b>""", parse_mode="HTML", reply_markup=cancel_key("adminmenu"))
        await callback.answer()

    elif command == "payout":
        amonut_to_pay = await db.payout_total_balance_picker()
        count_of_workers_to_pay = await db.payout_count_worker_picker()
        await callback.message.edit_text(f"💰 Подтверди процесс выплат\n\n|  Всего к оплате: <b><i>{amonut_to_pay}$</i></b>\n|  Воркеров с зп: <b><i>{count_of_workers_to_pay[0]}</i></b>\n\n<b><i>⚠ Убедись что на балансе приложения достаточно средств для отправки всех чеков</i></b>", parse_mode="HTML", reply_markup=payout_key())
        await callback.answer()

    elif command == "find":
        await state.set_state(AdminFind.username)
        await callback.message.edit_text("""👁 Введи <b><i>ID</i></b> воркера:""", parse_mode="HTML",  reply_markup=cancel_key("adminmenu"))
        await callback.answer()

    elif command == "date":
        date = await db.last_check_date_picker(callback.from_user.id)
        await callback.answer(f"Последний чекинг: {date}", show_alert=True)


@router.message(AdminBalanceApp.enter_payin)
async def get_payin(message: Message,
                    state: FSMContext):
     amount = float(message.text)
     invoice = await cp.create_invoice(amount, "TON")
     await message.answer(f"""💸 Оплати баланс приложения: {invoice.mini_app_invoice_url}

<b><i>⚠️ Зачисление происходит в течении 3 минут. Проверь баланс приложения в CryptoBot</i></b>""", parse_mode="HTML", reply_markup=exit_key("adminmenu"))
     invoice.await_payment(message=message)
     await state.clear()


@cp.polling_handler()
async def handle_payment(
    invoice: Invoice,
    message: Message,
) -> None:
    await message.answer(
        f"payment received: {invoice.amount} {invoice.asset}",
    )


@router.message(AdminFind.username)
async def get_username_worker(message: Message,
                              state: FSMContext):
    try:
        userid = int(message.text)
        worker_info = await db.user_picker(userid)
        print(worker_info)
        if worker_info is not None:
            await db.connect()
            status = await db.get("SELECT userid from bannedUsers WHERE userid = ?", [userid, ])
            await db.close()
            if status is None:
                isBanned = "не забанен"
            else:
                isBanned = "забанен"

            await message.answer(f"""📈 Статистика воркера <code>{userid}</code>
    
|  @username: <b><i>{worker_info[0]}</i></b>
|  Баланс: <b><i>{worker_info[1]} $</i></b>
|  Аккаунтов за все время: <b><i>{worker_info[2]}</i></b>
|  Аккаунтов на модерации: <b><i>{worker_info[3]}</i></b>
|  Аккаунтов выплачено: <b><i>{worker_info[4]}</i></b>
|  Статус: <b><i>{isBanned}</i></b>""", parse_mode="HTML", reply_markup=control_worker(userid))

            await state.clear()
        else:
            await message.answer("""❗️ Такого воркера не существует. Попробуй снова""", reply_markup=cancel_key("adminmenu"))
    except ValueError:
        await message.answer("""❗️ <b><i>ID</i></b> указан в неверном формате. Попробуй снова""", parse_mode="HTML",
                             reply_markup=cancel_key("adminmenu"))

@router.callback_query(F.data.startswith("workerban_"))
async def start_ban_worker(callback: CallbackQuery):
    user_id = callback.data.split("_")[1]
    await db.connect()
    username = await db.get("SELECT username FROM users WHERE userid = ?", (user_id,))
    await db.close()
    print(username)
    await callback.message.edit_text(f"🚫 Забанить воркера <b><i>@{username[0]}</i></b>?", parse_mode="HTML", reply_markup=accept_ban(user_id))
    await callback.answer()


@router.callback_query(F.data.startswith("confirmban_"))
async def confirm_ban_worker(callback: CallbackQuery):
    userid = callback.data.split("_")[1]
    await db.banWorker(userid)
    await callback.message.edit_text("🚫 Воркер <b><i>успешно забанен</i></b>", parse_mode="HTML", reply_markup=exit_key("adminmenu"))
    await callback.answer()


@router.callback_query(F.data.startswith("workerzero_"))
async def zero_worker(callback: CallbackQuery,
                      state: FSMContext):
    user_id = callback.data.split("_")[1]
    await db.connect()
    username = await db.get("SELECT username FROM users WHERE userid = ?", (user_id,))
    balance = await db.get("SELECT balance FROM users WHERE userid = ?", (user_id,))
    await db.close()
    await state.set_state(AdminZeroWorker.userid)
    await state.update_data(user_id=user_id)
    print(username)
    await callback.message.edit_text(f"💰 Текущий баланс воркера <b><i>@{username[0]}: {balance[0]}$</i></b>\n\n⌨️ Введи сумму в формате <b><i>0.0</i></b>", parse_mode="HTML", reply_markup=cancel_key("adminmenu"))
    await callback.answer()


@router.message(AdminZeroWorker.userid)
async def confirm_zero_worker(message: Message,
                              state: FSMContext):
    balance = float(message.text)
    data = await state.get_data()
    user_id = data.get("user_id")
    await db.balance_updater(user_id, balance)
    await db.connect()
    username = await db.get("SELECT username FROM users WHERE userid = ?", (user_id,))
    await db.close()
    await state.clear()
    await message.answer(f"✅ Баланс пользователя <b><i>@{username[0]} успешно изменен: {balance}$</i></b>", parse_mode="HTML", reply_markup=exit_key("adminmenu"))

@router.callback_query(F.data.startswith("workerunban_"))
async def start_ban_worker(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    await db.connect()
    if await db.get("SELECT userid from bannedUsers WHERE userid = ?", [user_id]) is None:
        await callback.answer("Этот пользователь не заблокирован", show_alert=True)
    else:
        await db.change("DELETE FROM bannedUsers WHERE userid = ?", [user_id])
        await callback.answer("Пользователь успешно разблокирован", show_alert=True)
    await db.close()

@router.callback_query(F.data == "payout_confirm")
async def payout_confirming_send(callback: CallbackQuery,
                                 bot: Bot):
    await db.payout_status_updater(callback.from_user.id)
    user_list = await db.payout_worker_picker()
    print(user_list)
    worker_data = [t[0] for t in user_list]
    for worker in worker_data:
        await db.connect()
        methode_pay = await db.get("SELECT methode FROM users WHERE userid = ?", (worker,))
        if int(methode_pay[0]) == 0:
            amount = await db.payout_balance_views_picker(worker)
            print(amount)
            # check = await cp.create_check(float(amount), "TON", f"{worker}")
            account = await db.moderationCountAcc_picker(worker)
            await bot.send_message(chat_id=worker, text=f"Активируй чек, чтобы получить выплату {amount}")
            '''await bot.send_message(chat_id=worker,
                                   text=f"💸 Активируй чек, чтобы получить выплату <b><i>{amount}$</i></b>\n\n{check.bot_check_url}",
                                   parse_mode="HTML")'''
            await db.balance_updater(worker, amount)
            await db.moderation_account_zero_updater(worker)
            await db.moderation_list_deleter(worker)
            await db.payed_accounts_updater(worker, account)
            await db.connect()
            await db.change("UPDATE users SET views_balance = 0 WHERE userid = ?", (worker,))
        else:
            amount = await db.payout_balance_leads_picker(worker)
            print(amount)
            # check = await cp.create_check(float(amount), "TON", f"{worker}")
            account = await db.moderationCountAcc_picker(worker)
            await bot.send_message(chat_id=worker, text=f"Активируй чек, чтобы получить выплату {amount}")
            '''await bot.send_message(chat_id=worker,
                                   text=f"💸 Активируй чек, чтобы получить выплату <b><i>{amount}$</i></b>\n\n{check.bot_check_url}",
                                   parse_mode="HTML")'''
            await db.balance_updater(worker, amount)
            await db.moderation_account_zero_updater(worker)
            await db.moderation_list_deleter(worker)
            await db.payed_accounts_updater(worker, account)
            await db.connect()
            await db.change("UPDATE users SET leads_balance = 0 WHERE userid = ?", (worker,))
    await db.payout_status_updater(callback.from_user.id)
    await callback.message.edit_text("""<b><i>🤑 Приветствую тебя, Админ!</i></b>""", parse_mode="HTML",
                                     reply_markup=admin_panel_key(0))
    await callback.answer("Процесс выплат успешно завершен", show_alert=True)

