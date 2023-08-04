"""
"""
from asyncio.log import logger
from json.decoder import JSONDecodeError
from glob import glob
from pydantic import ValidationError, parse_file_as
from code.backends.memory import MemoryBackend
from code.event import GameEvent

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger("match.py: ")


class Match:
    def __init__(self, path, backend=None, testing=False):
        self.game_path = path
        self.game_files = glob(self.game_path)
        self.game_files.sort()
        self.test_mode = testing
        if backend is None:
            self.backend = MemoryBackend()
        else:
            # get backend from config
            pass
        self.match=None
        self.teams=[]
        # self.players=[]

    def load_game(self):
        for game_file in self.game_files:
            try:
                event = parse_file_as(GameEvent, game_file)
                self.event_handler(event)
                if self.test_mode:
                    self.backend.add_event(event)
            except ValidationError as exc:
                logger.error(f"ValidationError: on file {game_file}")

            except JSONDecodeError as exc:
                logger.error(f"JSONDecodeError: on file {game_file}")

            except Exception as exc:
                logger.error(exc)
                logger.error(f"Unexpected error: on file {game_file}")

    def event_handler(self, event):
        if event.type == "MATCH_START":
            self.match = event.matchID
            self.fixture = event.payload.fixture
            self.teams = event.payload.teams

        elif event.type == "MINION_KILL":
            self.update_player(event.payload.playerID, meta={
                "minions": 1,
                "gold": event.payload.goldGranted,
            })

        elif event.type == "PLAYER_KILL":
            self.update_player(event.payload.killerID, meta={
                "kills": 1,
                "gold": event.payload.goldGranted
            })
            for each in event.payload.assistants:
                self.update_player(each, meta={
                    "assists": 1,
                    "gold": event.payload.assistGold
                })
            self.update_player(event.payload.victimID, meta={
                "deaths": 1,
                "alive": False
            })

        elif event.type == "PLAYER_REVIVE":
            self.update_player(event.payload.playerID, meta={
                "alive": True
            })
        
        elif event.type == "DRAGON_KILL":
            self.update_player(event.payload.killerID, meta={
                "gold": event.payload.goldGranted
            })
            team = self.get_team_from_player(event.payload.killerID)
            self.update_team(team.teamID, meta={
                "dragons": 1
            })

        elif event.type == "NASHOR_KILL":
            team = self.get_team_from_player(event.payload.killerID)
            for player in team.players:
                self.update_player(player.playerID, meta={
                    "gold": event.payload.teamGoldGranted
                })
            self.update_team(team.teamID, meta={
                "nashors": 1
            })
        
        elif event.type == "TURRET_DESTROY":
            if event.payload.killerID:
                team = self.get_team_from_player(event.payload.killerID)
                self.update_player(event.payload.killerID, meta={
                    "gold": event.payload.playerGoldGranted
                })
                for player in team.players:
                    self.update_player(player.playerID, meta={
                        "gold": event.payload.teamGoldGranted
                    })

            self.update_team(event.payload.killerTeamID, meta={
                "towers": 1
            })

        elif event.type == "MATCH_END":
            self.match = None
            logger.info("############ Match ended ############")
            logger.info(f"The winner team is: {event.payload.winningTeamID}\n")
            for team in self.teams:
                logger.info("################ TEAM INFO ###################")
                logger.info(f"Team {team.teamID}")
                logger.info(f"Dragon kills: {team.dragonKills}")
                logger.info(f"Nashor kills: {team.nashorKills}")
                logger.info(f"Tower kills: {team.towersDestroyed}\n")
                logger.info(f"*******## Players: ##********")
                for player in team.players:
                    logger.info(f"{player}")
                logger.info("\n\n")

        else:
            logger.error(f"Unknown event type: {event.type}")
        # self.backend.add_event(event) no need to persist events in memory
    
    def update_player(self, player_id, meta):
        player=self.get_player(player_id)
        if player:
            player.update(meta)
        # print("Player score updated:", player)

    def update_team(self, team_id, meta):
        team = self.get_team(team_id)
        if team:
            team.update(meta)

        # print("Team score updated:", team)


    def get_player(self, player_id):
        for team in self.teams:
            player = team.get_player(player_id)
            if player:
                return player
        return None
    
    def get_team(self, team_id):
        for team in self.teams:
            if team.teamID == team_id:
                return team
        return None

    def get_team_from_player(self, player_id):
        for team in self.teams:
            for player in team.players:
                if player.playerID == player_id:
                    return team
        return None

