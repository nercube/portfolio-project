
import pytest
from datetime import date
import crud
from database import SessionLocal


@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    yield session
    session.close()


def test_get_player(db_session):
    player = crud.get_player(db_session, player_id=1001)

    assert player is not None
    assert player.player_id == 1001



def test_get_players_by_name(db_session):
    players = crud.get_players(
        db_session,
        first_name="Bryce",
        last_name="Young",
    )

    assert len(players) == 1
    assert players[0].player_id == 2009



def test_get_players_by_date(db_session):
    players = crud.get_players(
        db_session,
        skip=0,
        limit=10000,
        min_last_changed_date=date(2024, 4, 1),
    )

    assert len(players) == 1018
    assert all(
        player.last_changed_date >= date(2024, 4, 1)
        for player in players
    )

def test_get_players_pagination(db_session):
    first_page = crud.get_players(db_session, skip=0, limit=5)
    second_page = crud.get_players(db_session, skip=5, limit=5)

    assert len(first_page) == 5
    assert len(second_page) == 5

    first_page_ids = {player.player_id for player in first_page}
    second_page_ids = {player.player_id for player in second_page}

    assert first_page_ids.isdisjoint(second_page_ids)