import type { ReadingCard } from '../types/api'

interface CardSlotProps {
  readingCard: ReadingCard
  isFlipped: boolean
  onFlip: () => void
}

export default function CardSlot({ readingCard, isFlipped, onFlip }: CardSlotProps) {
  const { card, position, is_reversed, interpretation } = readingCard
  const keywords = is_reversed ? card.keywords_reversed : card.keywords_upright

  return (
    <div className="flex flex-col items-center gap-5 flex-1 min-w-0 max-w-[240px]">

      {/* Position label */}
      <div className="text-center">
        <h3 className="text-purple-400 font-semibold tracking-widest text-xs uppercase">
          {position.name}
        </h3>
        <p className="text-gray-700 text-xs mt-1 leading-snug max-w-[180px]">
          {position.description}
        </p>
      </div>

      {/* Card */}
      <div
        className="card-wrapper"
        onClick={!isFlipped ? onFlip : undefined}
        style={{ cursor: isFlipped ? 'default' : 'pointer' }}
        title={isFlipped ? undefined : 'Click to reveal'}
      >
        <div className={`card-inner ${isFlipped ? 'flipped' : ''}`}>

          {/* ── Back (face-down) ── */}
          <div className="card-back bg-gradient-to-br from-indigo-950 via-purple-950 to-gray-950 border border-purple-900/40 flex flex-col items-center justify-center gap-3 group">
            <span className="text-purple-800 text-4xl group-hover:text-purple-700 transition-colors">✦</span>
            <span className="text-purple-900/70 text-[10px] tracking-[0.3em] uppercase">Tarot</span>
          </div>

          {/* ── Face (revealed) ── */}
          <div
            className={`card-face border flex flex-col p-4 gap-3 ${
              is_reversed
                ? 'bg-gray-900 border-rose-950/60'
                : 'bg-gray-900 border-purple-950/60'
            }`}
          >
            {/* Reversed badge */}
            {is_reversed && (
              <span className="text-rose-600 text-[10px] font-bold tracking-widest uppercase flex items-center gap-1">
                <span>↓</span> Reversed
              </span>
            )}

            {/* Card identity */}
            <div className="flex-1 flex flex-col justify-center gap-2">
              <h4 className="text-purple-200 font-bold text-base leading-tight">
                {card.name}
              </h4>
              <p className="text-gray-600 text-[10px] capitalize tracking-wide">
                {card.arcana === 'major'
                  ? 'Major Arcana'
                  : `${card.arcana} Arcana · ${card.suit}`}
              </p>
            </div>

            {/* Keywords */}
            {keywords.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {keywords.slice(0, 3).map(kw => (
                  <span
                    key={kw}
                    className="text-[10px] bg-gray-800 text-gray-500 px-2 py-0.5 rounded-full"
                  >
                    {kw}
                  </span>
                ))}
              </div>
            )}
          </div>

        </div>
      </div>

      {/* Interpretation — fades in after flip */}
      <div
        className={`text-sm text-gray-500 leading-relaxed border-l-2 border-purple-950 pl-4 py-1 transition-opacity duration-700 ${
          isFlipped ? 'opacity-100' : 'opacity-0 pointer-events-none'
        }`}
      >
        {interpretation}
      </div>

    </div>
  )
}
