from typing import List

from game import Game
from telegram_bot import Telegram_Bot
from webdriver import Webdriver

if __name__ == "__main__":
    previous_games: List[Game] = []
    with open("/app/previous_games.txt","r") as file:
        for line in file:
            line = line.replace("\n","")
            previous_games.append(Game(line))
    driver = Webdriver()
    bot = Telegram_Bot()
    print("running clubcorner bot")
    print(f"previous games:{[game.game_id for game in previous_games]}")

    if driver.LogIn():
        driver.change_to_site("https://www.clubcorner.ch/schiedsrichter/spiele_ohne_einsaetze")
        driver.wait(1)

        games = driver.get_data()
        print(f"games:{[game.game_id for game in games]}")

        new_games = [game for game in games if game not in previous_games]
        print(f"new games:{[game.game_id for game in new_games]}")


        bot.send_games(new_games)

        previous_games = games

        with open("/app/previous_games.txt", "w") as file:
            for game in previous_games:
                file.write(f"{game.game_id}\n")
        print("Finished")