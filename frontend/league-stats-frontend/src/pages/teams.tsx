import { useEffect, useState } from "react";
import type { ColDef } from 'ag-grid-community';
import Table from "../components/table";
import "../styles/teams.css"


function TeamList(){
    const [teamList, setTeamList] = useState<any>(null);

    type Team = {
        id: string;
        name: string;
        region: string;
        games_played: number;
        wins: number;
        losses: number;
        win_rate: number;
        avg_game_length: number;
    };

    const team_data: Team[] = teamList ? teamList.map((team: any) => ({
        id: team.team_id,
        name: team.team_name,
        region: team.league,
        games_played: team.games_played,
        wins: team.wins,
        losses: team.losses,
        win_rate: team.win_rate,
        avg_game_length: team.avg_game_length,
    })) : [];

    const columnDefs: ColDef<Team>[] = [
        {   
            field: "name",
            flex: 3,
            cellStyle: { textAlign: 'left' },
            cellRenderer: (params: { data: { id: string }; value: string }) => {
                return (
                    <a className="team-link" href={`/team?id=${params.data.id}`}>
                        {params.value}
                    </a>
                );
            },
        },
        { field: "region", cellStyle: { textAlign: 'left' }, sortable: true, filter: true,  flex: 2, initialSort: 'asc' },
        { 
            field: "games_played",
            headerClass: "text-center", 
            headerName: "Games Played", 
            cellStyle: { textAlign: 'center' }, 
            flex: 2 
        },
        { field: "wins", headerClass: "text-center", cellStyle: { textAlign: 'center' }, sortable: true, flex: 1 },
        { field: "losses", headerClass: "text-center", cellStyle: { textAlign: 'center' }, sortable: true, flex: 1 },
        {
            field: "win_rate",
            headerClass: "text-center",
            cellStyle: { textAlign: 'center' },
            valueFormatter: params => params.value != null ? (params.value * 1).toFixed(2) + '%' : ""
        },
    ]

    async function fetchTeamList(setTeamList: (data: any) => void) {
        const retries = 5;
        const delay = 1000;
        for (let attempt = 0; attempt < retries; attempt++) {
            try {
                const response = await fetch(`/api/getTeamList`);
                if (!response.ok) throw new Error('Network Response Error: ' + response.statusText);
                const data = await response.json();
                setTeamList(data.teams);
                return;
            } catch (error) {
                console.error('Fetch attempt failed:', error);
            }
            if (attempt === retries - 1) {
                console.error('Failed to fetch team list after retries:');
            } else {
                await new Promise(res => setTimeout(res, delay));
            }
        }
    }
    //Fetch the team list
    useEffect(() => {
    let isMounted = true;
      fetchTeamList(data => {
        if (isMounted) setTeamList(data);
      });
        return () => { isMounted = false; }
    }, []);


    return (
    <div className='team-list-page'>
        <h2 className="title">Team List Page</h2>
        <p className="subtitle">Click name to go to link</p>
        {teamList ? (
            <Table<Team> rowData={team_data} columnDefs={columnDefs} />
        ) : (
            <p className="team-list-loading">Loading team list...</p>
        )}
    </div>
    );
}
export default TeamList;