from database.connection import get_db_connection
from typing import Dict, Any, List, Optional

class PlayersProfile:
    @staticmethod
    async def get_all_player_profile():
        """Get all player profiles"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM player_profile;")
            stats = cursor.fetchall()
            # Convert tuple results to dictionaries
            columns = [description[0] for description in cursor.description]
            result = [dict(zip(columns, row)) for row in stats]
            return result
        except Exception as e:
            print(f"Error fetching player profile: {e}")
            return []
    
    @staticmethod
    async def get_player_profile(member_id: str) -> Optional[Dict[str, Any]]:
        """Get a single player profile by member_id"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM player_profile WHERE member_id = ?", (member_id,))
            player = cursor.fetchone()
            
            if not player:
                return None
                
            # Convert tuple to dict
            columns = [description[0] for description in cursor.description]
            result = dict(zip(columns, player))
            return result
        except Exception as e:
            print(f"Error fetching player profile: {e}")
            return None

    @staticmethod
    async def insert_player_profile(player_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new player to our notebook"""
        try:
            print(f"Inserting player data: {player_data}")
            
            conn = get_db_connection(force_sync=True)
            cursor = conn.cursor()
            
            # Check if player already exists
            cursor.execute(
                "SELECT member_id, player_name FROM player_profile WHERE member_id = ?",
                (player_data["member_id"],)
            )
            existing_player = cursor.fetchone()
            
            if existing_player:
                # Get the player's name from results
                columns = ["member_id", "player_name"]
                existing_player_dict = dict(zip(columns, existing_player))
                existing_name = existing_player_dict["player_name"]
                
                print(f"Player with member_id {player_data['member_id']} ({existing_name}) already exists")
                raise ValueError(
                    f"Player \"{existing_name}\" (ID: {player_data['member_id']}) already exists in the database. "
                    "Please contact Shashank for resubmission of player information."
                )
            else:
                print(f"Creating new player record with member_id {player_data['member_id']}")
                
                # Add the new player
                cursor.execute(
                    """
                    INSERT INTO player_profile (
                        member_id, player_name, birth_date, nationality, role, 
                        batting_style, bowling_hand, bowling_style, debut_year, image_path
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        player_data["member_id"],
                        player_data["player_name"],
                        player_data["birth_date"],
                        player_data["nationality"],
                        player_data["role"],
                        player_data["batting_style"],
                        player_data["bowling_hand"],
                        player_data["bowling_style"],
                        player_data["debut_year"],
                        player_data["image_path"],
                    )
                )
                conn.commit()
                
                return {
                    "success": True,
                    "message": "Player profile created successfully",
                }
        except ValueError as error:
            # Pass along the special error
            raise
        except Exception as error:
            print(f"Database error: {error}")
            raise RuntimeError(f"Failed to save player data: {str(error)}")