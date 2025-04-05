import aiosqlite
import os
import string
import random
from settings import settings

DB_PATH = settings.bots.db_path

class DataBase:
    def __init__(self, db_name=DB_PATH):
        self.db_name = db_name


    async def connect(self):
        """Устанавливает соединение с базой данных"""
        self.connection = await aiosqlite.connect(self.db_name)
        self.cursor = await self.connection.cursor()

    async def close(self):
        """Закрывает соединение с базой данных"""
        await self.cursor.close()
        await self.connection.close()

    async def change(self, query, values=[]):
        """Изменение базы данных (Insert, Update, Alert)"""
        await self.cursor.execute(query, values)
        await self.connection.commit()

    async def get(self, query, values=[], fetchone=True):
        """Получение данных из базы данных"""
        await self.cursor.execute(query, values)
        if fetchone:
            return await self.cursor.fetchone()
        else:
            return await self.cursor.fetchall()

        """Добавляет нового воркера в базу данных"""

    async def addLame(self, userid, username, login, passwrd):
        await self.connect()
        await self.change("INSERT INTO lames (userid, username, login, passwrd) VALUES (?,?,?,?)",
                          (userid, username, login, passwrd))
        await self.close()
        return

        """Добавляет воркера вступившего по реф ссылке в базу данных """

    async def addLead(self, userid, username, urlRef, sber, vtb, tin, alfa, count_of_accs):
        await self.connect()
        user = await self.get("SELECT * from leads WHERE userid = ?", [userid, ])
        if user is None:
            await self.change(
                "INSERT INTO leads(userid, username, urlRef, sber, vtb, tin, alfa, count_of_accs) VALUES (?,?,?,?,?,?,?,?)",
                (userid, username, urlRef, sber, vtb, tin, alfa, count_of_accs))
        await self.close()
        return

    async def count_of_leads_updater(self, userid, referral_code):
        await self.connect()
        user = await self.get("SELECT userid from leads WHERE userid = ?", [userid, ])
        if user is None:
            await self.change("UPDATE users SET count_of_lead = count_of_lead + 1 WHERE urlBot = ?", (referral_code,))
            await self.change("UPDATE users SET leads_balance = leads_balance + 4 WHERE urlBot = ?", (referral_code,))
            await self.change(f"UPDATE users SET balance = balance + 4 WHERE urlBot = ?", (referral_code,))

        await self.close()
        return

        """ЗАПРОСЫ К ТАБЛИЦАМ СВЯЗАННЫМ С ВОРКЕРАМИ"""

        """Добавляет нового воркера в базу данных"""

    async def addUser(self, userid, username, balance, wallet, methode, totalCountAcc, moderationCountAcc,
                      payedCountAcc, count_of_lead, views_balance, leads_balance):
        await self.connect()
        user = await self.get("SELECT * from users WHERE userid = ?", [userid, ])
        if user is None:
            urlRef = generate_ref_code()
            LeadurlRef = generate_ref_code()
            await self.change(
                "INSERT INTO users (userid, username, balance, wallet, methode, totalCountAcc, moderationCountAcc, payedCountAcc, urlRef, urlBot, count_of_lead, views_balance, leads_balance) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (userid, username, balance, wallet, methode, totalCountAcc, moderationCountAcc, payedCountAcc, urlRef,
                 LeadurlRef, count_of_lead, views_balance, leads_balance))
        await self.close()
        return

        """Добавляет воркера вступившего по реф ссылке в базу данных """

    async def addRefUser(self, userid, username, urlRef):
        await self.connect()
        user = await self.get("SELECT * from referrals WHERE userid = ?", [userid, ])
        if user is None:
            await self.change("INSERT INTO referrals (userid, username, urlRef) VALUES (?,?,?)",
                              (userid, username, urlRef))
        await self.close()
        return

        """Добавляет новый аккаунт ТТ в базу данных"""

    async def addTtAccount(self, userid, username, tt_url, total_count_videos, total_count_views, total_count_subs,
                           total_count_likes):
        await self.connect()
        tt_url_from_db = await self.get("SELECT tt_url from accounts WHERE userid = ? and tt_url = ?",
                                        [userid, tt_url, ])
        print(tt_url_from_db)
        if tt_url_from_db is None:
            await self.change(
                "INSERT INTO accounts (userid, username, tt_url, total_count_videos, total_count_views, total_count_subs, total_count_likes) VALUES (?,?,?,?,?,?,?)",
                (userid, username, tt_url, total_count_videos, total_count_views, total_count_subs, total_count_likes))
            await self.change(f"UPDATE users SET totalCountAcc = totalCountAcc + 1 WHERE userid = ?", (userid,))
            await self.change(f"UPDATE users SET moderationCountAcc = moderationCountAcc + 1 WHERE userid = ?",
                              (userid,))
            await self.change(
                "INSERT INTO moderationAccounts (userid, tt_url) VALUES (?,?)", (userid, tt_url))

            await self.close()
            return 1
        else:
            await self.close()
            return 0

    """Добавляет выплаченный аккаунт ТТ в базу данных"""

    async def addModerationTtAccount(self, userid, tt_url):
        await self.connect()
        await self.change(
            "INSERT INTO moderationAccounts (userid, tt_url) VALUES (?,?)", (userid, tt_url))
        await self.close()
        return

    """Добавляет выплаченный аккаунт ТТ в базу данных"""

    async def addPayedTtAccount(self, userid, tt_url):
        await self.connect()
        await self.change(
            "INSERT INTO payedAccounts (userid, tt_url) VALUES (?,?)", (userid, tt_url))
        await self.close()
        return

    """Забаненный пользователь в БД"""

    async def banWorker(self, userid):
        await self.connect()
        user = await self.get("SELECT userid from bannedUsers WHERE userid = ?",
                              [userid, ])
        if user is None:
            await self.change(
                "INSERT INTO bannedUsers (userid) VALUES (?)", (userid,))
        await self.close()
        return

    async def prfilie_info_selector(self, userid):
        await self.connect()
        result = await self.get("SELECT * from users WHERE userid = ?", [userid, ])
        await self.close()
        return result

    async def wallet_updater(self, userid, wallet):
        await self.connect()
        await self.change(f"UPDATE users SET wallet = \'{wallet}\' WHERE userid = ?", (userid,))
        await self.close()

    async def wallet_selector(self, userid):
        await self.connect()
        result = await self.get("SELECT wallet from users WHERE userid = ?", [userid, ])
        await self.close()
        return result[0]

    async def methode_switcher(self, userid):
        await self.connect()
        current = await self.get("SELECT methode from users WHERE userid = ?", [userid, ])
        if current[0] == 0:
            await self.change(f"UPDATE users SET methode = 1 WHERE userid = ?", (userid,))
        else:
            await self.change(f"UPDATE users SET methode = 0 WHERE userid = ?", (userid,))
        await self.close()

    async def methode_picker(self, userid):
        await self.connect()
        result = await self.get("SELECT methode from users WHERE userid = ?", [userid, ])
        await self.close()
        return result[0]

    async def refUrl_picker(self, userid):
        await self.connect()
        result = await self.get("SELECT urlRef from users WHERE userid = ?", [userid, ])
        await self.close()
        return result[0]

    async def get_referral_count(self, userid):
        await self.connect()
        refUrl = await self.get("SELECT urlRef from users WHERE userid = ?", [userid, ])
        count = await self.get("SELECT count(id) FROM referrals WHERE urlRef = ?", [str(refUrl[0]), ])
        await self.close()
        return count[0]

    async def totalCountAcc_picker(self, userid):
        await self.connect()
        result = await self.get("SELECT totalCountAcc from users WHERE userid = ?", [userid, ])
        await self.close()
        return result[0]

    async def moderatedAccUser_picker(self):
        await self.connect()
        result = await self.get("SELECT userid from users WHERE moderationCountAcc > 0", fetchone=False)
        await self.close()
        return result

    async def moderatedAccList_picker(self, userid):
        await self.connect()
        result = await self.get("SELECT tt_url from accounts WHERE userid = ?", [userid, ], fetchone=False)
        await self.close()
        return result

    async def count_of_views_updater(self, tt_url, count_of_views: int):
        await self.connect()
        await self.change(
            f"UPDATE accounts SET total_count_views = total_count_views + {count_of_views}  WHERE tt_url = ?",
            (tt_url,))
        await self.close()

    async def checker_balance_updater(self, userid, balance: float):
        await self.connect()
        await self.change(f"UPDATE users SET views_balance = views_balance + {balance} WHERE userid = ?", (userid,))
        await self.change(f"UPDATE users SET balance = balance + {balance} WHERE userid = ?", (userid,))
        await self.close()

    async def payout_worker_picker(self):
        await self.connect()
        result = await self.get("SELECT userid from users WHERE balance > 0", fetchone=False)
        await self.close()
        return result

    async def payout_balance_views_picker(self, userid):
        await self.connect()
        result = await self.get("SELECT views_balance from users WHERE userid = ?", (userid,))
        await self.close()
        print(result[0])
        return result[0]

    async def payout_balance_leads_picker(self, userid):
        await self.connect()
        result = await self.get("SELECT leads_balance from users WHERE userid = ?", (userid,))
        await self.close()
        print(result[0])
        return result[0]

    async def payout_total_balance_picker(self):
        await self.connect()
        result = await self.get("SELECT balance from users WHERE balance > 0", fetchone=False)
        await self.close()
        total_balance_list = [t[0] for t in result]
        new_balance = 0.0
        for balance in total_balance_list:
            new_balance += balance
        return new_balance

    async def payout_count_worker_picker(self):
        await self.connect()
        result = await self.get("SELECT COUNT(*) from users WHERE balance > 0")
        await self.close()
        return result

    async def payed_accounts_updater(self, userid, add_count: int):
        await self.connect()
        await self.change(f"UPDATE users SET payedCountAcc = payedCountAcc + {add_count} WHERE userid = ?", (userid,))
        await self.close()

    async def moderation_account_zero_updater(self, userid):
        await self.connect()
        await self.change(f"UPDATE users SET moderationCountAcc = 0 WHERE userid = ?", (userid,))
        await self.close()

    async def moderation_list_deleter(self, userid):
        await self.connect()
        await self.change(f"DELETE FROM accounts WHERE userid = ?", [userid, ])
        await self.close()

    """ADMIN PANEL"""

    async def user_picker(self, userid):
        await self.connect()
        result = await self.get(
            "SELECT username, balance, totalCountAcc, moderationCountAcc, payedCountAcc from users WHERE userid = ?",
            [userid, ])
        await self.close()
        return result

    async def moderationCountAcc_picker(self, userid):
        await self.connect()
        result = await self.get("SELECT moderationCountAcc from users WHERE userid = ?", [userid, ])
        await self.close()
        return result[0]

    async def balance_updater(self, userid, amount: float):
        await self.connect()
        await self.change(f"UPDATE users SET balance = balance - {amount} WHERE userid = ?", (userid,))
        await self.close()

    """Добавляет админа при первом сообщ /admin"""

    async def addAdmin(self, userid, checker_status, payout_status, last_check_date):
        await self.connect()
        user = await self.get("SELECT userid from admin WHERE userid = ?", [userid, ])
        print(user)
        if user is None:
            await self.change(
                "INSERT INTO admin (userid, checker_status, payout_status, last_check_date) VALUES (?,?,?,?)",
                (userid, checker_status, payout_status, last_check_date))
        await self.close()
        return

    async def checker_status_picker(self, userid):
        await self.connect()
        result = await self.get("SELECT checker_status from admin WHERE userid = ?", [userid, ])
        await self.close()
        return result[0]

    async def payout_status_picker(self, userid):
        await self.connect()
        result = await self.get("SELECT payout_status from admin WHERE userid = ?", [userid, ])
        await self.close()
        return result[0]

    async def last_check_date_picker(self, userid):
        await self.connect()
        result = await self.get("SELECT last_check_date from admin WHERE userid = ?", [userid, ])
        await self.close()
        return result[0]

    async def checker_status_updater(self, userid):
        await self.connect()
        current = await self.get("SELECT checker_status from admin WHERE userid = ?", [userid, ])
        if current[0] == 0:
            await self.change(f"UPDATE admin SET checker_status = 1 WHERE userid = ?", (userid,))
        else:
            await self.change(f"UPDATE admin SET checker_status = 0 WHERE userid = ?", (userid,))
        await self.close()

    async def payout_status_updater(self, userid):
        await self.connect()
        current = await self.get("SELECT payout_status from admin WHERE userid = ?", [userid, ])
        if current[0] == 0:
            await self.change(f"UPDATE admin SET payout_status = 1 WHERE userid = ?", (userid,))
        else:
            await self.change(f"UPDATE admin SET payout_status = 0 WHERE userid = ?", (userid,))
        await self.close()

    async def last_check_date_updater(self, userid, time_now: str):
        await self.connect()
        await self.change(f"UPDATE admin SET last_check_date = \'{time_now}\' WHERE userid = ?", (userid,))
        await self.close()


def generate_ref_code(length=8):
    characters = string.ascii_letters + string.digits
    referral_code = "".join(random.choice(characters) for _ in range(length))
    return referral_code
