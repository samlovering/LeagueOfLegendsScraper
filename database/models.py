import sqlalchemy
from sqlalchemy.orm import declarative_base

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:lovering@127.0.0.1:3306/lolesports")
Base = declarative_base()

'''

ASSETS

'''

class Champion(Base):
    __tablename__ = "champion"
    champion_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    champion_name = sqlalchemy.Column(sqlalchemy.String(255))
    champion_image = sqlalchemy.Column(sqlalchemy.String(255))
    
    def __repr__(self):
        return f"<Champion {self.champion_name}>"
    
'''

GENERAL INFORMATION

'''

class Team(Base):
    __tablename__ = "Team"
    team_id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)
    team_name = sqlalchemy.Column(sqlalchemy.String(255))
    league = sqlalchemy.Column(sqlalchemy.String(255))
    #team_slug = sqlalchemy.Column(sqlalchemy.String(255))
    #team_overviewpage = sqlalchemy.Column(sqlalchemy.String(255))
    
    def __repr__(self):
        return f"<Team {self.team_name}>"

class Player(Base):
    __tablename__ = "Player"
    player_id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)
    player_name = sqlalchemy.Column(sqlalchemy.String(255))

    def __repr__(self):
        return f"<Player {self.player_name}>"

class Team_Player(Base):
    __tablename__ = "Team_Player"
    team_player_id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)
    team_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Team.team_id"))
    player_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Player.player_id"))
    
    team = sqlalchemy.orm.relationship("Team", backref="team_players", lazy=True)
    player = sqlalchemy.orm.relationship("Player", backref="team_players", lazy=True)
    
    def __repr__(self):
        return f"<Team_Player {self.team_id} - {self.player_id}>"

'''

LOLESPORTS INFORMATION

'''

class League(Base):
    __tablename__ = "League"
    league_id = sqlalchemy.Column(sqlalchemy.String(255),primary_key=True)
    oracle_name = sqlalchemy.Column(sqlalchemy.String(255))
    lolesports_name = sqlalchemy.Column(sqlalchemy.String(255))

'''

GAME INFORMATION


'''


class Game(Base):
    __tablename__ = "Game"
    game_id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)
    team1_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Team.team_id"))
    team2_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Team.team_id"))
    date = sqlalchemy.Column(sqlalchemy.DateTime)
    data_complete = sqlalchemy.Column(sqlalchemy.String(255))
    url = sqlalchemy.Column(sqlalchemy.String(255))
    league = sqlalchemy.Column(sqlalchemy.String(255))
    year = sqlalchemy.Column(sqlalchemy.Integer)
    split = sqlalchemy.Column(sqlalchemy.String(255))
    playoffs = sqlalchemy.Column(sqlalchemy.Boolean)
    game_in_series = sqlalchemy.Column(sqlalchemy.Integer)
    patch = sqlalchemy.Column(sqlalchemy.String(255))
    
    team1 = sqlalchemy.orm.relationship("Team", foreign_keys=[team1_id], backref="games_as_team1", lazy=True)
    team2 = sqlalchemy.orm.relationship("Team", foreign_keys=[team2_id], backref="games_as_team2", lazy=True)
    
    def __repr__(self):
        return f"<Game {self.game_id}>"
    
