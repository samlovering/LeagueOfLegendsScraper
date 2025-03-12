from flask import Flask, jsonify, render_template, request, make_response

from database import game_db, team_db
from stat_calc import betting_stats

app = Flask(__name__)

@app.route('/api/getLeagues',methods=['GET'])
def get_leagues():
    return jsonify(game_db.getLeagues())

@app.route('/api/getPatches', methods=['GET'])
def get_patches():
    return jsonify(game_db.getPatches())

@app.route('/api/getBettingStatsForLeague', methods=['GET','POST'])
def getBettingStatsForLeague():
    data = request.json
    league = data.get('league')
    teams = team_db.getTeamsByLeague(league)
    print(teams)
    team_stats_list = [betting_stats.create_team_betting_stats(team['team_id']) for team in teams]
    return jsonify(team_stats_list)


@app.route('/betting', methods=['GET'])
def betting_stats_page():
    return render_template('betting.html')


def start_server():
    app.run(host='0.0.0.0', port=5000, debug=True)