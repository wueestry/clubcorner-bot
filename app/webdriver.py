import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import List
from game import Game, Team


class Webdriver:
    def __init__(self) -> None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_path = r"/usr/local/bin/chromedriver"
        # self.driver = webdriver.Remote("http://localhost:4444/wd/hub", options=chrome_options)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(3)

    def LogIn(self) -> bool:
        try:
            self.driver.get("https://www.clubcorner.ch/users/sign_in")
        except:
            print("Internet connection not working or clubcorner not available")
            return False

        self.driver.implicitly_wait(3)

        if self.driver.title == "Anmelden - clubcorner.ch":

            with open("/app/keys.json", "r") as keys_file:
                k = json.load(keys_file)
                key = k["clubcorner"]
                email = k["email"]
            
            username = self.driver.find_element(By.ID, "user_email")
            username.clear()
            username.send_keys(email)

            self.driver.implicitly_wait(0.5)
            password = self.driver.find_element(By.ID, "user_password")
            password.clear()
            password.send_keys(key)

            self.driver.find_element(By.NAME, "commit").click()

            return True

        elif self.driver.title == "Herzlich willkommen bei clubcorner.ch - clubcorner.ch":

            return True

        else:
            print("Clubcorner not available")
            return False

    def is_empty(self) -> bool:
        if len(self.driver.find_elements(By.CLASS_NAME, "no-data")) > 0:
            return True
        else:
            return False

    def wait(self, time: int) -> None:
        self.driver.implicitly_wait(time)

    def read_page_data(self) -> List[Game]:
        game_id = self.driver.find_elements(By.XPATH, "//span[@class= 'label label-info']")
        self.driver.implicitly_wait(0.1)
        teams = self.driver.find_elements(By.CLASS_NAME, "title")
        self.driver.implicitly_wait(0.1)
        leagues = self.driver.find_elements(By.CLASS_NAME, "subtitle")
        self.driver.implicitly_wait(0.1)
        time = self.driver.find_elements(
            By.XPATH, "//table[@class='listing table table-striped table-bordered']//td[2]"
        )

        games = list()
        for i in range(0, len(teams), 2):
            team_home = Team(teams[i].text, leagues[i].text)
            team_away = Team(teams[i + 1].text, leagues[i + 1].text)
            game = Game(game_id[i // 2].text, team_home, team_away, time[i // 2].text)
            games.append(game)

        return games

    def change_to_site(self, url: str) -> None:
        self.driver.get(url)

    def get_page_has_data(self, url: str) -> bool:
        self.change_to_site(url)
        self.driver.implicitly_wait(0.5)
        return True if not self.is_empty() else False

    def get_additional_page_data(self) -> List[Game]:
        page = 2
        games = list()
        while self.get_page_has_data(
            f"https://www.clubcorner.ch/schiedsrichter/spiele_ohne_einsaetze?page={page}"
        ):
            games += self.read_page_data()
            page += 1

        return games

    def get_data(self) -> List[Game]:
        if self.is_empty():
            return []

        games = self.read_page_data()
        games += self.get_additional_page_data()

        return games
