"""
Seed the database with the Rider-Waite deck (78 cards) and the
Three Card spread (Past / Present / Future).

Usage:
    docker compose exec backend python manage.py seed_deck
    docker compose exec backend python manage.py seed_deck --clear
"""
from django.core.management.base import BaseCommand
from tarot.models import Deck, Card, Spread, SpreadPosition


# ---------------------------------------------------------------------------
# Card data
# ---------------------------------------------------------------------------

MAJOR_ARCANA = [
    {
        'name': 'The Fool',
        'number': 0,
        'keywords_upright': ['beginnings', 'spontaneity', 'free spirit', 'innocence'],
        'keywords_reversed': ['recklessness', 'poor judgment', 'naivety'],
        'meaning_upright': (
            'New beginnings, optimism, and trust in life. The Fool invites you to take '
            'a leap of faith into the unknown with an open heart and beginner\'s mind.'
        ),
        'meaning_reversed': (
            'Recklessness or poor judgment — rushing forward without considering '
            'consequences. Check whether naivety is leaving you vulnerable.'
        ),
    },
    {
        'name': 'The Magician',
        'number': 1,
        'keywords_upright': ['manifestation', 'resourcefulness', 'power', 'action'],
        'keywords_reversed': ['manipulation', 'poor planning', 'untapped talents'],
        'meaning_upright': (
            'You have the tools, skills, and willpower to manifest your desires. '
            'This is a time of inspired action — channel your energy with focus.'
        ),
        'meaning_reversed': (
            'Talents going unused, or power being applied deceptively. '
            'Revisit your intentions and ensure your actions align with your values.'
        ),
    },
    {
        'name': 'The High Priestess',
        'number': 2,
        'keywords_upright': ['intuition', 'sacred knowledge', 'subconscious', 'mystery'],
        'keywords_reversed': ['secrets', 'disconnected intuition', 'repressed feelings'],
        'meaning_upright': (
            'Trust your inner knowing. The High Priestess urges stillness and '
            'attunement to the subtle — look beneath the surface.'
        ),
        'meaning_reversed': (
            'Important information is hidden or you are not listening to your '
            'intuition. Slow down and allow deeper wisdom to surface.'
        ),
    },
    {
        'name': 'The Empress',
        'number': 3,
        'keywords_upright': ['abundance', 'femininity', 'nurturing', 'nature', 'creativity'],
        'keywords_reversed': ['creative block', 'dependence', 'smothering'],
        'meaning_upright': (
            'Abundance, fertility, and creative expression. A time of growth, '
            'beauty, and nurturing — both of others and of yourself.'
        ),
        'meaning_reversed': (
            'Creative blocks or over-dependence on others. Examine whether you '
            'are neglecting your own needs or stifling those around you.'
        ),
    },
    {
        'name': 'The Emperor',
        'number': 4,
        'keywords_upright': ['authority', 'structure', 'stability', 'fatherhood'],
        'keywords_reversed': ['domination', 'excessive control', 'rigidity', 'inflexibility'],
        'meaning_upright': (
            'Stability through structure and authority. The Emperor represents '
            'the power of discipline, planning, and fatherly protection.'
        ),
        'meaning_reversed': (
            'Authority wielded too harshly, or an unwillingness to adapt. '
            'Where is rigidity creating resistance rather than security?'
        ),
    },
    {
        'name': 'The Hierophant',
        'number': 5,
        'keywords_upright': ['tradition', 'spiritual wisdom', 'conformity', 'institution'],
        'keywords_reversed': ['personal beliefs', 'challenging convention', 'freedom'],
        'meaning_upright': (
            'Established traditions and spiritual guidance. A teacher, mentor, or '
            'institution offers wisdom worth receiving with discernment.'
        ),
        'meaning_reversed': (
            'Questioning authority and forging your own spiritual path. '
            'It may be time to release rules that no longer serve you.'
        ),
    },
    {
        'name': 'The Lovers',
        'number': 6,
        'keywords_upright': ['love', 'harmony', 'alignment', 'choices', 'partnership'],
        'keywords_reversed': ['disharmony', 'imbalance', 'misaligned values', 'avoidance'],
        'meaning_upright': (
            'Deep connection, aligned values, and meaningful choices. '
            'Love in its many forms — romantic, platonic, or self-directed.'
        ),
        'meaning_reversed': (
            'Disharmony or a misalignment between your actions and your values. '
            'A choice may be avoided rather than faced honestly.'
        ),
    },
    {
        'name': 'The Chariot',
        'number': 7,
        'keywords_upright': ['willpower', 'determination', 'control', 'victory', 'focus'],
        'keywords_reversed': ['lack of direction', 'aggression', 'scattered energy'],
        'meaning_upright': (
            'Victory through focused will and self-discipline. You have the drive '
            'to overcome obstacles — harness opposing forces with confidence.'
        ),
        'meaning_reversed': (
            'Energy without direction, or force applied at the wrong target. '
            'Slow down to regain clarity before pressing forward.'
        ),
    },
    {
        'name': 'Strength',
        'number': 8,
        'keywords_upright': ['courage', 'compassion', 'inner strength', 'patience'],
        'keywords_reversed': ['self-doubt', 'weakness', 'insecurity', 'raw emotion'],
        'meaning_upright': (
            'Quiet strength through compassion and inner fortitude. True power '
            'comes not from force but from patience and gentle mastery.'
        ),
        'meaning_reversed': (
            'Self-doubt or allowing fear to undermine you. The strength you need '
            'is already within — reconnect with your courage.'
        ),
    },
    {
        'name': 'The Hermit',
        'number': 9,
        'keywords_upright': ['introspection', 'solitude', 'inner guidance', 'wisdom'],
        'keywords_reversed': ['isolation', 'loneliness', 'withdrawal', 'lost'],
        'meaning_upright': (
            'A period of reflection and soul-searching. Withdraw from noise to '
            'illuminate your path with the light of inner wisdom.'
        ),
        'meaning_reversed': (
            'Isolation that has become unhealthy, or resistance to necessary '
            'solitude. Consider whether you are hiding or genuinely seeking.'
        ),
    },
    {
        'name': 'Wheel of Fortune',
        'number': 10,
        'keywords_upright': ['cycles', 'destiny', 'turning point', 'luck', 'karma'],
        'keywords_reversed': ['bad luck', 'resistance', 'breaking cycles', 'stagnation'],
        'meaning_upright': (
            'The wheel turns — a pivotal moment of change, often bringing good '
            'fortune. Embrace the cycle; what goes around comes around.'
        ),
        'meaning_reversed': (
            'Resisting inevitable change or being caught in a repeating pattern. '
            'What cycle are you perpetuating rather than transcending?'
        ),
    },
    {
        'name': 'Justice',
        'number': 11,
        'keywords_upright': ['fairness', 'truth', 'cause and effect', 'law', 'clarity'],
        'keywords_reversed': ['unfairness', 'dishonesty', 'lack of accountability'],
        'meaning_upright': (
            'Truth and fair consequence. Actions and their results are being '
            'weighed with clear eyes — honesty and integrity are called for.'
        ),
        'meaning_reversed': (
            'Injustice, dishonesty, or an unwillingness to accept accountability. '
            'Examine whether you are seeing a situation clearly.'
        ),
    },
    {
        'name': 'The Hanged Man',
        'number': 12,
        'keywords_upright': ['pause', 'surrender', 'new perspective', 'letting go'],
        'keywords_reversed': ['delays', 'stalling', 'resistance', 'martyrdom'],
        'meaning_upright': (
            'A voluntary pause that opens a new perspective. Surrender the need '
            'to act — profound insight comes from stillness and suspension.'
        ),
        'meaning_reversed': (
            'Delays caused by resistance, or using sacrifice as manipulation. '
            'Are you truly pausing for wisdom, or just stalling?'
        ),
    },
    {
        'name': 'Death',
        'number': 13,
        'keywords_upright': ['endings', 'transformation', 'transition', 'release'],
        'keywords_reversed': ['resistance to change', 'stagnation', 'clinging to the past'],
        'meaning_upright': (
            'A profound ending that makes way for transformation. Something must '
            'be released so that new growth can begin.'
        ),
        'meaning_reversed': (
            'Clinging to what has already ended, preventing necessary change. '
            'The transition is inevitable — resistance only prolongs the struggle.'
        ),
    },
    {
        'name': 'Temperance',
        'number': 14,
        'keywords_upright': ['balance', 'moderation', 'patience', 'purpose', 'flow'],
        'keywords_reversed': ['imbalance', 'excess', 'lack of patience', 'discord'],
        'meaning_upright': (
            'Harmonious blending and measured patience. You are being called to '
            'find the middle path and allow things to unfold in their own time.'
        ),
        'meaning_reversed': (
            'Excess or imbalance in some area of life. Identify where you are '
            'overdoing or underdoing, and recalibrate with care.'
        ),
    },
    {
        'name': 'The Devil',
        'number': 15,
        'keywords_upright': ['shadow self', 'attachment', 'addiction', 'restriction'],
        'keywords_reversed': ['release', 'reclaiming power', 'detachment', 'freedom'],
        'meaning_upright': (
            'Bondage to materialism, habit, or unhealthy patterns. The chains '
            'are often self-imposed — awareness is the first step to freedom.'
        ),
        'meaning_reversed': (
            'Breaking free from limiting patterns or reclaiming power from an '
            'addiction. Liberation is closer than it appears.'
        ),
    },
    {
        'name': 'The Tower',
        'number': 16,
        'keywords_upright': ['upheaval', 'sudden change', 'revelation', 'chaos', 'awakening'],
        'keywords_reversed': ['avoiding disaster', 'fear of change', 'delaying the inevitable'],
        'meaning_upright': (
            'A sudden, disruptive revelation that shatters false structures. '
            'Painful as it is, what falls was built on shaky ground.'
        ),
        'meaning_reversed': (
            'Resisting an inevitable collapse, or narrowly averting disaster. '
            'Examine what you are propping up that may need to fall.'
        ),
    },
    {
        'name': 'The Star',
        'number': 17,
        'keywords_upright': ['hope', 'faith', 'renewal', 'serenity', 'inspiration'],
        'keywords_reversed': ['despair', 'lack of faith', 'disconnection', 'discouragement'],
        'meaning_upright': (
            'Hope and healing after hardship. The Star shines with calm assurance '
            'that you are on the right path — trust the universe.'
        ),
        'meaning_reversed': (
            'Loss of faith or a sense of disconnection from your purpose. '
            'Even in darkness a star remains — look for the small lights.'
        ),
    },
    {
        'name': 'The Moon',
        'number': 18,
        'keywords_upright': ['illusion', 'fear', 'the unconscious', 'intuition', 'confusion'],
        'keywords_reversed': ['releasing fear', 'repressed emotions', 'inner confusion'],
        'meaning_upright': (
            'The realm of illusion, dreams, and unconscious fears. Things are not '
            'as they appear — navigate by intuition rather than logic.'
        ),
        'meaning_reversed': (
            'Fears surfacing from the unconscious, or confusion slowly clearing. '
            'Hidden truths are beginning to come to light.'
        ),
    },
    {
        'name': 'The Sun',
        'number': 19,
        'keywords_upright': ['joy', 'success', 'vitality', 'positivity', 'clarity'],
        'keywords_reversed': ['temporary sadness', 'inner child blocked', 'clouded optimism'],
        'meaning_upright': (
            'Radiant joy, success, and clarity. The Sun illuminates everything '
            'with warmth — celebrate, be present, let yourself shine.'
        ),
        'meaning_reversed': (
            'Joy is present but temporarily obscured. The clouds will pass; '
            'reconnect with your inner child and allow yourself to feel good.'
        ),
    },
    {
        'name': 'Judgement',
        'number': 20,
        'keywords_upright': ['rebirth', 'inner calling', 'absolution', 'awakening'],
        'keywords_reversed': ['self-doubt', 'ignoring the call', 'harsh self-judgment'],
        'meaning_upright': (
            'A profound awakening and the call to rise to a higher version of '
            'yourself. Forgive, release judgment, and answer your calling.'
        ),
        'meaning_reversed': (
            'Self-doubt or refusing to heed an important inner calling. '
            'Where are you judging yourself too harshly to move forward?'
        ),
    },
    {
        'name': 'The World',
        'number': 21,
        'keywords_upright': ['completion', 'integration', 'accomplishment', 'wholeness'],
        'keywords_reversed': ['incompletion', 'shortcuts', 'seeking closure', 'delays'],
        'meaning_upright': (
            'A cycle completed with full integration of its lessons. You stand '
            'at the culmination of a long journey — celebrate your wholeness.'
        ),
        'meaning_reversed': (
            'A cycle left incomplete, or taking shortcuts that skip necessary '
            'growth. What remains unresolved before you can move on?'
        ),
    },
]

