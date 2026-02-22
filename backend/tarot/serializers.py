from rest_framework import serializers
from .models import Deck, Card, Spread, SpreadPosition, Reading, ReadingCard


class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ['id', 'name', 'description', 'created_at']


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            'id', 'name', 'number', 'arcana', 'suit',
            'keywords_upright', 'keywords_reversed',
            'meaning_upright', 'meaning_reversed',
            'image_filename',
        ]


class SpreadPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpreadPosition
        fields = ['id', 'position_number', 'name', 'description', 'thematic_note']


class SpreadSerializer(serializers.ModelSerializer):
    positions = SpreadPositionSerializer(many=True, read_only=True)

    class Meta:
        model = Spread
        fields = ['id', 'name', 'description', 'num_cards', 'positions']


class ReadingCardSerializer(serializers.ModelSerializer):
    card = CardSerializer(read_only=True)
    position = SpreadPositionSerializer(read_only=True)

    class Meta:
        model = ReadingCard
        fields = ['id', 'card', 'position', 'is_reversed', 'interpretation']


class ReadingSerializer(serializers.ModelSerializer):
    deck = DeckSerializer(read_only=True)
    spread = SpreadSerializer(read_only=True)
    cards = ReadingCardSerializer(many=True, read_only=True)

    class Meta:
        model = Reading
        fields = ['id', 'deck', 'spread', 'question', 'created_at', 'cards']


class ReadingCreateSerializer(serializers.Serializer):
    deck_id = serializers.IntegerField()
    spread_id = serializers.IntegerField()
    question = serializers.CharField(max_length=1000)

    def validate_deck_id(self, value):
        if not Deck.objects.filter(id=value).exists():
            raise serializers.ValidationError('Deck not found.')
        return value

    def validate_spread_id(self, value):
        if not Spread.objects.filter(id=value).exists():
            raise serializers.ValidationError('Spread not found.')
        return value

    def validate(self, data):
        deck = Deck.objects.get(id=data['deck_id'])
        spread = Spread.objects.get(id=data['spread_id'])
        card_count = deck.cards.count()
        if card_count < spread.num_cards:
            raise serializers.ValidationError(
                f'Deck "{deck.name}" has {card_count} cards but spread '
                f'"{spread.name}" requires {spread.num_cards}.'
            )
        return data
