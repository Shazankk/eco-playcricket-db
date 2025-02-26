-- DROP TABLE batting_stats;
-- DROP TABLE bowling_stats;
-- DROP TABLE clubs;
-- DROP TABLE competitions;
-- DROP TABLE fall_of_wickets;
-- DROP TABLE innings;
-- DROP TABLE leagues;
-- DROP TABLE match_players;
-- DROP TABLE match_points;
-- DROP TABLE match_result_types;
-- DROP TABLE matches;
-- DROP TABLE officials;
-- DROP TABLE players;
-- DROP TABLE result_summary;
-- DROP TABLE teams;

-- Leagues
CREATE TABLE
  leagues (league_id INTEGER PRIMARY KEY, name TEXT NOT NULL);

-- Competitions
CREATE TABLE
  competitions (
    competition_id INTEGER PRIMARY KEY,
    league_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL
  );

-- Clubs
CREATE TABLE
  clubs (club_id INTEGER PRIMARY KEY, name TEXT NOT NULL);

-- Teams
CREATE TABLE
  teams (
    team_id INTEGER PRIMARY KEY,
    club_id INTEGER NOT NULL,
    name TEXT NOT NULL
  );

-- Officials
CREATE TABLE
  officials (
    official_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL
  );

-- Players
CREATE TABLE
  players (member_id INTEGER PRIMARY KEY, name TEXT NOT NULL);

-- Match Result Types
-- DROP TABLE match_result_types;
CREATE TABLE
  match_result_types (
    result_type_id INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    team_id INTEGER
  );

  -- faqs
CREATE TABLE
  faqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

-- Matches
-- DROP TABLE matches;
CREATE TABLE
  matches (
    match_id INTEGER PRIMARY KEY,
    status TEXT NOT NULL,
    published TEXT,
    last_updated TEXT,
    league_id INTEGER NOT NULL,
    competition_id INTEGER NOT NULL,
    match_type TEXT NOT NULL,
    game_type TEXT NOT NULL,
    match_date TEXT NOT NULL,
    match_time TEXT NOT NULL,
    ground_name TEXT NOT NULL,
    ground_id INTEGER,
    home_team_id INTEGER NULL,
    away_team_id INTEGER NULL,
    umpire_1_id INTEGER,
    umpire_2_id INTEGER,
    referee_id INTEGER,
    scorer_1_id INTEGER,
    scorer_2_id INTEGER,
    toss_won_by_team_id INTEGER,
    batted_first INTEGER,
    result TEXT,
    result_description TEXT,
    result_applied_to TEXT,
    match_notes TEXT,
    no_of_overs INTEGER,
    no_of_innings INTEGER CHECK (no_of_innings > 0),
    no_of_days INTEGER CHECK (no_of_days > 0),
    no_of_players INTEGER CHECK (no_of_players > 0),
    no_of_reserves INTEGER CHECK (no_of_reserves >= 0)
  );

-- Match Points
CREATE TABLE
  match_points (
    match_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    game_points INTEGER NOT NULL DEFAULT 0,
    penalty_points INTEGER NOT NULL DEFAULT 0,
    bonus_points_batting INTEGER DEFAULT 0,
    bonus_points_bowling INTEGER DEFAULT 0,
    PRIMARY KEY (match_id, team_id)
  );

-- Match Players
CREATE TABLE
  match_players (
    match_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    is_captain INTEGER NOT NULL CHECK (is_captain IN (0, 1)),
    is_wicket_keeper INTEGER NOT NULL CHECK (is_wicket_keeper IN (0, 1)),
    position INTEGER CHECK (position > 0),
    PRIMARY KEY (match_id, team_id, player_id)
  );

-- Innings
CREATE TABLE
  innings (
    inning_id INTEGER PRIMARY KEY,
    match_id INTEGER NOT NULL,
    team_batting_id INTEGER NOT NULL,
    innings_number INTEGER NOT NULL CHECK (innings_number > 0),
    runs INTEGER DEFAULT 0,
    wickets INTEGER DEFAULT 0,
    overs REAL DEFAULT 0.0,
    declared INTEGER CHECK (declared IN (0, 1)),
    total_extras INTEGER DEFAULT 0
  );

