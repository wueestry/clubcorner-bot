class Team:
    def __init__(self, name, league) -> None:
        self.name = name
        self.league = league


class Game:
    def __init__(self, id: str, team_home: Team = None, team_away: Team = None, date: str = "") -> None:
        self.home_team = team_home
        self.away_team = team_away
        self.game_id = id
        self.date = date

    def __eq__(self, other) -> bool:
        return self.game_id == other.game_id

    def get_string(self) -> str:
        return f"{self.date}\n{self.home_team.name} ( {self.home_team.league} ) vs {self.away_team.name} ( {self.away_team.league} )\n"
