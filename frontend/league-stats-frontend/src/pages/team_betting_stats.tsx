import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import TeamHeader from "../components/team_header";
import "../styles/team_betting_stats.css"


function TeamBettingPage() {
    const location = useLocation();
    const params = new URLSearchParams(location.search);
    const id = params.get('id');
    const [bettingStats, setBettingStats] = useState<any>(null);


    async function fetchBettingStats(id: string, setBettingStats: (data: any) => void) {
        const retries = 5;
        const delay = 1000;
        for (let attempt = 0; attempt < retries; attempt++) {
            try {
                const response = await fetch(`/api/getTeamBettingStats?id=${id}`);
                if (!response.ok) throw new Error('Network Response Error: ' + response.statusText);
                const data = await response.json();
                setBettingStats(data);
                console.log(data);
                return;
            } catch (error) {
                if (attempt === retries - 1) {
                    console.error('Failed to fetch team stats after retries:', error);
                } else {
                    await new Promise(res => setTimeout(res, delay));
                }
            }
        }
    }

    //Fetch the team list
    useEffect(() => {
        let isMounted = true;
        if (id) {
            fetchBettingStats(id, data => {
                if (isMounted) setBettingStats(data);
            });
        }
        return () => { isMounted = false; };
    }, [id]);


    return (
    <div className='betting-stats-page'>
        <TeamHeader />
        <h2 className="title">Team Betting Stats</h2>
        
        {bettingStats ? (
                  <div>
        <div className="betting-stats-grid">

          <div className="betting-stats-box">
            <div className="betting-stats-box-label">General</div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">Team:</div>
              <div className="betting-stats-value">{bettingStats.team_name}</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">Wins Rate:</div>
              <div className="betting-stats-value">{Number(bettingStats.win_rate * 100).toFixed(2)}%</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">Games Played:</div>
              <div className="betting-stats-value">{bettingStats.num_games}</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">Average Game Duration:</div>
              <div className="betting-stats-value">{(bettingStats.avg_length / 60).toFixed(2)} mins</div>
            </div>
          </div>
          <div className="betting-stats-box">
            <div className="betting-stats-box-label">Kills</div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">Avg Kills:</div>
              <div className="betting-stats-value">{Number(bettingStats.avg_kills).toFixed(2)}</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">Avg Deaths:</div>
              <div className="betting-stats-value">{Number(bettingStats.avg_deaths).toFixed(2)}</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">Avg Combined Kills:</div>
              <div className="betting-stats-value">{Number(bettingStats.c_kills).toFixed(2)}</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">% Over 23 Kills (Combined):</div>
              <div className="betting-stats-value">{Number(bettingStats.kills_over23*100).toFixed(2)}%</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">% Over 25 Kills (Combined):</div>
              <div className="betting-stats-value">{Number(bettingStats.kills_over25*100).toFixed(2)}%</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">% Over 27 Kills (Combined):</div>
              <div className="betting-stats-value">{Number(bettingStats.kills_over27*100).toFixed(2)}%</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">% Over 29 Kills (Combined):</div>
              <div className="betting-stats-value">{Number(bettingStats.kills_over29*100).toFixed(2)}%</div>
            </div>
          </div>

          <div className="betting-stats-box">
            <div className="betting-stats-box-label">Structures</div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">% Inhibitors Over 1:</div>
              <div className="betting-stats-value">{Number(bettingStats.inhibitors_over1*100).toFixed(2)}%</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">% Towers Over 10:</div>
              <div className="betting-stats-value">{Number(bettingStats.towers_over10*100).toFixed(2)}%</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">% Towers Over 11:</div>
              <div className="betting-stats-value">{Number(bettingStats.towers_over11*100).toFixed(2)}%</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">% Towers Over 12:</div>
              <div className="betting-stats-value">{Number(bettingStats.towers_over12*100).toFixed(2)}%</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">Average Combined Towers:</div>
              <div className="betting-stats-value">{Number(bettingStats.c_towers).toFixed(2)}</div>
            </div>
          </div>
          <div className="betting-stats-box">
            <div className="betting-stats-box-label">Objectives</div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">% Dragons Over 4 (Combined):</div>
              <div className="betting-stats-value">{Number(bettingStats.dragons_over4*100).toFixed(2)}%</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">% Dragons Over 5 (Combined):</div>
              <div className="betting-stats-value">{Number(bettingStats.dragons_over5*100).toFixed(2)}%</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">Average Combined Dragons:</div>
              <div className="betting-stats-value">{Number(bettingStats.c_dragons).toFixed(2)}</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">Average Combined Barons:</div>
              <div className="betting-stats-value">{Number(bettingStats.c_barons).toFixed(2)}</div>
            </div>
          </div>
          <div className="betting-stats-box">
            <div className="betting-stats-box-label">Firsts</div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">% First Blood:</div>
              <div className="betting-stats-value">{Number(bettingStats.first_blood_pct*100).toFixed(2)}%</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">% First Dragon:</div>
              <div className="betting-stats-value">{Number(bettingStats.first_dragon_pct*100).toFixed(2)}%</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">% First Tower:</div>
              <div className="betting-stats-value">{Number(bettingStats.first_tower_pct*100).toFixed(2)}%</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">% First Herald:</div>
              <div className="betting-stats-value">{Number(bettingStats.first_herald_pct*100).toFixed(2)}%</div>
            </div>
            <div className="betting-stats-value-row">
              <div className="betting-stats-value-label">% First Baron:</div>
              <div className="betting-stats-value">{Number(bettingStats.first_baron_pct*100).toFixed(2)}%</div>
            </div>
          </div>
        </div>
    </div>
    ) : (
        <h2>Loading team stats...</h2>
    )}
    </div>
);

}
export default TeamBettingPage;

/**
 *  General
 *  Kills
 * Structures
 * Objectives
 * Firsts
 * Combined
 */