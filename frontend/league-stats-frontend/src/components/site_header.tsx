import { Link } from "react-router-dom";
import "../styles/site_header.css"

function SiteHeader() {


    return (
        <div className="site-header">
            <nav className="site-header-nav">
                <Link to={`/teams`} className="nav-link">Teams</Link>
            </nav>
        </div>
    );
}

export default SiteHeader;