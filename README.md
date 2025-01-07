# CavsDatabase

This project is designed to fetch and store cricket-related data from the Play-Cricket API into a SQLite database. The project includes various scripts to fetch data for competition teams, fixtures, players, result summaries, and teams.

## Project Structure

CavsDatabase/ 
├── .env.example 
├── .gitignore 
├── .venv/ 
├── main.py 
├── routes/
│ ├── competition_teams.py 
│ ├── fixtures.py 
│ ├── initdb.py 
│ ├── match_details.py 
│ ├── players.py 
│ ├── result_summary.py 
│ └── teams.py 
└── cavsdatabase.db

### Files and Folders

#### `.env.example`

This file contains example environment variables required for the project. Copy this file to `.env` and fill in the appropriate values.

API_TOKEN=your_api_token 
SITE_ID=your_site_id 
LEAGUE_ID=your_league_id 
COMPETITION_NAME=your_competition_name 
COMPETITION_TYPE=your_competition_type 
MATCH_TYPE=your_match_type 
INCLUDE_EVERYONE=yes_or_no 
INCLUDE_HISTORIC=yes_or_no 
INCLUDE_UNPUBLISHED=yes_or_no

#### `.gitignore`

This file specifies the files and directories that should be ignored by Git. It includes the following entries:

.env 
.venv/ 
.vscode/ 
pycache/ 
*.db

### `.venv/`

This directory contains the virtual environment for the project. It is ignored by Git.

#### `main.py`

This is the main script that orchestrates the fetching and storing of data. It imports functions from the `routes` module and executes them in sequence, logging the progress and handling errors.

#### `routes/`

This directory contains the individual scripts for fetching and storing different types of data. Each script is responsible for a specific type of data and includes the necessary SQL queries to create the corresponding tables in the SQLite database.

- `competition_teams.py`: Fetches and stores competition teams data.
- `fixtures.py`: Fetches and stores fixtures data.
- `initdb.py`: Contains the SQL queries to initialize the database tables.
- `match_details.py`: Fetches and stores match details data.
- `players.py`: Fetches and stores players data.
- `result_summary.py`: Fetches and stores result summary data.
- `teams.py`: Fetches and stores teams data.

#### `cavsdatabase.db`

This is the SQLite database file where the fetched data is stored. It is ignored by Git.

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/Shazankk/eco-playcricket-db.git
    cd CavsDatabase
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Copy the [.env.example](http://_vscodecontentref_/5) file to [.env](http://_vscodecontentref_/6) and fill in the appropriate values:
    ```bash
    cp .env.example .env
    ```

5. Run the [main.py](http://_vscodecontentref_/7) script:
    ```bash
    python main.py
    ```

## Usage

The [main.py](http://_vscodecontentref_/8) script will fetch data from the Play-Cricket API and store it in the SQLite database. The progress and any errors will be logged to the console.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.