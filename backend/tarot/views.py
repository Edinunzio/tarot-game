from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Deck, Card, Spread, Reading, ReadingCard
from .serializers import (
    DeckSerializer,
    SpreadSerializer,
    ReadingSerializer,
    ReadingCreateSerializer,
)
from .shuffle import build_deck, full_shuffle


class DeckListView(ListAPIView):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer


class SpreadListView(ListAPIView):
    queryset = Spread.objects.prefetch_related('positions').all()
    serializer_class = SpreadSerializer


class ReadingCreateView(APIView):
    """
    POST /api/readings/
    Body: { deck_id, spread_id, question }

    Shuffles the deck, draws cards for the spread, generates stub
    interpretations, persists everything, and returns the full reading.
    """

    def post(self, request):
        create_serializer = ReadingCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = create_serializer.validated_data
        deck = Deck.objects.get(id=data['deck_id'])
        spread = Spread.objects.prefetch_related('positions').get(id=data['spread_id'])

        # Build and shuffle the deck
        cards = list(deck.cards.all())
        shuffled = full_shuffle(build_deck(cards))

        # Map card_id → Card object for quick lookup
        card_map = {card.id: card for card in cards}

        # Draw one card per spread position
        positions = list(spread.positions.all())  # already ordered by position_number
        drawn = shuffled[:spread.num_cards]

        # Persist
        reading = Reading.objects.create(
            deck=deck,
            spread=spread,
            question=data['question'],
        )

        for position, drawn_card in zip(positions, drawn):
            card_obj = card_map[drawn_card['card_id']]
            is_reversed = drawn_card['is_reversed']
            interpretation = _stub_interpretation(card_obj, position, is_reversed)
            ReadingCard.objects.create(
                reading=reading,
                card=card_obj,
                position=position,
                is_reversed=is_reversed,
                interpretation=interpretation,
            )

        reading_serializer = ReadingSerializer(reading)
        return Response(reading_serializer.data, status=status.HTTP_201_CREATED)


class ReadingDetailView(RetrieveAPIView):
    queryset = Reading.objects.prefetch_related(
        'cards__card',
        'cards__position',
    ).select_related('deck', 'spread')
    serializer_class = ReadingSerializer


# ---------------------------------------------------------------------------
# Interpretation stub
# ---------------------------------------------------------------------------

def _stub_interpretation(card, position, is_reversed: bool) -> str:
    """
    Template-based interpretation stored at reading creation time.
    Replaced by LLM output in Phase 6.
    """
    orientation = 'reversed' if is_reversed else 'upright'
    keywords = card.keywords_reversed if is_reversed else card.keywords_upright
    meaning = card.meaning_reversed if is_reversed else card.meaning_upright
    keyword_str = ', '.join(keywords[:3]) if keywords else ''

    parts = [
        f"{card.name} appears {orientation} in the {position.name} position "
        f"— {position.description.lower().rstrip('.')}.",
    ]
    if keyword_str:
        parts.append(f"Key themes: {keyword_str}.")
    parts.append(meaning)
    if position.thematic_note:
        parts.append(position.thematic_note)

    return ' '.join(parts)
