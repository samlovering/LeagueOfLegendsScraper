import { Routes, Route, } from 'react-router-dom'

import './App.css'
import TeamStatsPage from './pages/team_stats'
import TeamList from './pages/teams'
import SiteHeader from './components/site_header'
import TeamBettingPage from './pages/team_betting_stats'

function App() {

  return (
    <>
    <SiteHeader />
      <Routes>
        <Route path="/" element={<TeamList />} />
        <Route path="/teams" element={<TeamList />} />
        <Route path="/team" element={<TeamStatsPage />} />
        <Route path="/team_betting" element={<TeamBettingPage />} />
      </Routes>
      
    </>
  )
}

export default App