class Team_Draft(Base):
    __tablename__ = "Team_Draft"
    team_game_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Team_Game.team_game_id"), primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Game.game_id"))
    team_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Team.team_id"))
    ban1 = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("champion.champion_id"))
    ban2 = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("champion.champion_id"))
    ban3 = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("champion.champion_id"))
    ban4 = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("champion.champion_id"))
    ban5 = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("champion.champion_id"))
    pick1 = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("champion.champion_id"))
    pick2 = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("champion.champion_id"))
    pick3 = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("champion.champion_id"))
    pick4 = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("champion.champion_id"))
    pick5 = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("champion.champion_id"))

    game = sqlalchemy.orm.relationship("Game", backref="team_drafts", lazy=True)
    team = sqlalchemy.orm.relationship("Team", backref="team_drafts", lazy=True)
    ban1_champion = sqlalchemy.orm.relationship("Champion", foreign_keys=[ban1], lazy=True)
    ban2_champion = sqlalchemy.orm.relationship("Champion", foreign_keys=[ban2], lazy=True)
    ban3_champion = sqlalchemy.orm.relationship("Champion", foreign_keys=[ban3], lazy=True)
    ban4_champion = sqlalchemy.orm.relationship("Champion", foreign_keys=[ban4], lazy=True)
    ban5_champion = sqlalchemy.orm.relationship("Champion", foreign_keys=[ban5], lazy=True)
    pick1_champion = sqlalchemy.orm.relationship("Champion", foreign_keys=[pick1], lazy=True)
    pick2_champion = sqlalchemy.orm.relationship("Champion", foreign_keys=[pick2], lazy=True)
    pick3_champion = sqlalchemy.orm.relationship("Champion", foreign_keys=[pick3], lazy=True)
    pick4_champion = sqlalchemy.orm.relationship("Champion", foreign_keys=[pick4], lazy=True)
    pick5_champion = sqlalchemy.orm.relationship("Champion", foreign_keys=[pick5], lazy=True)

    def __repr__(self):
        return f"<Team_Draft {self.team_game_id} - {self.game_id} - {self.team_id}>"
    
'''

TEAM GAME INFORATION

'''    

class Team_Game(Base):
    __tablename__ = "Team_Game"
    team_game_id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Game.game_id"))
    team_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Team.team_id"))
    game_length = sqlalchemy.Column(sqlalchemy.Integer)
    side = sqlalchemy.Column(sqlalchemy.String(255))
    result = sqlalchemy.Column(sqlalchemy.Boolean)
    
    game = sqlalchemy.orm.relationship("Game", backref="team_games", lazy=True)
    team = sqlalchemy.orm.relationship("Team", backref="team_games", lazy=True)
    
    def __repr__(self):
        return f"<Team_Game {self.team_game_id} - {self.game_id} - {self.team_id}>"

class Team_Game_Combat(Base):
    __tablename__ = "Team_Game_Combat"
    team_game_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Team_Game.team_game_id"), primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Game.game_id"))
    team_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Team.team_id"))
    kills = sqlalchemy.Column(sqlalchemy.Integer)
    deaths = sqlalchemy.Column(sqlalchemy.Integer)
    assists = sqlalchemy.Column(sqlalchemy.Integer)
    doublekills = sqlalchemy.Column(sqlalchemy.Integer)
    triplekills = sqlalchemy.Column(sqlalchemy.Integer)
    quadrakills = sqlalchemy.Column(sqlalchemy.Integer)
    pentakills = sqlalchemy.Column(sqlalchemy.Integer)
    firstblood = sqlalchemy.Column(sqlalchemy.Boolean)
    damagetochampions = sqlalchemy.Column(sqlalchemy.Integer)
    
    game = sqlalchemy.orm.relationship("Game", backref="team_combats", lazy=True)
    team = sqlalchemy.orm.relationship("Team", backref="team_combats", lazy=True)
    
    def __repr__(self):
        return f"<Team_Combat {self.team_game_id} - {self.game_id} - {self.team_id}>"

class Team_Game_Objectives(Base):
    __tablename__ = "Team_Game_Objectives"
    team_game_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Team_Game.team_game_id"), primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Game.game_id"))
    team_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Team.team_id"))
    dragons = sqlalchemy.Column(sqlalchemy.Integer)
    firstdragon = sqlalchemy.Column(sqlalchemy.Boolean)
    infernals = sqlalchemy.Column(sqlalchemy.Integer)
    mountains = sqlalchemy.Column(sqlalchemy.Integer)
    clouds = sqlalchemy.Column(sqlalchemy.Integer)
    oceans = sqlalchemy.Column(sqlalchemy.Integer)
    chemtechs = sqlalchemy.Column(sqlalchemy.Integer)
    hextechs = sqlalchemy.Column(sqlalchemy.Integer)
    elders = sqlalchemy.Column(sqlalchemy.Integer)
    heralds = sqlalchemy.Column(sqlalchemy.Integer)
    firstherald = sqlalchemy.Column(sqlalchemy.Boolean)
    voidgrubs = sqlalchemy.Column(sqlalchemy.Integer)
    barons = sqlalchemy.Column(sqlalchemy.Integer)
    firstbaron = sqlalchemy.Column(sqlalchemy.Boolean)
    firsttower = sqlalchemy.Column(sqlalchemy.Boolean)
    firstmidtower = sqlalchemy.Column(sqlalchemy.Boolean)
    firsttothreetowers = sqlalchemy.Column(sqlalchemy.Boolean)
    towers = sqlalchemy.Column(sqlalchemy.Integer)
    turretplates = sqlalchemy.Column(sqlalchemy.Integer)
    inhibitors = sqlalchemy.Column(sqlalchemy.Integer)
    
    game = sqlalchemy.orm.relationship("Game", backref="team_game_objectives", lazy=True)
    team = sqlalchemy.orm.relationship("Team", backref="team_game_objectives", lazy=True)
    
    def __repr__(self):
        return f"<Team_Game_Objectives {self.team_game_id} - {self.game_id} - {self.team_id}>"

