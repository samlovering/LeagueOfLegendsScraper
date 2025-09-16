$(document).ready(function() {
    //Get Leagues for drop down.
    $.ajax({
        url: '/api/getLeagues',
        method:'GET',
        dataType:'json',
        success: function(leagues){
            if(leagues.error){
                console.error(leagues.error);
                return;
            }
            $(document).ready(function() {
                const leagueSelect = $("#league-select");
                leagueSelect.append($("<option>", {
                    value: "Select a League",
                    text: "Select a League",
                    selected: true,
                    disabled: true
                }));
                leagues.forEach(league => {
                    leagueSelect.append($('<option>',{
                        value: league,
                        text: league
                    }));
                });
            });
        }
    });
    $('#league-select').on('change', function() {
        const selectedLeague = $(this).val();
        if (!selectedLeague) {
            $('#datatable').hide();
            return;
        }
        $.ajax({
            url: '/api/getBettingStatsForLeague',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({league: selectedLeague}),
            success: function(bettingStats){
                const tbody = $('#datatable tbody')
                tbody.empty();
                bettingStats.forEach(team_stats => {
                    tbody.append(`
                        <tr>
                            <td>${team_stats.team_name}</td>
                            <td>${team_stats.num_games}</td>
                            <td>${(team_stats.win_rate * 100).toFixed(2)}%</td>
                            <td>${Math.floor(team_stats.avg_length / 60)}:${Math.floor(team_stats.avg_length % 60).toString().padStart(2, '0')}</td>
                            <td>${(team_stats.first_blood_pct * 100).toFixed(2)}%</td>
                            <td>${(team_stats.first_herald_pct * 100).toFixed(2)}%</td>
                            <td>${(team_stats.first_tower_pct * 100).toFixed(2)}%</td>
                            <td>${(team_stats.first_dragon_pct * 100).toFixed(2)}%</td>
                            <td>${(team_stats.first_baron_pct * 100).toFixed(2)}%</td>
                            <td>${parseFloat(team_stats.avg_kills || 0).toFixed(2)}</td>
                            <td>${parseFloat(team_stats.avg_deaths || 0).toFixed(2)}</td>
                            <td>${parseFloat(team_stats.avg_gold || 0).toFixed(2)}</td>
                            <td>${parseFloat(team_stats.c_kills || 0).toFixed(2)}</td>
                            <td>${parseFloat(team_stats.c_gold || 0).toFixed(2)}</td>
                            <td>${parseFloat(team_stats.c_dragons || 0).toFixed(2)}</td>
                            <td>${parseFloat(team_stats.c_towers || 0).toFixed(2)}</td>
                            <td>${parseFloat(team_stats.c_barons || 0).toFixed(2)}</td>
                            <td>${(team_stats.kills_over23 * 100).toFixed(2)}%</td>
                            <td>${(team_stats.kills_over25 * 100).toFixed(2)}%</td>
                            <td>${(team_stats.kills_over27 * 100).toFixed(2)}%</td>
                            <td>${(team_stats.kills_over29 * 100).toFixed(2)}%</td>
                            <td>${(team_stats.towers_over10 * 100).toFixed(2)}%</td>
                            <td>${(team_stats.towers_over11 * 100).toFixed(2)}%</td>
                            <td>${(team_stats.towers_over12 * 100).toFixed(2)}%</td>
                            <td>${(team_stats.dragons_over4 * 100).toFixed(2)}%</td>
                            <td>${(team_stats.dragons_over5 * 100).toFixed(2)}%</td>
                            <td>${(team_stats.barons_over1 * 100).toFixed(2)}%</td>
                            <td>${(team_stats.inhibitors_over1 * 100).toFixed(2)}%</td>
                        </tr>
                    `)
                })
                $('#datatable').show();
            },
            error: function(xhr, status, error) {
                console.error('Error fetching games:', error);
            }
        })
    })
})