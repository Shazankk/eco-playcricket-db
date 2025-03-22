from fastapi import APIRouter, HTTPException
from models.faqs_list import FAQsList
from models.teams_list import TeamsList
from models.sponsors_list import SponsorsList
from models.fixtures_and_results import FixturesResults
from models.players_list import PlayersList
from models.player_profile import PlayersProfile

router = APIRouter()

@router.get("/faqs")
async def get_faqs():
    try:
        return await FAQsList.get_all_faqs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/teams")
async def get_teams():
    try:
        return await TeamsList.get_all_teams()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sponsors")
async def get_sponsors():
    try:
        return await SponsorsList.get_all_sponsors()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/fixtures-and-results")
async def get_fixtures():
    try:
        return await FixturesResults.get_all_fixtures()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/player-stats")
async def get_player_stats():
    try:
        return await PlayersList.get_all_player_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/player-profile")
async def get_player_profile():
    try:
        return await PlayersProfile.get_all_player_profile()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
