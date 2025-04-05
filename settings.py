from environs import Env
from dataclasses import dataclass

# Скрипт имортирует значение токена из текстового файла input и подключает его в диспетчер


@dataclass
class Bots:
    bot_work_token: str
    bot_fish_token: str
    crpt_token: str
    admin_id: int
    gorup_id: int
    db_path: str

@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_work_token=env.str('WORK_TOKEN'),
            bot_fish_token=env.str('FISH_TOKEN'),
            admin_id=env.int('ADMIN_ID'),
            gorup_id=env.int('GROUP_ID'),
            crpt_token=env.str('CRPT_BOT_TOKEN'),
            db_path = env.str('DB_PATH')
        )
    )


settings = get_settings('input.txt')
