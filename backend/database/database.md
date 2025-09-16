<h1>Database Layout:</h1>

# General Information

## Teams
**team_id** - Int **Primary Key**\
team_name - var char SLUG FORM\
team_slug varchar\
region - varchar\
created_at - TIMESTAMP\
I am unsure what other information would go here, maybe image links?

## Players
**player_id** - INT **Primary Key**\
player_name - varchar\
player_ign - varchar\
region - varchar\
created_at - TIMESTAMP\

## Team_Player
**team_player_id** INT **Primary Key**\
team_id INT NOT NULL \
player_id INT NOT NULL \
start_date DATE NOT NULL\
end_date DATE\
FOREIGN KEY (team_id) REFERENCES Teams(team_id),\
FOREIGN KEY (player_id) REFERENCES Players(player_id)\

# Game Information

## Games
**game_id** INT **Primary Key**\
game_time TIMESTAMP \
duration TIMESTAMP \
team1_id INT NOT NULL\
team2_id INT NOT NULL\
pick_bans_id INT NOT NULL\
winder_id INT, (From Teams Table)\
tournament_name varchar\
patch_version varchar\
FOREIGN KEY (team1_id) REFERENCES Teams(team_id)\
FOREIGN KEY (team2_id) REFERENCES Teams(team_id)\
FOREIGN KEY (winner_id) REFERENCES Teams(team_id)\
FOREIGN KEY (pick_bans_id) REFERENCES PickBans(pick_bans_id)\

# Game Team Information

## Game_Team
**game_team_id** INT **primary Key**\
team_id INT NOT NULL\
team_kills INT\
team_atakahn INT\
team_baron INT\
team_dragons INT\
team_towers INT\
team_voidgrubs INT \
team_inhibitors INT\



## PicksBans
game_id INT NOT NULL\
team1_id INT NOT NULL\
team2_id INT NOT NULL\
Team1Ban1 INT,\
Team2Ban1 INT,\
Team1Ban2 INT,\
Team2Ban2 INT,\
Team1Ban3 INT,\
Team2Ban3 INT,\
Team1Pick1 INT,\
Team2Pick1 INT,\
Team2Pick2 INT,\
Team1Pick2 INT,\
Team1Pick3 INT,\
Team2Pick3 INT,\
Team2Ban4 INT,\
Team1Ban4 INT,\
Team2Ban5 INT,\
Team1Ban5 INT,\
Team2Pick4 INT,\
Team1Pick4 INT,\
Team1Pick5 INT,\
Team2Pick5 INT,\
PRIMARY KEY (game_id)\
FOREIGN KEY (game_id) REFERENCES Games(game_id)\
FOREIGN KEY (team1_id) REFERENCES Games(team1_id)\
FOREIGN Key (team2_id) REFERENCES Games(team2_id)\

# Game Player Info

## Game_Player
game_player_id INT PRIMARY KEY AUTO_INCREMENT,\
game_id INT NOT NULL,\
player_id INT NOT NULL,\
team_id INT NOT NULL,\
champion_played INT NOT NULL\
role VARCHAR(50),\
kills INT,\
deaths INT,\
assists INT,\
cs INT\
gold INT \
vision_score INT \
damage_to_champions INT 

FOREIGN KEY (game_id) REFERENCES Games(game_id),\
FOREIGN KEY (player_id) REFERENCES Players(player_id),\
FOREIGN KEY (team_id) REFERENCES Teams(team_id)\


## Player_Runes
**player_runes_id** INT **Primary Key**\
game_id INT NOT NULL\
player_id INT NOT NULL\
primary_tree_id INT\
secondary_tree_id INT\
primary_slot1_id INT\
primary_slot2_id INT\
primary_slot3_id INT\
primary_slot4_id INT\
secondary_slot1_id INT\
secondary_slot2_id INT\
secondary_slot3_id INT\
FOREIGN KEY (game_player_id) REFERENCES Game_Player(game_player_id)\

## Items
**player_items_id** INT **Primary Key**\
game_id INT NOT NULL\
player_id INT NOT NULL\
item_slot1_id INT\
item_slot2_id INT\
item_slot3_id INT\
item_slot4_id INT\
item_slot5_id INT\
item_slot6_id INT\
FOREIGN KEY (game_player_id) REFERENCES Game_Player(game_player_id)\

## Summoner Spells
**player_spells_id** INT **Primary Key**\
game_id INT NOT NULL\
player_id INT NOT NULL\
spell_slot1_id INT\
spell_slot2_id INT\
FOREIGN KEY (game_player_id) REFERENCES Game_Player(game_player_id)\

# Asset Tables

## Runes

**rune_id** INT **Primary Key** \
rune_name  varchar\
rune_image_path varchar\

## Summoner Spells
**Summoner Spells** INT **Primary Key** \
spell_name  varchar\
spell_image_path varchar\

## Items
**items_id** INT **Primary Key** \
items_name  varchar\
items_image_path varchar\


