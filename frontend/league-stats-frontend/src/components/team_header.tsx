import { Link, useLocation } from "react-router-dom";
import "../styles/team_header.css"

function TeamHeader() {
    const location = useLocation();
    const params = new URLSearchParams(location.search);
    const id = params.get("id");

    return (
        <div className="team-header">
            <nav className="team-header-nav">
                <Link to={`/team?id=${id}`} className="nav-link">General Stats</Link>
                <Link to={`/team_betting?id=${id}`} className="nav-link">Betting Stats</Link>
            </nav>
        </div>
    );
}

export default TeamHeader;