-- Batting Statistics
CREATE TABLE
  batting_stats (
    batting_stat_id INTEGER PRIMARY KEY,
    inning_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    position INTEGER CHECK (position > 0),
    runs INTEGER DEFAULT 0,
    how_out TEXT,
    fielder_id INTEGER,
    bowler_id INTEGER,
    fours INTEGER DEFAULT 0,
    sixes INTEGER DEFAULT 0,
    balls INTEGER DEFAULT 0 CHECK (balls >= 0)
  );

-- Bowling Statistics
CREATE TABLE
  bowling_stats (
    bowling_stat_id INTEGER PRIMARY KEY,
    inning_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    overs REAL DEFAULT 0.0 CHECK (overs >= 0),
    maidens INTEGER DEFAULT 0 CHECK (maidens >= 0),
    runs INTEGER DEFAULT 0 CHECK (runs >= 0),
    wickets INTEGER DEFAULT 0 CHECK (wickets >= 0),
    wides INTEGER DEFAULT 0 CHECK (wides >= 0),
    no_balls INTEGER DEFAULT 0 CHECK (no_balls >= 0)
  );

-- Fall of Wickets
-- DROP TABLE fall_of_wickets;
CREATE TABLE
  fall_of_wickets (
    fow_id INTEGER PRIMARY KEY,
    inning_id INTEGER NOT NULL,
    runs INTEGER DEFAULT 0,
    wickets INTEGER DEFAULT 0 CHECK (wickets >= 0),
    batsman_out_id INTEGER NOT NULL,
    batsman_in_id INTEGER NOT NULL,
    batsman_in_runs INTEGER NOT NULL
  );

-- Result Summary
CREATE TABLE  result_summary (
    id INTEGER PRIMARY KEY,
    status TEXT,
    published TEXT,
    last_updated TEXT,
    league_name TEXT,
    league_id TEXT,
    competition_name TEXT,
    competition_id TEXT,
    competition_type TEXT,
    match_type TEXT,
    game_type TEXT,
    countdown_cricket TEXT,
    match_date TEXT,
    match_time TEXT,
    ground_name TEXT,
    ground_id TEXT,
    home_team_name TEXT,
    home_team_id TEXT,
    home_club_name TEXT,
    home_club_id TEXT,
    away_team_name TEXT,
    away_team_id TEXT,
    away_club_name TEXT,
    away_club_id TEXT,
    umpire_1_name TEXT,
    umpire_1_id TEXT,
    umpire_2_name TEXT,
    umpire_2_id TEXT,
    umpire_3_name TEXT,
    umpire_3_id TEXT,
    referee_name TEXT,
    referee_id TEXT,
    scorer_1_name TEXT,
    scorer_1_id TEXT,
    scorer_2_name TEXT,
    scorer_2_id TEXT,
    toss_won_by_team_id TEXT,
    toss TEXT,
    batted_first TEXT,
    no_of_overs TEXT,
    balls_per_innings TEXT,
    no_of_innings TEXT,
    result TEXT,
    result_description TEXT,
    result_applied_to TEXT,
    home_confirmed TEXT,
    away_confirmed TEXT,
    result_locked TEXT,
    scorecard_locked TEXT,
    match_notes TEXT,
    points_0_team_id INTEGER,
    points_0_game_points TEXT,
    points_0_penalty_points TEXT,
    points_0_bonus_points_together TEXT,
    points_0_bonus_points_batting TEXT,
    points_0_bonus_points_bowling TEXT,
    points_0_bonus_points_2nd_innings_together TEXT,
    points_1_team_id INTEGER,
    points_1_game_points TEXT,
    points_1_penalty_points TEXT,
    points_1_bonus_points_together TEXT,
    points_1_bonus_points_batting TEXT,
    points_1_bonus_points_bowling TEXT,
    points_1_bonus_points_2nd_innings_together TEXT,
    innings_0_team_batting_id TEXT,
    innings_0_innings_number INTEGER,
    innings_0_extra_byes TEXT,
    innings_0_extra_leg_byes TEXT,
    innings_0_extra_wides TEXT,
    innings_0_extra_no_balls TEXT,
    innings_0_extra_penalty_runs TEXT,
    innings_0_penalties_runs_awarded_in_other_innings TEXT,
    innings_0_total_extras TEXT,
    innings_0_runs TEXT,
    innings_0_wickets TEXT,
    innings_0_overs TEXT,
    innings_0_balls TEXT,
    innings_0_declared BOOLEAN,
    innings_0_forfeited_innings BOOLEAN,
    innings_0_revised_target_runs TEXT,
    innings_0_revised_target_overs TEXT,
    innings_0_revised_target_balls TEXT,
    innings_1_team_batting_id TEXT,
    innings_1_innings_number INTEGER,
    innings_1_extra_byes TEXT,
    innings_1_extra_leg_byes TEXT,
    innings_1_extra_wides TEXT,
    innings_1_extra_no_balls TEXT,
    innings_1_extra_penalty_runs TEXT,
    innings_1_penalties_runs_awarded_in_other_innings TEXT,
    innings_1_total_extras TEXT,
    innings_1_runs TEXT,
    innings_1_wickets TEXT,
    innings_1_overs TEXT,
    innings_1_balls TEXT,
    innings_1_declared BOOLEAN,
    innings_1_forfeited_innings BOOLEAN,
    innings_1_revised_target_runs TEXT,
    innings_1_revised_target_overs TEXT,
    innings_1_revised_target_balls TEXT
  );

