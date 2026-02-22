"""
Shuffling algorithms that simulate physical card handling.

A "deck" throughout this module is a list of dicts:
    [{'card_id': int, 'is_reversed': bool}, ...]

All functions return a new list and do not mutate the input.
"""
import random


def overhand_shuffle(deck: list[dict]) -> list[dict]:
    """
    One overhand shuffle pass — the most common real-world method.

    Simulates taking small packets from the top of the right-hand pile
    and dropping them onto the front of the left-hand pile, so earlier
    packets end up deeper in the result.

    ~20% chance per packet that it gets physically flipped, reversing
    both the card orientations within it and their order.
    """
    source = list(deck)
    destination: list[dict] = []

    while source:
        chunk_size = random.randint(3, 12)
        chunk = source[:chunk_size]
        source = source[chunk_size:]

        if random.random() < 0.20:
            # Flip the whole packet: reverse order + toggle each card's orientation
            chunk = [
                {'card_id': c['card_id'], 'is_reversed': not c['is_reversed']}
                for c in reversed(chunk)
            ]

        destination = chunk + destination

    return destination


def riffle_shuffle(deck: list[dict]) -> list[dict]:
    """
    One riffle shuffle pass.

    Splits the deck roughly in half (±5 card variance), then interleaves
    the two halves with weighted randomness — not a perfect alternation,
    which is physically unrealistic anyway.
    """
    if len(deck) < 4:
        return list(deck)

    mid = len(deck) // 2
    variance = random.randint(-5, 5)
    split = max(1, min(len(deck) - 1, mid + variance))

    left = list(deck[:split])
    right = list(deck[split:])
    result: list[dict] = []

    while left and right:
        # Weight toward the larger pile — that's where thumbs slip first
        if random.random() < len(left) / (len(left) + len(right)):
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))

    result.extend(left)
    result.extend(right)
    return result


def cut(deck: list[dict]) -> list[dict]:
    """
    Cut the deck at a random point in the middle 35–65% range.
    The bottom portion moves to the top.
    """
    if len(deck) < 4:
        return list(deck)

    lo = int(len(deck) * 0.35)
    hi = int(len(deck) * 0.65)
    cut_point = random.randint(lo, hi)
    return deck[cut_point:] + deck[:cut_point]


def full_shuffle(deck: list[dict]) -> list[dict]:
    """
    Composite shuffle sequence that mimics a realistic hand-shuffle ritual:

        overhand × 5  →  riffle × 2  →  cut  →  overhand × 2  →  cut

    Returns the shuffled deck.
    """
    result = list(deck)

    for _ in range(5):
        result = overhand_shuffle(result)
    for _ in range(2):
        result = riffle_shuffle(result)
    result = cut(result)
    for _ in range(2):
        result = overhand_shuffle(result)
    result = cut(result)

    return result


def build_deck(cards) -> list[dict]:
    """
    Convert a queryset of Card objects into the shuffle-ready list format.
    All cards start upright; the shuffle algorithms introduce reversals.
    """
    return [{'card_id': card.id, 'is_reversed': False} for card in cards]