# ---------------------------------------------------------------------------
# Minor Arcana helpers
# ---------------------------------------------------------------------------

MINOR_ARCANA = {
    'wands': [
        {
            'number': 1,
            'name': 'Ace of Wands',
            'keywords_upright': ['inspiration', 'creative spark', 'new opportunity', 'potential'],
            'keywords_reversed': ['delays', 'lack of passion', 'blocked creativity'],
            'meaning_upright': 'A burst of creative energy and the seed of a new venture. The spark is real — act on it.',
            'meaning_reversed': 'Creative blocks or delays dampening a promising start. The energy exists; find the blockage.',
        },
        {
            'number': 2,
            'name': 'Two of Wands',
            'keywords_upright': ['planning', 'future vision', 'decisions', 'discovery'],
            'keywords_reversed': ['fear of unknown', 'lack of planning', 'staying safe'],
            'meaning_upright': 'You have taken the first step and now survey the horizon. Bold planning and forward vision.',
            'meaning_reversed': 'Hesitation or fear of the unknown is preventing meaningful progress. Commit to a direction.',
        },
        {
            'number': 3,
            'name': 'Three of Wands',
            'keywords_upright': ['expansion', 'foresight', 'overseas opportunity', 'progress'],
            'keywords_reversed': ['delays', 'frustration', 'playing it safe', 'retreat'],
            'meaning_upright': 'Your plans are in motion and expanding beyond initial horizons. Watch for new opportunities.',
            'meaning_reversed': 'Expected progress is delayed or you are retreating rather than expanding. Reassess the plan.',
        },
        {
            'number': 4,
            'name': 'Four of Wands',
            'keywords_upright': ['celebration', 'harmony', 'homecoming', 'joy'],
            'keywords_reversed': ['lack of support', 'transition', 'personal milestone'],
            'meaning_upright': 'A time of celebration, stability, and coming home. Enjoy this moment of earned harmony.',
            'meaning_reversed': 'Celebrating alone or support is missing from a milestone. Find your own reasons for joy.',
        },
        {
            'number': 5,
            'name': 'Five of Wands',
            'keywords_upright': ['conflict', 'competition', 'tension', 'diversity of views'],
            'keywords_reversed': ['avoiding conflict', 'inner conflict', 'compromise'],
            'meaning_upright': 'Competing voices and friction. Healthy conflict can sharpen ideas — stay constructive.',
            'meaning_reversed': 'Conflict avoided or internalized. Address tension rather than letting it fester.',
        },
        {
            'number': 6,
            'name': 'Six of Wands',
            'keywords_upright': ['victory', 'public recognition', 'confidence', 'success'],
            'keywords_reversed': ['private achievement', 'self-doubt', 'fall from grace'],
            'meaning_upright': 'Recognition and victory after effort. Hold your head high — success is deserved.',
            'meaning_reversed': 'Success that goes unacknowledged, or confidence undermined by self-doubt. Own your wins.',
        },
        {
            'number': 7,
            'name': 'Seven of Wands',
            'keywords_upright': ['perseverance', 'defensive', 'challenge', 'competition'],
            'keywords_reversed': ['giving up', 'overwhelmed', 'ceding ground'],
            'meaning_upright': 'You hold the high ground but must defend it. Stand firm — perseverance will carry you through.',
            'meaning_reversed': 'Exhaustion leading to surrender. Consider whether the position is worth defending.',
        },
        {
            'number': 8,
            'name': 'Eight of Wands',
            'keywords_upright': ['movement', 'speed', 'swift action', 'news arriving'],
            'keywords_reversed': ['delays', 'frustration', 'resisting change', 'miscommunication'],
            'meaning_upright': 'Things are moving fast — exciting momentum and rapid developments. Act while the energy is high.',
            'meaning_reversed': 'Delays and frustrations stall fast-moving plans. Check for miscommunications or obstacles.',
        },
        {
            'number': 9,
            'name': 'Nine of Wands',
            'keywords_upright': ['resilience', 'persistence', 'last stand', 'courage'],
            'keywords_reversed': ['exhaustion', 'giving up', 'paranoia', 'stubbornness'],
            'meaning_upright': 'Battle-worn but still standing. One final push is needed — your resilience will see you through.',
            'meaning_reversed': 'Exhaustion has become paralyzing. Rest and reassess whether the battle remains worth fighting.',
        },
        {
            'number': 10,
            'name': 'Ten of Wands',
            'keywords_upright': ['burden', 'extra responsibility', 'hard work', 'completion'],
            'keywords_reversed': ['doing it alone', 'delegation needed', 'avoiding responsibility'],
            'meaning_upright': 'Carrying a heavy load near the finish line. The burden is temporary — set down what you can.',
            'meaning_reversed': 'Overwhelmed by responsibility or avoiding it entirely. Ask for help or redistribute the load.',
        },
        {
            'number': 11,
            'name': 'Page of Wands',
            'keywords_upright': ['inspiration', 'exploration', 'free spirit', 'discovery'],
            'keywords_reversed': ['immaturity', 'lack of direction', 'all talk no action'],
            'meaning_upright': 'Enthusiastic and curious energy around a new idea or creative pursuit. Explore freely.',
            'meaning_reversed': 'Inspiration without follow-through, or creative energy scattered. Focus the spark.',
        },
        {
            'number': 12,
            'name': 'Knight of Wands',
            'keywords_upright': ['action', 'adventure', 'passion', 'impulsiveness'],
            'keywords_reversed': ['haste', 'scattered energy', 'delays', 'frustration'],
            'meaning_upright': 'Charging forward with fire and passion. Bold action — but watch for impulsiveness.',
            'meaning_reversed': 'Energy without direction, or forward motion suddenly stalled. Slow down to recalibrate.',
        },
        {
            'number': 13,
            'name': 'Queen of Wands',
            'keywords_upright': ['courage', 'confidence', 'independence', 'warmth'],
            'keywords_reversed': ['self-doubt', 'jealousy', 'demanding', 'introverted'],
            'meaning_upright': 'Radiant, self-assured energy. Lead with confidence and warmth — you have what it takes.',
            'meaning_reversed': 'Self-doubt is dimming your natural fire. Reconnect with your inner confidence.',
        },
        {
            'number': 14,
            'name': 'King of Wands',
            'keywords_upright': ['leadership', 'vision', 'entrepreneur', 'bold action'],
            'keywords_reversed': ['impulsive', 'reckless', 'arrogant', 'ineffective'],
            'meaning_upright': 'Visionary leadership and entrepreneurial fire. Take the helm with bold, decisive authority.',
            'meaning_reversed': 'Vision without wisdom, or leadership driven by ego rather than purpose. Course-correct.',
        },
    ],
    'cups': [
        {
            'number': 1,
            'name': 'Ace of Cups',
            'keywords_upright': ['new love', 'compassion', 'creativity', 'emotional opening'],
            'keywords_reversed': ['self-love needed', 'emotional repression', 'blocked intuition'],
            'meaning_upright': 'An overflowing cup of love, compassion, and new emotional beginnings. Open your heart.',
            'meaning_reversed': 'Emotions blocked or turned inward. Self-love is the necessary first step.',
        },
        {
            'number': 2,
            'name': 'Two of Cups',
            'keywords_upright': ['partnership', 'mutual attraction', 'connection', 'unity'],
            'keywords_reversed': ['disharmony', 'break-up', 'imbalance', 'self-love'],
            'meaning_upright': 'Deep mutual connection and harmonious partnership. A bond of equals, freely chosen.',
            'meaning_reversed': 'Imbalance in a relationship, or a partnership coming undone. Examine the dynamic honestly.',
        },
        {
            'number': 3,
            'name': 'Three of Cups',
            'keywords_upright': ['celebration', 'friendship', 'community', 'joy'],
            'keywords_reversed': ['overindulgence', 'isolation', 'gossip', "three's a crowd"],
            'meaning_upright': 'Joyful celebration with friends and community. Revel in togetherness and shared happiness.',
            'meaning_reversed': 'Social excess or feeling excluded from a group. Find balance between connection and solitude.',
        },
        {
            'number': 4,
            'name': 'Four of Cups',
            'keywords_upright': ['meditation', 'contemplation', 'apathy', 'reevaluation'],
            'keywords_reversed': ['new awareness', 'missed opportunity', 'emerging from withdrawal'],
            'meaning_upright': 'Turning inward to reassess. Be careful not to miss an offered cup while lost in contemplation.',
            'meaning_reversed': 'Emerging from introspection to notice what was previously overlooked. A new perspective opens.',
        },
        {
            'number': 5,
            'name': 'Five of Cups',
            'keywords_upright': ['grief', 'regret', 'disappointment', 'loss'],
            'keywords_reversed': ['moving on', 'forgiveness', 'acceptance', 'new perspective'],
            'meaning_upright': 'Mourning what was lost. Grief is valid — but do not forget the cups still standing behind you.',
            'meaning_reversed': 'Beginning to accept loss and turn toward what remains. Healing is underway.',
        },
        {
            'number': 6,
            'name': 'Six of Cups',
            'keywords_upright': ['nostalgia', 'happy memories', 'childhood', 'innocence'],
            'keywords_reversed': ['living in the past', 'naivety', 'moving forward'],
            'meaning_upright': 'Sweet nostalgia and gifts from the past. Revisiting old joys can offer healing and warmth.',
            'meaning_reversed': 'Clinging to the past rather than engaging with the present. Honor memory without being trapped by it.',
        },
        {
            'number': 7,
            'name': 'Seven of Cups',
            'keywords_upright': ['choices', 'wishful thinking', 'illusion', 'fantasy'],
            'keywords_reversed': ['clarity', 'alignment', 'cutting through illusion'],
            'meaning_upright': 'Many tempting options, not all what they seem. Fantasy clouds reality — clarity requires discernment.',
            'meaning_reversed': 'The fog is lifting and a clear choice is emerging. Cut through illusion with honest evaluation.',
        },
        {
            'number': 8,
            'name': 'Eight of Cups',
            'keywords_upright': ['walking away', 'disillusionment', 'leaving behind', 'seeking more'],
            'keywords_reversed': ['stagnation', 'fear of change', 'aimlessness', 'staying too long'],
            'meaning_upright': 'Leaving something that no longer fulfills you, however difficult. Something better awaits.',
            'meaning_reversed': 'Staying in a situation past its time, or wandering without purpose. Face what needs to change.',
        },
        {
            'number': 9,
            'name': 'Nine of Cups',
            'keywords_upright': ['wishes fulfilled', 'contentment', 'satisfaction', 'gratitude'],
            'keywords_reversed': ['greed', 'dissatisfaction', 'materialism', 'smugness'],
            'meaning_upright': 'Your wish is granted. Contentment and emotional satisfaction — allow yourself to feel good.',
            'meaning_reversed': 'Fulfillment sought through external means or not fully appreciated. True contentment is inner.',
        },
        {
            'number': 10,
            'name': 'Ten of Cups',
            'keywords_upright': ['harmony', 'bliss', 'family', 'lasting joy'],
            'keywords_reversed': ['broken home', 'misaligned values', 'disconnection'],
            'meaning_upright': 'The fullest expression of emotional fulfilment — love, family, and lasting peace.',
            'meaning_reversed': 'Disharmony beneath a surface of contentment. What needs to be addressed to restore genuine joy?',
        },
        {
            'number': 11,
            'name': 'Page of Cups',
            'keywords_upright': ['creative opportunity', 'intuitive messages', 'emotional curiosity'],
            'keywords_reversed': ['emotional immaturity', 'creative block', 'escapism'],
            'meaning_upright': 'Playful, intuitive messages and creative invitations. Stay open to the unexpected.',
            'meaning_reversed': 'Emotional immaturity or escaping into fantasy. Ground creative energy in reality.',
        },
        {
            'number': 12,
            'name': 'Knight of Cups',
            'keywords_upright': ['romance', 'charm', 'following the heart', 'artistic'],
            'keywords_reversed': ['unrealistic', 'moody', 'overactive imagination'],
            'meaning_upright': 'Following your heart with romantic idealism. A creative, emotionally driven pursuit calls.',
            'meaning_reversed': 'Swept away by fantasy or emotion without a grounding tether. Bring heart and head into balance.',
        },
        {
            'number': 13,
            'name': 'Queen of Cups',
            'keywords_upright': ['compassion', 'emotional security', 'intuition', 'nurturing'],
            'keywords_reversed': ['co-dependency', 'emotional overwhelm', 'self-neglect'],
            'meaning_upright': 'Deep empathy and emotional intelligence. You hold space for others without losing yourself.',
            'meaning_reversed': 'Emotional boundaries blurred or personal needs neglected. Care for yourself first.',
        },
        {
            'number': 14,
            'name': 'King of Cups',
            'keywords_upright': ['emotional balance', 'diplomacy', 'compassionate authority'],
            'keywords_reversed': ['moodiness', 'emotional manipulation', 'repression'],
            'meaning_upright': 'Mastery of emotion — leading with calm, empathetic authority and wisdom.',
            'meaning_reversed': 'Emotions used as leverage or suppressed unhealthily. True mastery requires honest acknowledgment.',
        },
    ],
    'swords': [
        {
            'number': 1,
            'name': 'Ace of Swords',
            'keywords_upright': ['mental clarity', 'breakthrough', 'truth', 'new ideas'],
            'keywords_reversed': ['confusion', 'chaos', 'brutality', 'clouded thinking'],
            'meaning_upright': 'A sharp mental breakthrough cuts through confusion. Truth and clarity emerge — speak and think clearly.',
            'meaning_reversed': 'Mental fog or ideas that wound rather than illuminate. Wait for clarity before acting.',
        },
        {
            'number': 2,
            'name': 'Two of Swords',
            'keywords_upright': ['stalemate', 'difficult decision', 'indecision', 'truce'],
            'keywords_reversed': ['confusion', 'information overload', 'no right answer'],
            'meaning_upright': 'Poised at a crossroads with eyes covered. Gather information, then make a choice.',
            'meaning_reversed': 'Paralysis through over-analysis. Sometimes a decision made imperfectly beats no decision at all.',
        },
        {
            'number': 3,
            'name': 'Three of Swords',
            'keywords_upright': ['heartbreak', 'grief', 'sorrow', 'painful truth'],
            'keywords_reversed': ['releasing pain', 'healing', 'forgiveness', 'moving forward'],
            'meaning_upright': 'Grief or heartbreak that must be felt fully. Allow the pain — it carries important truth.',
            'meaning_reversed': 'The worst of the pain is passing. Release what happened and allow healing to begin.',
        },
        {
            'number': 4,
            'name': 'Four of Swords',
            'keywords_upright': ['rest', 'recovery', 'meditation', 'withdrawal'],
            'keywords_reversed': ['burnout', 'restlessness', 'returning to action'],
            'meaning_upright': 'Rest is not retreat — it is essential recovery. Step back and let your mind and body heal.',
            'meaning_reversed': 'Burnout from ignoring the need for rest, or a period of rest now ending. Reenter thoughtfully.',
        },
        {
            'number': 5,
            'name': 'Five of Swords',
            'keywords_upright': ['conflict', 'defeat', 'hollow victory', 'self-interest'],
            'keywords_reversed': ['reconciliation', 'regret', 'making amends'],
            'meaning_upright': 'A win that costs too much, or defeat that stings. Choose battles wisely — not all victories are worth having.',
            'meaning_reversed': 'Regret over past conflict opens the door to reconciliation. Humble yourself to repair what was damaged.',
        },
        {
            'number': 6,
            'name': 'Six of Swords',
            'keywords_upright': ['transition', 'moving on', 'rite of passage', 'calmer waters'],
            'keywords_reversed': ['resistance', 'stuck in the past', 'unfinished business'],
            'meaning_upright': 'Leaving turbulent waters behind for calmer shores. The transition may be quiet but it is real.',
            'meaning_reversed': 'Resisting a necessary departure. What keeps you anchored to the troubled place you are leaving?',
        },
        {
            'number': 7,
            'name': 'Seven of Swords',
            'keywords_upright': ['deception', 'strategy', 'getting away with it', 'stealth'],
            'keywords_reversed': ['coming clean', 'caught out', 'imposter syndrome'],
            'meaning_upright': 'Cunning strategy or deception — someone may not be showing their full hand. Trust carefully.',
            'meaning_reversed': 'A deception is exposed or guilt is weighing heavily. Honesty, however uncomfortable, is the way forward.',
        },
        {
            'number': 8,
            'name': 'Eight of Swords',
            'keywords_upright': ['restriction', 'negative thoughts', 'self-imprisonment', 'powerlessness'],
            'keywords_reversed': ['releasing limitation', 'new perspective', 'taking back power'],
            'meaning_upright': 'Trapped by your own thinking — the blindfold and bonds are largely self-imposed. Question your assumptions.',
            'meaning_reversed': 'The mental prison is beginning to dissolve. Step forward; freedom is closer than it seemed.',
        },
        {
            'number': 9,
            'name': 'Nine of Swords',
            'keywords_upright': ['anxiety', 'nightmare', 'fear', 'despair', 'worry'],
            'keywords_reversed': ['inner turmoil', 'deep-seated fears', 'secrets', 'dawn breaking'],
            'meaning_upright': 'Anxiety and worst-case thinking at 3 a.m. The mind torments itself. Seek support and perspective.',
            'meaning_reversed': 'The worst of the anxiety is breaking up. What hidden fear needs to be brought into the light?',
        },
        {
            'number': 10,
            'name': 'Ten of Swords',
            'keywords_upright': ['painful ending', 'betrayal', 'hitting rock bottom', 'deep wounds'],
            'keywords_reversed': ['recovery', 'resisting the end', 'partial healing'],
            'meaning_upright': 'A painful, final ending — but the darkest hour before dawn. The low point signals a turning point.',
            'meaning_reversed': 'Recovery is underway, or resistance to an ending that has already occurred. Accept and begin again.',
        },
        {
            'number': 11,
            'name': 'Page of Swords',
            'keywords_upright': ['curiosity', 'new ideas', 'mental energy', 'communication'],
            'keywords_reversed': ['all talk no action', 'hasty words', 'lack of follow-through'],
            'meaning_upright': 'Quick, curious mental energy and a thirst for truth. Ideas are sharp — now act on them.',
            'meaning_reversed': 'Sharp words without substance, or ideas that go no further than talk. Focus the mental energy.',
        },
        {
            'number': 12,
            'name': 'Knight of Swords',
            'keywords_upright': ['ambition', 'decisive action', 'directness', 'fast movement'],
            'keywords_reversed': ['reckless', 'hasty', 'scattered', 'missed details'],
            'meaning_upright': 'Moving at full speed with sharp focus. Act decisively, but ensure the charge has a clear target.',
            'meaning_reversed': 'Haste leading to mistakes. Slow down long enough to aim before drawing the sword.',
        },
        {
            'number': 13,
            'name': 'Queen of Swords',
            'keywords_upright': ['clear boundaries', 'direct communication', 'independence', 'wit'],
            'keywords_reversed': ['cold', 'easily hurt', 'overly critical', 'bitterness'],
            'meaning_upright': 'Uncompromising clarity and sharp intelligence. Speak your truth with precision and grace.',
            'meaning_reversed': 'Hurt feelings hardening into coldness, or cutting words that wound unnecessarily.',
        },
        {
            'number': 14,
            'name': 'King of Swords',
            'keywords_upright': ['intellectual authority', 'ethical leadership', 'truth', 'logic'],
            'keywords_reversed': ['tyrannical', 'manipulative', 'abusive power', 'coldness'],
            'meaning_upright': 'The highest application of intellect in service of justice and ethical leadership. Think clearly, act justly.',
            'meaning_reversed': 'Authority used to dominate rather than guide. Examine where cold logic has overridden compassion.',
        },
    ],
    'pentacles': [
        {
            'number': 1,
            'name': 'Ace of Pentacles',
            'keywords_upright': ['new financial opportunity', 'manifestation', 'abundance', 'security'],
            'keywords_reversed': ['missed opportunity', 'lack of planning', 'scarcity thinking'],
            'meaning_upright': 'A material or financial opportunity is at hand. Plant this seed wisely — it can grow into something lasting.',
            'meaning_reversed': 'A financial opportunity is missed or poorly planned. Examine your relationship with money and security.',
        },
        {
            'number': 2,
            'name': 'Two of Pentacles',
            'keywords_upright': ['balance', 'adaptability', 'time management', 'juggling priorities'],
            'keywords_reversed': ['imbalance', 'overwhelmed', 'disorganization'],
            'meaning_upright': 'Gracefully managing multiple demands. Keep the balls in the air — flexibility is your strength here.',
            'meaning_reversed': 'Too many plates spinning and something is about to drop. Simplify and prioritize ruthlessly.',
        },
        {
            'number': 3,
            'name': 'Three of Pentacles',
            'keywords_upright': ['teamwork', 'collaboration', 'craftsmanship', 'initial success'],
            'keywords_reversed': ['disorganization', 'lack of teamwork', 'working alone'],
            'meaning_upright': 'Skilled collaboration produces excellent results. Your contribution is valued — work with others.',
            'meaning_reversed': 'Miscommunication or ego undermining the team. Is everyone working toward the same goal?',
        },
        {
            'number': 4,
            'name': 'Four of Pentacles',
            'keywords_upright': ['security', 'conservatism', 'saving', 'control'],
            'keywords_reversed': ['greed', 'over-spending', 'financial insecurity', 'letting go'],
            'meaning_upright': 'Holding what you have earned. Prudent security — but check whether holding on has become hoarding.',
            'meaning_reversed': 'Gripping too tightly to money or possessions, or the opposite — reckless spending. Find the middle ground.',
        },
        {
            'number': 5,
            'name': 'Five of Pentacles',
            'keywords_upright': ['financial loss', 'hardship', 'isolation', 'lack mindset'],
            'keywords_reversed': ['recovery', 'spiritual poverty', 'gradual improvement'],
            'meaning_upright': 'A period of material hardship or feeling left out in the cold. Help is available — look up and ask.',
            'meaning_reversed': 'Emerging from a difficult period, or wealth present but no peace of mind. Tend to your inner resources.',
        },
        {
            'number': 6,
            'name': 'Six of Pentacles',
            'keywords_upright': ['generosity', 'giving', 'receiving', 'sharing wealth'],
            'keywords_reversed': ['one-sided charity', 'debt', 'power imbalance'],
            'meaning_upright': 'The cycle of giving and receiving flows freely. Be generous — what you give returns.',
            'meaning_reversed': 'Charity with strings attached, or an imbalance of power in financial relationships. Examine the exchange.',
        },
        {
            'number': 7,
            'name': 'Seven of Pentacles',
            'keywords_upright': ['patience', 'long-term investment', 'assessment', 'sustainable effort'],
            'keywords_reversed': ['impatience', 'limited reward', 'poor investment'],
            'meaning_upright': 'Pausing to assess the growth of your efforts. Not every harvest is immediate — tend the garden with patience.',
            'meaning_reversed': 'Effort not yielding expected returns. Evaluate whether this investment of time and energy is sound.',
        },
        {
            'number': 8,
            'name': 'Eight of Pentacles',
            'keywords_upright': ['diligence', 'mastery', 'craftsmanship', 'apprenticeship'],
            'keywords_reversed': ['perfectionism', 'self-development stalled', 'misdirected effort'],
            'meaning_upright': 'Dedicated, focused work toward mastery. Put in the hours — quality comes from repetition and devotion.',
            'meaning_reversed': 'Perfectionism blocking completion, or effort aimed at the wrong goal. Reassess your focus.',
        },
        {
            'number': 9,
            'name': 'Nine of Pentacles',
            'keywords_upright': ['abundance', 'luxury', 'self-sufficiency', 'refinement'],
            'keywords_reversed': ['self-worth issues', 'financial setback', 'over-reliance on others'],
            'meaning_upright': 'Hard-earned abundance and the satisfaction of self-sufficiency. Enjoy the fruits of your labour.',
            'meaning_reversed': 'Financial independence threatened or self-worth tied too tightly to material success. Look deeper.',
        },
        {
            'number': 10,
            'name': 'Ten of Pentacles',
            'keywords_upright': ['legacy', 'wealth', 'family', 'long-term security'],
            'keywords_reversed': ['family disputes', 'instability', 'loss of legacy'],
            'meaning_upright': 'Lasting wealth and a meaningful legacy. The fullest material fulfilment — security across generations.',
            'meaning_reversed': 'Family conflict over money or inheritance, or long-built security suddenly unstable.',
        },
        {
            'number': 11,
            'name': 'Page of Pentacles',
            'keywords_upright': ['ambition', 'manifestation', 'skill development', 'new venture'],
            'keywords_reversed': ['procrastination', 'lack of progress', 'poor planning'],
            'meaning_upright': 'Eager, grounded energy around a new practical venture. Study, plan, and begin with steady focus.',
            'meaning_reversed': 'Ambition without action, or a promising plan stalled by procrastination. Take the first small step.',
        },
        {
            'number': 12,
            'name': 'Knight of Pentacles',
            'keywords_upright': ['hard work', 'reliability', 'methodical', 'responsibility'],
            'keywords_reversed': ['boredom', 'stagnation', 'feeling stuck', 'perfectionism'],
            'meaning_upright': 'Steady, reliable progress through careful methodical effort. Slow and sure wins the race.',
            'meaning_reversed': 'Stuck in routine or bored by the pace. Inject some flexibility without abandoning discipline.',
        },
        {
            'number': 13,
            'name': 'Queen of Pentacles',
            'keywords_upright': ['nurturing', 'practical', 'financially savvy', 'grounded warmth'],
            'keywords_reversed': ['financial insecurity', 'smothering', 'self-neglect'],
            'meaning_upright': 'Abundantly practical and warmly nurturing. You provide richly for those in your care, including yourself.',
            'meaning_reversed': 'Neglecting your own needs while caring for others, or anxiety around financial security.',
        },
        {
            'number': 14,
            'name': 'King of Pentacles',
            'keywords_upright': ['wealth', 'business acumen', 'leadership', 'security'],
            'keywords_reversed': ['materialistic', 'stubborn', 'poor financial decisions'],
            'meaning_upright': 'The pinnacle of material mastery — wealth built through patience, wisdom, and steady work.',
            'meaning_reversed': 'Success pursued at the cost of everything else, or poor financial stewardship. Reassess priorities.',
        },
    ],
}

