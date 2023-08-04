"""
"""
from typing import Any, List, Optional, Type, TypeVar, Literal, Union
from pydantic import BaseModel, Field, validator
from code.core import BaseEntity
from code.fixture import Fixture, Team

class MatchStartPayload(BaseModel):
    fixture: Fixture
    teams: List[Team]

class DragonKillPayload(BaseModel):
    killerID: str
    dragonType: str
    goldGranted: int


class MatchEndPayload(BaseModel):
    winningTeamID: str


class PlayerKillPayload(BaseModel):
    killerID: Optional[str]
    victimID: str
    goldGranted: int
    assistants: List[str]
    assistGold: int


class MinionKillPayload(BaseModel):
    playerID: str
    goldGranted: int


class NashorKillPayload(BaseModel):
    killerID: str
    teamGoldGranted: int


class PlayerRevivePayload(BaseModel):
    playerID: str


class TurretDestroyPayload(BaseModel):
    killerID: Optional[str]
    killerTeamID: str
    turretTier: int
    turretLane: str
    playerGoldGranted: int
    teamGoldGranted: int


class UnknownPayload(BaseModel):
    playerID: str


PayloadType = TypeVar(
    "PayloadType",
    PlayerKillPayload,
    TurretDestroyPayload,
    MatchStartPayload,
    MatchEndPayload,
    DragonKillPayload,
    MinionKillPayload,
    NashorKillPayload,
    PlayerRevivePayload,
    UnknownPayload,
)


class GameEvent(BaseEntity):
    matchID: Optional[str]
    type: Literal[
        "MATCH_START",
        "MATCH_END",
        "DRAGON_KILL",
        "MINION_KILL",
        "PLAYER_KILL",
        "NASHOR_KILL",
        "PLAYER_REVIVE",
        "TURRET_DESTROY",
        "UNKNOWN",
    ]
    payload: PayloadType