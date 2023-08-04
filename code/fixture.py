from datetime import datetime
from pydantic import BaseModel
from typing import List

class Fixture(BaseModel):
    startTime: datetime
    title: str
    seriesCurrent: int
    seriesMax: int
    seriesType: str


class Players(BaseModel):
    playerID: str
    totalGold: int
    currentGold: int
    alive: bool
    kills: int
    deaths: int
    assists: int
    minions: int
    name: str

    def update_gold(self, gold: int):
        self.currentGold += gold
    
    def update_kills(self, kills: int = 1):
        self.kills += kills
    
    def update_deaths(self, deaths: int = 1):
        self.deaths += deaths
    
    def update_assists(self, assists: int = 1):
        self.assists += assists

    def update_minions(self, minions: int = 1):
        self.minions += minions

    def update_alive(self, alive: bool = True):
        self.alive = alive

    def update(self, meta: dict):
        self.update_minions(meta.get("minions", 0))
        self.update_gold(meta.get("gold", 0))
        self.update_deaths(meta.get("deaths", 0))
        self.update_assists(meta.get("assists", 0))
        self.update_kills(meta.get("kills", 0))
        self.update_alive(meta.get("alive", True))



class Team(BaseModel):
    teamID: str
    players: List[Players]
    dragonKills: int
    nashorKills: int
    towersDestroyed: int

    def update_dragon_kills(self, dragons: int = 1):
        self.dragonKills += dragons
    
    def update_nashor_kills(self, nashors: int = 1):
        self.nashorKills += nashors

    def update_tower_destroyed(self, towers: int = 1):
        self.towersDestroyed += towers

    def get_player(self, player_id: str):
        for player in self.players:
            if player.playerID == player_id:
                return player
        return None
        
    def update(self, meta: dict):
        self.update_dragon_kills(meta.get("dragons", 0))
        self.update_nashor_kills(meta.get("nashors", 0))
        self.update_tower_destroyed(meta.get("towers", 0))