# ---------------------------------------------------------------------------
# Three Card spread
# ---------------------------------------------------------------------------

THREE_CARD_SPREAD = {
    'name': 'Three Card',
    'description': (
        'A classic three-card spread offering insight into the arc of a situation '
        'across time or exploring its different facets.'
    ),
    'num_cards': 3,
    'positions': [
        {
            'position_number': 1,
            'name': 'Past',
            'description': 'What has led to the current situation — the roots, history, or recent events shaping things.',
            'thematic_note': (
                'This card represents the energies, events, or influences from the past '
                'that have directly contributed to the current moment. Consider what '
                'foundations or patterns are at play here.'
            ),
        },
        {
            'position_number': 2,
            'name': 'Present',
            'description': 'The current state of affairs — the heart of the matter as it stands now.',
            'thematic_note': (
                'This card reflects the energy most active in the querent\'s life right now. '
                'It is the crux of the situation and often the most important card in the spread.'
            ),
        },
        {
            'position_number': 3,
            'name': 'Future',
            'description': 'The likely outcome if the current course continues — a potential trajectory, not a fixed fate.',
            'thematic_note': (
                'This card points toward a probable future based on current energies. '
                'It is not inevitable — choices made now can shift the outcome. '
                'Read it as guidance rather than prophecy.'
            ),
        },
    ],
}


