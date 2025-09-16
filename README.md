# League Stats Project

This project is my sandbox for technology, built off of a stat scraper i've wrestled with over the last hald year.

## File Structure (Key Folders)

```
league-stats-frontend/
    src/
        components/         # Reusable React components (tables, headers, etc.)
        pages/              # Main pages (team stats, team list, betting stats)
        styles/             # CSS stylesheets for the frontend
    public/                 # Static assets
    App.tsx                 # Main React app entry

scraper/
    asset_scraper/          # Champion and asset scraping utilities
    match_scraper/          # Match data scraping and CSVs
    schedule_scraper/       # Schedule scraping logic
    web_connections/        # Web connectors for various data sources
    scraper_controller.py   # Main scraper orchestration logic

stat_calc/
    team_stats.py           # Team stats calculation logic
    betting_stats.py        # Betting stats calculation logic
    champion_stats.py       # Champion stats logic
    predict_kills.py        # Kill prediction logic

flask_server/
    app.py                  # Flask app entry point
    static/                 # Static files for Flask (CSS, JS)
    templates/              # HTML templates for Flask

database/
    models.py               # SQLAlchemy models
    team_db.py              # Team database utilities
    player_db.py            # Player database utilities
    asset_db.py             # Asset database utilities
    db_utils.py             # General DB utilities
```

---

## How to run



---

## Todo List
[] Create Pages for games, players stored in database
[] Create a page for poisson kill modeling
[] Throw draft stats into an AI

---

