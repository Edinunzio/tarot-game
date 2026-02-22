from django.db import models
from django.contrib.postgres.fields import ArrayField


class Deck(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    ARCANA_MAJOR = 'major'
    ARCANA_MINOR = 'minor'
    ARCANA_CHOICES = [(ARCANA_MAJOR, 'Major'), (ARCANA_MINOR, 'Minor')]

    SUIT_WANDS = 'wands'
    SUIT_CUPS = 'cups'
    SUIT_SWORDS = 'swords'
    SUIT_PENTACLES = 'pentacles'
    SUIT_CHOICES = [
        (SUIT_WANDS, 'Wands'),
        (SUIT_CUPS, 'Cups'),
        (SUIT_SWORDS, 'Swords'),
        (SUIT_PENTACLES, 'Pentacles'),
    ]

    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')
    name = models.CharField(max_length=200)
    number = models.IntegerField()
    arcana = models.CharField(max_length=10, choices=ARCANA_CHOICES)
    suit = models.CharField(max_length=20, choices=SUIT_CHOICES, blank=True, null=True)
    keywords_upright = ArrayField(models.CharField(max_length=100), default=list)
    keywords_reversed = ArrayField(models.CharField(max_length=100), default=list)
    meaning_upright = models.TextField()
    meaning_reversed = models.TextField()
    image_filename = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['arcana', 'suit', 'number']

    def __str__(self):
        return f'{self.name} ({self.deck.name})'


class Spread(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    num_cards = models.IntegerField()

    def __str__(self):
        return self.name


class SpreadPosition(models.Model):
    spread = models.ForeignKey(Spread, on_delete=models.CASCADE, related_name='positions')
    position_number = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    thematic_note = models.TextField(blank=True)

    class Meta:
        ordering = ['position_number']
        unique_together = ('spread', 'position_number')

    def __str__(self):
        return f'{self.spread.name} — {self.name}'


class Reading(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.PROTECT)
    spread = models.ForeignKey(Spread, on_delete=models.PROTECT)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reading {self.id} ({self.created_at:%Y-%m-%d})'


class ReadingCard(models.Model):
    reading = models.ForeignKey(Reading, on_delete=models.CASCADE, related_name='cards')
    card = models.ForeignKey(Card, on_delete=models.PROTECT)
    position = models.ForeignKey(SpreadPosition, on_delete=models.PROTECT)
    is_reversed = models.BooleanField(default=False)
    interpretation = models.TextField(blank=True)

    class Meta:
        unique_together = ('reading', 'position')

    def __str__(self):
        orientation = 'reversed' if self.is_reversed else 'upright'
        return f'{self.card.name} ({orientation}) at {self.position.name}'
