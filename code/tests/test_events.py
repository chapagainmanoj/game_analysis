from code.event import GameEvent

def test_events(match):
    """
    Test the events.
    """
    assert len(match.backend.events) == 0
    match.load_game()
    assert len(match.backend.events) == len(match.game_files) -1 # one file is unknown
    assert len(match.teams) == 2

    for event in match.backend.events:
        if event.type == "MATCH_START":
            assert event.matchID
            assert event.payload.fixture
            assert event.payload.teams

        elif event.type == "MATCH_END":
            assert event.matchID
            assert event.payload.winningTeamID

        else:
            pass