-- Create club_teams table
CREATE TABLE
  club_teams (
    id INTEGER PRIMARY KEY,
    status TEXT,
    last_updated TEXT,
    site_id INTEGER,
    team_name TEXT,
    other_team_name TEXT,
    nickname TEXT,
    team_captain TEXT
  );

-- Create fixtures table
CREATE TABLE
  fixtures (
    id INTEGER PRIMARY KEY,
    status TEXT,
    published TEXT,
    last_updated TEXT,
    league_name TEXT,
    league_id INTEGER,
    competition_name TEXT,
    competition_id INTEGER,
    competition_type TEXT,
    match_type TEXT,
    game_type TEXT,
    season INTEGER,
    match_date TEXT,
    match_time TEXT,
    ground_name TEXT,
    ground_id INTEGER,
    ground_latitude TEXT,
    ground_longitude TEXT,
    home_club_name TEXT,
    home_team_name TEXT,
    home_team_id INTEGER,
    home_club_id INTEGER,
    away_club_name TEXT,
    away_team_name TEXT,
    away_team_id INTEGER,
    away_club_id INTEGER,
    umpire_1_name TEXT,
    umpire_1_id TEXT,
    umpire_2_name TEXT,
    umpire_2_id TEXT,
    umpire_3_name TEXT,
    umpire_3_id TEXT,
    referee_name TEXT,
    referee_id TEXT,
    scorer_1_name TEXT,
    scorer_1_id TEXT,
    scorer_2_name TEXT,
    scorer_2_id TEXT
  );

  CREATE TABLE
  sponsors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- Basic Sponsor Info
    sponsor_name TEXT NOT NULL,
    website_link TEXT,
    logo_url TEXT,            -- URL to the sponsor’s logo (instead of storing the image binary)

    -- Polymorphic Linking (Which entity is being sponsored?)
    sponsored_entity_type TEXT,     -- e.g., 'PLAYER', 'TEAM', or 'CLUB_WIDE'
    sponsored_entity_id   INTEGER,  -- The actual Player ID or Team ID

    -- Timestamps (optional, but good practice)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

