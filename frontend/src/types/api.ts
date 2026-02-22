export interface Deck {
  id: number
  name: string
  description: string
  created_at: string
}

export interface Card {
  id: number
  name: string
  number: number
  arcana: 'major' | 'minor'
  suit: string | null
  keywords_upright: string[]
  keywords_reversed: string[]
  meaning_upright: string
  meaning_reversed: string
  image_filename: string
}

export interface SpreadPosition {
  id: number
  position_number: number
  name: string
  description: string
  thematic_note: string
}

export interface Spread {
  id: number
  name: string
  description: string
  num_cards: number
  positions: SpreadPosition[]
}

export interface ReadingCard {
  id: number
  card: Card
  position: SpreadPosition
  is_reversed: boolean
  interpretation: string
}

export interface Reading {
  id: number
  deck: Deck
  spread: Spread
  question: string
  created_at: string
  cards: ReadingCard[]
}
