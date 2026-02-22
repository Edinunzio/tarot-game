import { Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import ShufflePage from './pages/ShufflePage'
import ReadingPage from './pages/ReadingPage'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/shuffle" element={<ShufflePage />} />
      <Route path="/reading/:id" element={<ReadingPage />} />
    </Routes>
  )
}
