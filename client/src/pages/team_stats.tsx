import { useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Table from '../components/table';
import '../styles/team_stats.css';
import type { ColDef } from 'ag-grid-community';
import TeamHeader from '../components/team_header';

function TeamStatsPage() {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const id = params.get('id');
  const [teamStats, setTeamStats] = useState<any>(null);


  //Fetch the team stats
  async function fetchTeamStats(id: string, setTeamStats: (data: any) => void) {
    const retries = 5;
    const delay = 1000;
    for (let attempt = 0; attempt < retries; attempt++) {
      try {
        const response = await fetch(`/api/getTeamStats?id=${id}`);
        if (!response.ok) throw new Error('Network Response Error: ' + response.statusText);
        const data = await response.json();
        setTeamStats(data);
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

  //When page loads, fetch the team stats
  useEffect(() => {
    let isMounted = true;
    if (id) {
      fetchTeamStats(id, data => {
        if (isMounted) setTeamStats(data);
      });
    }
    return () => { isMounted = false; };
  }, [id]);
  //Helper for Images
  type ChampImage = {
    src: string;
    count: number;
    alt?: string;
  };
  //Player object
  type Player = {
    role: string;
    name: string;
    kda: number;
    avg_gold: number;
    avg_dmg: number;
    champions: ChampImage[];
  };


//Process player data for the table
const roleOrder = ["top", "jng", "mid", "bot", "sup"];
const player_data: Player[] = teamStats
  ? teamStats.players.map((p: any) => ({
      role: p.role,
      name: p.player_name,
      kda: Number(p.kda),
      avg_gold: Number(p.avg_total_gold),
      avg_dmg: Number(p.avg_damage_to_champions),
      champions: p.champions_played
        .sort((a: any, b: any) => b.count - a.count)
        .slice(0, 5)
        .map((c: any) => ({
          src: `https://ddragon.canisback.com/img/champion/tiles/${c.champion_name}_0.jpg`,
          alt: c.champion_name,
          count: c.count,
        })),
    }))
    .sort((a: { role: string; }, b: { role: string; }) => roleOrder.indexOf(a.role) - roleOrder.indexOf(b.role))
  : [];

//Define columns/formatting for the table
const columnDefs: ColDef<Player>[] = [
  { field: "role", cellStyle: { textAlign: 'left' } },
  { field: "name", cellStyle: { textAlign: 'left' } },
  { field: "kda", cellStyle: { textAlign: 'center' } },
  { 
    field: "avg_gold",
    valueFormatter: params => params.value != null ? Number(params.value).toFixed(2) : "",
  },
  { 
    field: "avg_dmg",
    valueFormatter: params => params.value != null ? Number(params.value).toFixed(2) : "",
  },
  { 
    field: "champions", 
    autoHeight: true,
    valueFormatter: () => "",
    cellRenderer: (params: { value: { src: string; count: number; alt?: string; }[]; }) => {
      const champions: ChampImage[] = params.value;
      return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
          {champions.map((champion, index) => (
            <div key={index} style={{ textAlign: 'center' }}>
              <img
                src={champion.src}
                alt={champion.alt || 'Champion'}
                style={{ width: '30px', height: '30px', borderRadius: '20%', display: 'block', margin: '0 0' }}
                title={champion.alt}
              />
              <div style={{ fontSize: '1.4em' }}>{champion.count}</div>
            </div>    
          ))}
        </div>
      );
    },
  }
];

  //Render page
  return (
    <div className='team-stats-page'>
      <TeamHeader />
    {teamStats ? (
      <div>
        <h2>{teamStats.team_info.team_name}</h2>
        <div className="team-stats-grid">

          <div className="team-stats-box">
            <div className="team-stats-box-label">General</div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Region:</div>
              <div className="team-stats-value">{teamStats.team_info.league}</div>
            </div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Wins Rate:</div>
              <div className="team-stats-value">{teamStats.team_basic_stats.wins} - {teamStats.team_basic_stats.losses}</div>
            </div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label"></div>
              <div className="team-stats-value" style={{ textAlign: "right", width: "100%" }}>
              {teamStats.team_basic_stats.win_rate}%
              </div>
            </div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Average Game Duration:</div>
              <div className="team-stats-value">{(teamStats.team_basic_stats.avg_game_length / 60).toFixed(2)} mins</div>
            </div>
          </div>

          <div className="team-stats-box">
            <div className="team-stats-box-label">Economy</div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Avg CSPM:</div>
              <div className="team-stats-value">{teamStats.team_economy.avg_cspm}</div>
            </div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Avg GPM:</div>
              <div className="team-stats-value">{teamStats.team_economy.avg_gpm}</div>
            </div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Average CS / Game:</div>
              <div className="team-stats-value">{Number(teamStats.team_economy.avg_minion_kills).toFixed(2)}</div>
            </div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Average Gold / Game:</div>
              <div className="team-stats-value">{Number(teamStats.team_economy.avg_total_gold).toFixed(2)}</div>
            </div>
          </div>

          <div className="team-stats-box">
            <div className="team-stats-box-label">Combat</div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">First Blood Rate:</div>
              <div className="team-stats-value">{teamStats.team_combat.first_blood_rate}</div>
            </div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Average Kills:</div>
              <div className="team-stats-value">{teamStats.team_combat.avg_kills}</div>
            </div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Average Deaths:</div>
              <div className="team-stats-value">{teamStats.team_combat.avg_deaths}</div>
            </div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Average Assists:</div>
              <div className="team-stats-value">{teamStats.team_combat.avg_assists}</div>
            </div>
          </div>
          <div className="team-stats-box">
            <div className="team-stats-box-label">Objectives</div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Average Dragons:</div>
              <div className="team-stats-value">{teamStats.team_objectives.dragons_per_game}</div>
            </div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Average Dragons:</div>
              <div className="team-stats-value">{teamStats.team_objectives.dragons_per_game}</div>
            </div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Average Voidgrubs:</div>
              <div className="team-stats-value">{teamStats.team_objectives.voidgrubs_per_game}</div>
            </div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Average Heralds:</div>
              <div className="team-stats-value">{teamStats.team_objectives.heralds_per_game}</div>
            </div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Average Atakhans:</div>
              <div className="team-stats-value">{teamStats.team_objectives.atakhan_per_game}</div>
            </div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Average Barons:</div>
              <div className="team-stats-value">{teamStats.team_objectives.barons_per_game}</div>
            </div>
          </div>
          <div className="team-stats-box">
            <div className="team-stats-box-label">Vision</div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Average Vision Score Per Min:</div>
              <div className="team-stats-value">{teamStats.team_vision.vspm}</div>
            </div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Wards Killed Per Min:</div>
              <div className="team-stats-value">{teamStats.team_vision.wkpm}</div>
            </div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Control Wards Per Min:</div>
              <div className="team-stats-value">{teamStats.team_vision.control_wpm}</div>
            </div>
            <div className="team-stats-value-row">
              <div className="team-stats-value-label">Wards Placed Per Min:</div>
              <div className="team-stats-value">{teamStats.team_vision.wpm}</div>
            </div>
            
          </div>
        </div>
        <div className='team-stats-box' style={{ marginTop: '20px' }}>
          <div className="team-stats-box-label">Players:</div>
          <Table<Player> rowData={player_data} columnDefs={columnDefs} />
        </div>
      </div>
      ): (
        <h2>Loading team stats...</h2>
      )}
    </div>
  );
}
export default TeamStatsPage;