from django.contrib import admin
from .models import Deck, Card, Spread, SpreadPosition, Reading, ReadingCard


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'arcana', 'suit', 'number', 'deck')
    list_filter = ('arcana', 'suit', 'deck')
    search_fields = ('name',)
    ordering = ('arcana', 'suit', 'number')


@admin.register(Spread)
class SpreadAdmin(admin.ModelAdmin):
    list_display = ('name', 'num_cards')


class SpreadPositionInline(admin.TabularInline):
    model = SpreadPosition
    extra = 0


@admin.register(SpreadPosition)
class SpreadPositionAdmin(admin.ModelAdmin):
    list_display = ('spread', 'position_number', 'name')
    list_filter = ('spread',)


class ReadingCardInline(admin.TabularInline):
    model = ReadingCard
    extra = 0
    readonly_fields = ('card', 'position', 'is_reversed', 'interpretation')


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ('id', 'deck', 'spread', 'created_at', 'question_preview')
    list_filter = ('deck', 'spread')
    inlines = [ReadingCardInline]

    def question_preview(self, obj):
        return obj.question[:60] + '…' if len(obj.question) > 60 else obj.question
    question_preview.short_description = 'Question'


@admin.register(ReadingCard)
class ReadingCardAdmin(admin.ModelAdmin):
    list_display = ('reading', 'card', 'position', 'is_reversed')
    list_filter = ('is_reversed', 'position__spread')
