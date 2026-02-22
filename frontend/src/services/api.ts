import type { Deck, Spread, Reading } from '../types/api'

const BASE = '/api'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, options)
  if (!res.ok) {
    const body = await res.text()
    throw new Error(`${res.status} ${res.statusText}: ${body}`)
  }
  return res.json() as Promise<T>
}

export function fetchDecks(): Promise<Deck[]> {
  return request('/decks/')
}

export function fetchSpreads(): Promise<Spread[]> {
  return request('/spreads/')
}

export function createReading(params: {
  deck_id: number
  spread_id: number
  question: string
}): Promise<Reading> {
  return request('/readings/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params),
  })
}

export function fetchReading(id: number): Promise<Reading> {
  return request(`/readings/${id}/`)
}
