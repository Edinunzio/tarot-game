import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { fetchReading } from '../services/api'
import type { Reading } from '../types/api'
import CardSlot from '../components/CardSlot'

export default function ReadingPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [reading, setReading] = useState<Reading | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [flipped, setFlipped] = useState<Set<number>>(new Set())

  useEffect(() => {
    if (!id) return
    fetchReading(Number(id))
      .then(r => {
        setReading(r)
        setLoading(false)
      })
      .catch(() => {
        setError('Could not load this reading.')
        setLoading(false)
      })
  }, [id])

  const flipCard = (positionNumber: number) => {
    setFlipped(prev => new Set(prev).add(positionNumber))
  }

  const revealAll = () => {
    if (!reading) return
    setFlipped(new Set(reading.cards.map(c => c.position.position_number)))
  }

  if (loading) {
    return (
      <Screen>
        <p className="text-gray-500 tracking-widest animate-pulse text-sm">Reading the cards...</p>
      </Screen>
    )
  }

  if (error || !reading) {
    return (
      <Screen>
        <p className="text-red-500 text-sm">{error || 'Reading not found.'}</p>
        <button
          onClick={() => navigate('/')}
          className="mt-4 text-gray-600 hover:text-gray-400 text-sm underline"
        >
          Start over
        </button>
      </Screen>
    )
  }

  const sortedCards = [...reading.cards].sort(
    (a, b) => a.position.position_number - b.position.position_number
  )
  const allFlipped = sortedCards.every(c => flipped.has(c.position.position_number))

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 px-6 py-12">
      <div className="max-w-5xl mx-auto">

        {/* Question header */}
        <div className="text-center mb-14">
          <p className="text-gray-600 text-xs tracking-widest uppercase mb-3">You asked</p>
          <p className="text-gray-200 text-xl italic max-w-2xl mx-auto leading-relaxed">
            "{reading.question}"
          </p>
          <p className="text-gray-700 text-xs mt-3">
            {reading.spread.name} · {reading.deck.name}
          </p>
        </div>

        {/* Cards */}
        <div className="flex flex-col md:flex-row gap-10 justify-center items-start mb-12">
          {sortedCards.map(rc => (
            <CardSlot
              key={rc.id}
              readingCard={rc}
              isFlipped={flipped.has(rc.position.position_number)}
              onFlip={() => flipCard(rc.position.position_number)}
            />
          ))}
        </div>

        {/* Actions */}
        <div className="flex justify-center gap-6">
          {!allFlipped && (
            <button
              onClick={revealAll}
              className="text-gray-600 hover:text-gray-400 text-sm underline transition-colors"
            >
              Reveal all
            </button>
          )}
          <button
            onClick={() => navigate('/')}
            className="bg-gray-900 hover:bg-gray-800 text-gray-400 hover:text-gray-200 text-sm py-2 px-6 rounded-lg transition-colors border border-gray-800"
          >
            New Reading
          </button>
        </div>

      </div>
    </div>
  )
}

function Screen({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center p-6 gap-2">
      {children}
    </div>
  )
}