class Team_Game_Economy(Base):
    __tablename__ = "Team_Game_Economy"
    team_game_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Team_Game.team_game_id"), primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Game.game_id"))
    team_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Team.team_id"))
    totalgold = sqlalchemy.Column(sqlalchemy.Integer)
    goldspent = sqlalchemy.Column(sqlalchemy.Integer)
    minionkills = sqlalchemy.Column(sqlalchemy.Integer)
    monsterkills = sqlalchemy.Column(sqlalchemy.Integer)
    
    game = sqlalchemy.orm.relationship("Game", backref="team_game_economies", lazy=True)
    team = sqlalchemy.orm.relationship("Team", backref="team_game_economies", lazy=True)
    
    def __repr__(self):
        return f"<Team_Game_Economy {self.team_game_id} - {self.game_id} - {self.team_id}>"

class Team_Game_Vision(Base):
    __tablename__ = "Team_Game_Vision"
    team_game_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Team_Game.team_game_id"), primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Game.game_id"))
    team_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Team.team_id"))
    wardsplaced = sqlalchemy.Column(sqlalchemy.Integer)
    wardskilled = sqlalchemy.Column(sqlalchemy.Integer)
    controlwardsbought = sqlalchemy.Column(sqlalchemy.Integer)
    visionscore = sqlalchemy.Column(sqlalchemy.Integer)
    
    game = sqlalchemy.orm.relationship("Game", backref="team_game_visions", lazy=True)
    team = sqlalchemy.orm.relationship("Team", backref="team_game_visions", lazy=True)
    
    def __repr__(self):
        return f"<Team_Game_Vision {self.team_game_id} - {self.game_id} - {self.team_id}>"

class Team_Game_At15(Base):
    __tablename__ = "Team_Game_At15"
    team_game_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Team_Game.team_game_id"), primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Game.game_id"))
    team_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Team.team_id"))
    goldat15 = sqlalchemy.Column(sqlalchemy.Integer)
    xpat15 = sqlalchemy.Column(sqlalchemy.Integer)
    csat15 = sqlalchemy.Column(sqlalchemy.Integer)
    xpdiffat15 = sqlalchemy.Column(sqlalchemy.Integer)
    golddiffat15 = sqlalchemy.Column(sqlalchemy.Integer)
    csdiffat15 = sqlalchemy.Column(sqlalchemy.Integer)
    
    game = sqlalchemy.orm.relationship("Game", backref="team_game_at15s", lazy=True)
    team = sqlalchemy.orm.relationship("Team", backref="team_game_at15s", lazy=True)
    
    def __repr__(self):
        return f"<Team_Game_At15 {self.team_game_id} - {self.game_id} - {self.team_id}>"
    
    
'''

GAME Player INFORMATION

'''    
class Game_Player(Base):
    __tablename__ = "Game_Player"
    game_player_id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Game.game_id"))
    player_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Player.player_id"))
    team_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Team.team_id"))
    game_length = sqlalchemy.Column(sqlalchemy.Integer)
    side = sqlalchemy.Column(sqlalchemy.String(255))
    result = sqlalchemy.Column(sqlalchemy.Boolean)
    champion_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("champion.champion_id"))

    game = sqlalchemy.orm.relationship("Game", backref="game_players", lazy=True)
    player = sqlalchemy.orm.relationship("Player", backref="game_players", lazy=True)
    team = sqlalchemy.orm.relationship("Team", backref="game_players", lazy=True)
    champion = sqlalchemy.orm.relationship("Champion", backref="game_players", lazy=True)

    def __repr__(self):
        return f"<game_player {self.game_player_id} - {self.game_id} - {self.player_id}>"

