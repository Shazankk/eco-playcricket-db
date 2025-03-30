from fastapi import APIRouter, HTTPException, File, UploadFile, Form, Body, Response
from fastapi.responses import JSONResponse
import io
import logging
from typing import Dict, Any, List, Optional
from PIL import Image
from utils.r2_storage import upload_image_to_r2
from models.faqs_list import FAQsList
from models.teams_list import TeamsList
from models.sponsors_list import SponsorsList
from models.fixtures_and_results import FixturesResults
from models.players_list import PlayersList
from models.player_profile import PlayersProfile
from database.connection import refresh_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = APIRouter()

# --- Helper functions ---

def add_cache_headers(response):
    """Add cache prevention headers to response"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# --- Read endpoints ---

@router.get("/faqs")
async def get_faqs():
    """Get all FAQs."""
    try:
        logger.info("Processing request for FAQs")
        data = await FAQsList.get_all_faqs()
        response = JSONResponse(content=data)
        return add_cache_headers(response)
    except Exception as e:
        logger.error(f"Error fetching FAQs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/teams")
async def get_teams():
    """Get all teams."""
    try:
        logger.info("Processing request for teams")
        data = await TeamsList.get_all_teams()
        response = JSONResponse(content=data)
        return add_cache_headers(response)
    except Exception as e:
        logger.error(f"Error fetching teams: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sponsors")
async def get_sponsors():
    """Get all sponsors."""
    try:
        logger.info("Processing request for sponsors")
        data = await SponsorsList.get_all_sponsors()
        response = JSONResponse(content=data)
        return add_cache_headers(response)
    except Exception as e:
        logger.error(f"Error fetching sponsors: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/fixtures-and-results")
async def get_fixtures():
    """Get all fixtures and results."""
    try:
        logger.info("Processing request for fixtures and results")
        data = await FixturesResults.get_all_fixtures()
        response = JSONResponse(content=data)
        return add_cache_headers(response)
    except Exception as e:
        logger.error(f"Error fetching fixtures and results: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/player-stats")
async def get_player_stats():
    """Get all player statistics."""
    try:
        logger.info("Processing request for player statistics")
        # Force refresh connection to ensure fresh data using sync()
        refresh_db_connection()
        data = await PlayersList.get_all_player_stats()
        response = JSONResponse(content=data)
        return add_cache_headers(response)
    except Exception as e:
        logger.error(f"Error fetching player statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/player-profile")
async def get_player_profile():
    """Get all player profiles."""
    try:
        logger.info("Processing request for player profiles")
        # Force refresh connection to ensure fresh data using sync()
        refresh_db_connection()
        data = await PlayersProfile.get_all_player_profile()
        response = JSONResponse(content=data)
        return add_cache_headers(response)
    except Exception as e:
        logger.error(f"Error fetching player profiles: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Player profile management endpoints ---

@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    member_id: str = Form(None),
    player_name: str = Form(None)
):
    """Handle player picture uploads."""
    try:
        logger.info(f"Received upload request for member_id={member_id}, player_name={player_name}")
        
        # Read the picture
        file_content = await file.read()
        
        # Determine player identifier
        player_identifier = "unknown"
        if member_id and member_id.strip():
            player_identifier = member_id
        elif player_name and player_name.strip():
            player_identifier = player_name.replace(" ", "_").lower()
        
        logger.info(f"Using player identifier: {player_identifier}")
        
        # Prepare image processing
        image = Image.open(io.BytesIO(file_content))
        image = image.resize((800, int(800 * image.height / image.width)))
        
        # Try AVIF format first, fall back to JPEG if not supported
        output = io.BytesIO()
        content_type = "image/jpeg"
        file_ext = "jpg"
        
        try:
            # Try AVIF first (better compression)
            logger.info("Attempting AVIF conversion")
            image.save(output, format="AVIF", quality=80)
            content_type = "image/avif"
            file_ext = "avif"
            logger.info("AVIF conversion successful")
        except (ValueError, IOError, KeyError) as e:
            # AVIF not supported, fall back to JPEG
            logger.info(f"AVIF not supported ({str(e)}), falling back to JPEG")
            output = io.BytesIO()
            image.save(output, format="JPEG", quality=85, optimize=True)
        
        compressed_image = output.getvalue()
        
        # Prepare file path with appropriate extension
        file_name = f"player_{player_identifier}.{file_ext}"
        file_path = f"players/{file_name}"
        
        # Upload to cloud storage
        image_url = upload_image_to_r2(
            compressed_image,
            file_path,
            content_type
        )
        
        logger.info(f"Image uploaded successfully: {image_url}")
        
        # Return direct response with no wrapping but add cache headers
        response = JSONResponse(content={
            "imageUrl": image_url,
            "fileName": file_name,
            "playerIdentifier": player_identifier,
            "format": file_ext.upper()
        })
        return add_cache_headers(response)
        
    except ValueError as e:
        logger.warning(f"Value error during upload: {e}")
        if "already exists in R2 storage" in str(e):
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Image upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")

@router.post("/submit")
async def submit_player_data(player_data: Dict[str, Any] = Body(...)):
    """Handle new player profile information submission."""
    try:
        logger.info("Received player data submission")
        
        # Validate required fields
        required_fields = [
            "member_id", "player_name", "nationality", "role",
            "birth_date", "batting_style", "bowling_hand", 
            "bowling_style", "debut_year", "image_path"
        ]
        
        missing_fields = [field for field in required_fields if field not in player_data or not player_data[field]]
        
        if missing_fields:
            logger.warning(f"Missing required fields: {missing_fields}")
            raise HTTPException(
                status_code=400,
                detail=f"Missing required fields: {', '.join(missing_fields)}"
            )
        
        # Clean up the data
        formatted_data = {
            "member_id": str(player_data["member_id"]),
            "player_name": player_data["player_name"],
            "birth_date": player_data["birth_date"],
            "nationality": player_data["nationality"],
            "role": player_data["role"],
            "batting_style": player_data["batting_style"],
            "bowling_hand": player_data["bowling_hand"],
            "bowling_style": player_data["bowling_style"],
            "debut_year": int(player_data["debut_year"]),
            "image_path": player_data["image_path"]
        }
        
        # Force refresh connection before inserting to ensure we're working with the latest data
        refresh_db_connection()
        
        # Save player profile
        result = await PlayersProfile.insert_player_profile(formatted_data)
        
        logger.info(f"Player profile saved: {formatted_data['player_name']} (ID: {formatted_data['member_id']})")
        
        # Return direct result with no wrapping but add cache headers
        response_content = {
            "member_id": formatted_data["member_id"],
            "player_name": formatted_data["player_name"],
            "message": result.get("message", "Player profile saved successfully!")
        }
        response = JSONResponse(content=response_content)
        return add_cache_headers(response)
        
    except ValueError as e:
        logger.warning(f"Value error during submission: {e}")
        if "already exists in the database" in str(e):
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Player submission error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save player data: {str(e)}")

# --- Debug endpoints ---

@router.get("/debug/player/{member_id}")
async def check_player_exists(member_id: str):
    """Debug endpoint to check if a player exists in the database."""
    try:
        logger.info(f"Debug request to check player existence: {member_id}")
        # Force database sync to ensure fresh data
        refresh_db_connection()
        player = await PlayersProfile.get_player_profile(member_id)
        
        if player:
            response_data = {
                "exists": True,
                "player": player
            }
            status_code = 200
        else:
            response_data = {
                "exists": False,
                "message": f"No player found with member_id: {member_id}"
            }
            status_code = 404
            
        response = JSONResponse(content=response_data, status_code=status_code)
        return add_cache_headers(response)
        
    except Exception as e:
        logger.error(f"Error checking player existence: {e}")
        raise HTTPException(status_code=500, detail=str(e))