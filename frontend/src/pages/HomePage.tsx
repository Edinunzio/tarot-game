import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { fetchDecks, fetchSpreads } from '../services/api'
import type { Deck, Spread } from '../types/api'

export default function HomePage() {
  const navigate = useNavigate()
  const [decks, setDecks] = useState<Deck[]>([])
  const [spreads, setSpreads] = useState<Spread[]>([])
  const [question, setQuestion] = useState('')
  const [deckId, setDeckId] = useState<number | null>(null)
  const [spreadId, setSpreadId] = useState<number | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([fetchDecks(), fetchSpreads()])
      .then(([d, s]) => {
        setDecks(d)
        setSpreads(s)
        if (d.length > 0) setDeckId(d[0].id)
        if (s.length > 0) setSpreadId(s[0].id)
        setLoading(false)
      })
      .catch(() => {
        setError('Could not reach the server. Is the backend running?')
        setLoading(false)
      })
  }, [])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!question.trim() || !deckId || !spreadId) return
    navigate('/shuffle', { state: { deckId, spreadId, question: question.trim() } })
  }

  if (loading) {
    return (
      <Screen>
        <p className="text-gray-500 tracking-widest animate-pulse text-sm">Loading...</p>
      </Screen>
    )
  }

  if (error) {
    return (
      <Screen>
        <p className="text-red-500 text-sm">{error}</p>
      </Screen>
    )
  }

  return (
    <Screen>
      <div className="w-full max-w-md">
        <div className="text-center mb-10">
          <h1 className="text-5xl font-bold text-purple-300 tracking-widest mb-3">✦ TAROT ✦</h1>
          <p className="text-gray-600 text-xs tracking-widest uppercase">Ask, and the cards will answer</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-gray-500 text-xs mb-2 tracking-widest uppercase">
              Your Question
            </label>
            <textarea
              value={question}
              onChange={e => setQuestion(e.target.value)}
              placeholder="What guidance do you seek?"
              rows={3}
              className="w-full bg-gray-900 border border-gray-800 rounded-lg p-3 text-gray-200 placeholder-gray-700 focus:outline-none focus:border-purple-800 resize-none transition-colors"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-gray-500 text-xs mb-2 tracking-widest uppercase">Deck</label>
              <select
                value={deckId ?? ''}
                onChange={e => setDeckId(Number(e.target.value))}
                className="w-full bg-gray-900 border border-gray-800 rounded-lg p-3 text-gray-200 focus:outline-none focus:border-purple-800 transition-colors"
              >
                {decks.map(d => (
                  <option key={d.id} value={d.id}>{d.name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-gray-500 text-xs mb-2 tracking-widest uppercase">Spread</label>
              <select
                value={spreadId ?? ''}
                onChange={e => setSpreadId(Number(e.target.value))}
                className="w-full bg-gray-900 border border-gray-800 rounded-lg p-3 text-gray-200 focus:outline-none focus:border-purple-800 transition-colors"
              >
                {spreads.map(s => (
                  <option key={s.id} value={s.id}>{s.name}</option>
                ))}
              </select>
            </div>
          </div>

          <button
            type="submit"
            disabled={!question.trim() || !deckId || !spreadId}
            className="w-full bg-purple-900 hover:bg-purple-800 disabled:opacity-30 disabled:cursor-not-allowed text-purple-100 font-semibold py-3 px-6 rounded-lg tracking-widest text-sm uppercase transition-colors mt-2"
          >
            Begin Reading
          </button>
        </form>
      </div>
    </Screen>
  )
}

function Screen({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center p-6">
      {children}
    </div>
  )
}