# ---------------------------------------------------------------------------
# Management command
# ---------------------------------------------------------------------------

class Command(BaseCommand):
    help = 'Seed the database with the Rider-Waite deck and Three Card spread.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete existing deck and spread data before seeding.',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Deck.objects.filter(name='Rider-Waite').delete()
            Spread.objects.filter(name='Three Card').delete()
            self.stdout.write(self.style.WARNING('Cleared.'))

        # -- Deck & cards --------------------------------------------------
        deck, created = Deck.objects.get_or_create(
            name='Rider-Waite',
            defaults={'description': (
                'The classic 1909 Rider-Waite-Smith tarot deck illustrated by '
                'Pamela Colman Smith under the direction of Arthur Edward Waite. '
                'The most widely recognised tarot deck in the world.'
            )},
        )
        if not created:
            self.stdout.write(self.style.WARNING('Rider-Waite deck already exists — skipping cards. Use --clear to reseed.'))
        else:
            self._seed_cards(deck)
            self.stdout.write(self.style.SUCCESS(f'Created Rider-Waite deck with {deck.cards.count()} cards.'))

        # -- Spread --------------------------------------------------------
        spread, created = Spread.objects.get_or_create(
            name='Three Card',
            defaults={
                'description': THREE_CARD_SPREAD['description'],
                'num_cards': THREE_CARD_SPREAD['num_cards'],
            },
        )
        if not created:
            self.stdout.write(self.style.WARNING('Three Card spread already exists — skipping. Use --clear to reseed.'))
        else:
            for pos_data in THREE_CARD_SPREAD['positions']:
                SpreadPosition.objects.create(spread=spread, **pos_data)
            self.stdout.write(self.style.SUCCESS('Created Three Card spread with 3 positions.'))

        self.stdout.write(self.style.SUCCESS('Done.'))

    def _seed_cards(self, deck):
        # Major Arcana
        for card_data in MAJOR_ARCANA:
            Card.objects.create(
                deck=deck,
                arcana='major',
                suit=None,
                image_filename=f"{card_data['number']:02d}-{card_data['name'].lower().replace(' ', '-').replace('the-', '')}.jpg",
                **card_data,
            )

        # Minor Arcana
        for suit, cards in MINOR_ARCANA.items():
            for card_data in cards:
                Card.objects.create(
                    deck=deck,
                    arcana='minor',
                    suit=suit,
                    image_filename=f"{suit}-{card_data['number']:02d}-{card_data['name'].lower().replace(' ', '-')}.jpg",
                    **card_data,
                )
