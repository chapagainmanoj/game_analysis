import pytest
from code.match import Match

DATA_PATH="./samples/*"

@pytest.fixture
def match():
    return Match(path=DATA_PATH, testing=True)