class Game_Player_Combat(Base):
    __tablename__ = "Game_Player_Combat"
    game_player_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Game_Player.game_player_id"), primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Game.game_id"))
    player_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Player.player_id"))
    kills = sqlalchemy.Column(sqlalchemy.Integer)
    deaths = sqlalchemy.Column(sqlalchemy.Integer)
    assists = sqlalchemy.Column(sqlalchemy.Integer)
    doublekills = sqlalchemy.Column(sqlalchemy.Integer)
    triplekills = sqlalchemy.Column(sqlalchemy.Integer)
    quadrakills = sqlalchemy.Column(sqlalchemy.Integer)
    pentakills = sqlalchemy.Column(sqlalchemy.Integer)
    firstblood = sqlalchemy.Column(sqlalchemy.Boolean)
    firstbloodkill = sqlalchemy.Column(sqlalchemy.Boolean)
    firstbloodassist = sqlalchemy.Column(sqlalchemy.Boolean)
    firstbloodvictim = sqlalchemy.Column(sqlalchemy.Boolean)
    damagetochampions = sqlalchemy.Column(sqlalchemy.Integer)

    game = sqlalchemy.orm.relationship("Game", backref="player_combats", lazy=True)
    player = sqlalchemy.orm.relationship("Player", backref="player_combats", lazy=True)

    def __repr__(self):
        return f"<Game_Player_Combat {self.game_player_id} - {self.game_id} - {self.player_id}>"

class Game_Player_Economy(Base):
    __tablename__ = "Game_Player_Economy"
    game_player_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Game_Player.game_player_id"), primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Game.game_id"))
    player_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Player.player_id"))
    totalgold = sqlalchemy.Column(sqlalchemy.Integer)
    goldspent = sqlalchemy.Column(sqlalchemy.Integer)
    minionkills = sqlalchemy.Column(sqlalchemy.Integer)
    monsterkills = sqlalchemy.Column(sqlalchemy.Integer)

    game = sqlalchemy.orm.relationship("Game", backref="player_economies", lazy=True)
    player = sqlalchemy.orm.relationship("Player", backref="player_economies", lazy=True)

    def __repr__(self):
        return f"<Game_Player_Economy {self.game_player_id} - {self.game_id} - {self.player_id}>"

class Game_Player_Vision(Base):
    __tablename__ = "Game_Player_Vision"
    game_player_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Game_Player.game_player_id"), primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Game.game_id"))
    player_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Player.player_id"))
    wardsplaced = sqlalchemy.Column(sqlalchemy.Integer)
    wardskilled = sqlalchemy.Column(sqlalchemy.Integer)
    controlwardsbought = sqlalchemy.Column(sqlalchemy.Integer)
    visionscore = sqlalchemy.Column(sqlalchemy.Integer)

    game = sqlalchemy.orm.relationship("Game", backref="player_visions", lazy=True)
    player = sqlalchemy.orm.relationship("Player", backref="player_visions", lazy=True)

    def __repr__(self):
        return f"<Game_Player_Vision {self.game_player_id} - {self.game_id} - {self.player_id}>"

class Game_Player_At15(Base):
    __tablename__ = "Game_Player_At15"
    game_player_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Game_Player.game_player_id"), primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Game.game_id"))
    player_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("Player.player_id"))
    goldat15 = sqlalchemy.Column(sqlalchemy.Integer)
    xpat15 = sqlalchemy.Column(sqlalchemy.Integer)
    csat15 = sqlalchemy.Column(sqlalchemy.Integer)
    xpdiffat15 = sqlalchemy.Column(sqlalchemy.Integer)
    golddiffat15 = sqlalchemy.Column(sqlalchemy.Integer)
    csdiffat15 = sqlalchemy.Column(sqlalchemy.Integer)

    game = sqlalchemy.orm.relationship("Game", backref="player_at15s", lazy=True)
    player = sqlalchemy.orm.relationship("Player", backref="player_at15s", lazy=True)

    def __repr__(self):
        return f"<Game_Player_At15 {self.game_player_id} - {self.game_id} - {self.player_id}>"