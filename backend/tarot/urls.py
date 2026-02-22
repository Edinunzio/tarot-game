from django.urls import path
from .views import DeckListView, SpreadListView, ReadingCreateView, ReadingDetailView

urlpatterns = [
    path('decks/', DeckListView.as_view(), name='deck-list'),
    path('spreads/', SpreadListView.as_view(), name='spread-list'),
    path('readings/', ReadingCreateView.as_view(), name='reading-create'),
    path('readings/<int:pk>/', ReadingDetailView.as_view(), name='reading-detail'),
]
