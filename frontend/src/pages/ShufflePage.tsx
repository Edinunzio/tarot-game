import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { createReading } from '../services/api'

interface LocationState {
  deckId: number
  spreadId: number
  question: string
}

// Static per-card rotations so the stack looks like a real pile
const CARD_ROTATIONS = [-6, -3, 0, 3, 6]

export default function ShufflePage() {
  const navigate = useNavigate()
  const location = useLocation()
  const state = location.state as LocationState | null

  const [phase, setPhase] = useState<'shuffling' | 'ready' | 'loading'>('shuffling')
  const [error, setError] = useState('')

  // Guard: if arrived without state, send home
  useEffect(() => {
    if (!state?.deckId) {
      navigate('/', { replace: true })
    }
  }, [])

  // After 2.8s of animation, show the cut button
  useEffect(() => {
    if (phase !== 'shuffling') return
    const t = setTimeout(() => setPhase('ready'), 2800)
    return () => clearTimeout(t)
  }, [phase])

  const handleCut = async () => {
    if (!state) return
    setPhase('loading')
    setError('')
    try {
      const reading = await createReading({
        deck_id: state.deckId,
        spread_id: state.spreadId,
        question: state.question,
      })
      navigate(`/reading/${reading.id}`)
    } catch {
      setError('Something went wrong. Please try again.')
      setPhase('ready')
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center gap-12 p-6">
      {/* Card stack */}
      <div className="relative w-40 h-[268px]">
        {CARD_ROTATIONS.map((rot, i) => (
          <div
            key={i}
            className={`absolute inset-0 bg-gradient-to-br from-indigo-950 via-purple-950 to-gray-900 border border-purple-900/50 rounded-lg ${phase === 'shuffling' ? 'shuffle-card' : ''}`}
            style={{
              '--r': `${rot}deg`,
              transform: `rotate(${rot}deg)`,
              zIndex: i,
              animationDelay: `${i * 0.15}s`,
            } as React.CSSProperties}
          >
            <div className="flex items-center justify-center h-full select-none">
              <span className="text-purple-900/60 text-3xl">✦</span>
            </div>
          </div>
        ))}
      </div>

      {/* Status and action */}
      <div className="text-center space-y-6 min-h-[80px] flex flex-col items-center justify-center">
        {phase === 'shuffling' && (
          <p className="text-purple-500 text-sm tracking-widest uppercase animate-pulse">
            Shuffling the deck...
          </p>
        )}

        {phase === 'ready' && (
          <>
            <p className="text-gray-600 text-sm tracking-wide">The deck is ready for you.</p>
            <button
              onClick={handleCut}
              className="bg-purple-900 hover:bg-purple-800 text-purple-100 font-semibold py-3 px-10 rounded-lg tracking-widest text-sm uppercase transition-colors"
            >
              Cut the Deck
            </button>
          </>
        )}

        {phase === 'loading' && (
          <p className="text-purple-500 text-sm tracking-widest uppercase animate-pulse">
            Reading the cards...
          </p>
        )}

        {error && (
          <p className="text-red-500 text-xs">{error}</p>
        )}
      </div>

      {/* Back link */}
      <button
        onClick={() => navigate('/')}
        className="absolute top-6 left-6 text-gray-700 hover:text-gray-500 text-sm transition-colors"
      >
        ← Back
      </button>
    </div>
  )
}