-- Create player_batting_stats view
CREATE VIEW player_batting_stats AS
SELECT 
    p.name,
    COUNT(*) AS total_innings,
    MAX(bs.runs) AS high_score,
    SUM(bs.runs)*1.0 / NULLIF((COUNT(*) - COUNT(CASE WHEN bs.how_out = 'not out' THEN 1 END)), 0) AS average,
    SUM(bs.runs)*100.0 / NULLIF(SUM(bs.balls), 0) AS strike_rate,
    SUM(bs.runs) AS total_runs,
    SUM(bs.fours) AS total_fours,
    SUM(bs.sixes) AS total_sixes,
    COUNT(CASE WHEN bs.how_out = 'not out' THEN 1 END) AS not_out,
    SUM(CASE WHEN bs.runs >= 100 THEN 1 ELSE 0 END) AS hundred_count,
    SUM(CASE WHEN bs.runs >= 50 AND bs.runs < 100 THEN 1 ELSE 0 END) AS fifty_count
FROM batting_stats bs
JOIN innings i 
    ON bs.inning_id = i.inning_id
JOIN teams t 
    ON i.team_batting_id = t.team_id
JOIN players p 
    ON bs.player_id = p.member_id
WHERE t.club_id = 1969
GROUP BY p.member_id
ORDER BY total_runs desc;

-- Create bowler_stats view
CREATE VIEW bowler_stats AS
WITH bowler_agg AS (
  SELECT
    p.member_id,
    p.name,
    SUM( (CAST(bs.overs AS INTEGER) * 6) +
         CAST(((bs.overs - CAST(bs.overs AS INTEGER)) * 10) AS INTEGER)
       ) AS balls,
    SUM(bs.maidens) AS maidens,
    SUM(bs.wickets) AS wickets,
    SUM(bs.runs) AS runs,
    SUM(CASE WHEN bs.wickets >= 5 THEN 1 ELSE 0 END) AS five_wicket_hauls
  FROM bowling_stats bs
  JOIN innings i 
    ON bs.inning_id = i.inning_id
  JOIN match_players mp 
    ON i.match_id = mp.match_id AND bs.player_id = mp.player_id
  JOIN teams t 
    ON mp.team_id = t.team_id
  JOIN players p 
    ON bs.player_id = p.member_id
  WHERE t.club_id = 1969
  GROUP BY p.member_id, p.name
),
best_figures_cte AS (
  SELECT 
    bs.player_id,
    bs.wickets,
    bs.runs,
    ROW_NUMBER() OVER (PARTITION BY bs.player_id 
                       ORDER BY bs.wickets DESC, bs.runs ASC) AS rn
  FROM bowling_stats bs
  JOIN innings i 
    ON bs.inning_id = i.inning_id
  JOIN match_players mp 
    ON i.match_id = mp.match_id AND bs.player_id = mp.player_id
  JOIN teams t 
    ON mp.team_id = t.team_id
  WHERE t.club_id = 1969
)
SELECT 
  b.name,
  -- Convert total balls back to cricket overs notation: (overs.balls)
  (b.balls / 6) || '.' || (b.balls % 6) AS overs,
  b.maidens,
  b.wickets,
  bf.wickets || '/' || bf.runs AS best_figures,
  b.five_wicket_hauls,
  b.runs AS runs_conceded,
  b.runs * 1.0 / NULLIF(b.balls / 6.0, 0) AS economy
FROM bowler_agg b
LEFT JOIN best_figures_cte bf 
  ON b.member_id = bf.player_id AND bf.rn = 1
ORDER BY b.wickets DESC;

-- Create view for fixtures and results
CREATE VIEW
  fixtures_and_results AS
SELECT
  f.match_date,
  f.match_time,
  f.home_club_name,
  f.away_club_name,
  f.competition_name,
  f.ground_name,
  f.ground_latitude,
  f.ground_longitude,
  COALESCE(r.result_description, '') AS result
FROM
  fixtures f
  LEFT JOIN result_summary r ON f.id = r.id
ORDER BY
  SUBSTR(f.match_date, 7, 4) || '/' || SUBSTR(f.match_date, 4, 2) || '/' || SUBSTR(f.match_date, 1, 2) DESC;