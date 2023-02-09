import json
import telegram
from typing import List
from game import Game


class Telegram_Bot:
    def __init__(self) -> None:
        with open("/app/keys.json", "r") as keys_file:
            k = json.load(keys_file)
            self.token = k["telegram_token"]
            self.chat_id = k["telegram_chat_id"]

        self.bot = telegram.Bot(token=self.token)

    def send_message(self, message: str) -> None:
        if len(message) > 4096:
            for x in range(0, len(message) % 4096):
                self.bot.send_message(chat_id=self.chat_id, text=message[x : x + 4096])
        else:
            self.bot.send_message(chat_id=self.chat_id, text=message)

    def send_games(self, newGames: List[Game]) -> None:
        if not newGames:
            return

        n_games = len(newGames)
        msg = f"There {'is' if n_games == 1 else 'are'} {n_games} new game{'s' if not n_games == 1 else ''} available. \n"

        for game in newGames:
            msg += game.get_string()

        self.send_message(msg)
