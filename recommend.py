import random
from typing import Dict, List, Optional

class RecommendationEngine:
    """Handles mood-based recommendations"""
    
    RECOMMENDATIONS = {
        "joy": {
            "songs": [
                "🎵 Upbeat Pop - Try artists like Dua Lipa, Lizzo, or The Weeknd",
                "🎵 Classic Feel-Good - Queen, Stevie Wonder, Earth Wind & Fire",
                "🎵 Happy Hip-Hop - Chance the Rapper, Pharrell Williams",
                "🎵 Indie Pop Vibes - COIN, Two Door Cinema Club, Foster the People",
                "🎵 Dance/Electronic - Calvin Harris, Daft Punk, Disclosure"
            ],
            "quotes": [
                "Happiness is not something ready made. It comes from your own actions. - Dalai Lama",
                "The best time to plant a tree was 20 years ago. The second best time is now.",
                "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
                "Life is what happens when you're busy making other plans. - John Lennon",
                "The only way to do great work is to love what you do. - Steve Jobs"
            ],
            "activities": [
                "📞 Call someone you love and tell them why they matter",
                "🌳 Take a walk outside and notice 5 beautiful things",
                "🎨 Try a creative project - draw, write, or build something",
                "📸 Take photos of things that make you smile",
                "🍰 Bake something delicious for yourself or others"
            ]
        },
        "sadness": {
            "songs": [
                "🎵 Gentle Acoustic - Bon Iver, Iron & Wine, Fleet Foxes",
                "🎵 Comfort Music - Your personal comfort songs work best",
                "🎵 Healing Vibes - Lo-fi playlists or ambient music",
                "🎵 Soft R&B - Frank Ocean, SZA, Daniel Caesar",
                "🎵 Indie Folk - Phoebe Bridgers, Julien Baker, Big Thief"
            ],
            "quotes": [
                "This too shall pass.",
                "You are stronger than you think and more resilient than you know.",
                "It's okay to not be okay sometimes. Healing isn't linear.",
                "Every storm runs out of rain. - Maya Angelou",
                "The wound is the place where the Light enters you. - Rumi"
            ],
            "activities": [
                "🛁 Take a warm bath with calming music",
                "📝 Write in a journal - let it all out",
                "🫖 Make your favorite warm drink and savor it slowly",
                "🧸 Practice gentle self-care activities",
                "📱 Watch comforting videos or shows from your childhood"
            ]
        },
        "anger": {
            "songs": [
                "🎵 High Energy Rock - Foo Fighters, Green Day, Paramore",
                "🎵 Intense Workout Music - Whatever gets your energy out",
                "🎵 Metal/Hard Rock - Metallica, Linkin Park, Rage Against the Machine",
                "🎵 Aggressive Hip-Hop - Eminem, DMX, Run the Jewels",
                "🎵 Transition to Calm - After releasing energy, try something soothing"
            ],
            "quotes": [
                "Anger is an acid that can do more harm to the vessel than to anything it pours upon.",
                "You have power over your mind - not outside events. Realize this, and you will find strength. - Marcus Aurelius",
                "The best fighter is never angry. - Lao Tzu",
                "Holding onto anger is like drinking poison and expecting the other person to die.",
                "Speak when you are angry and you will make the best speech you will ever regret."
            ],
            "activities": [
                "🏃 Go for a run or do intense cardio",
                "🥊 Try a boxing workout or hit a punching bag",
                "🧘 Practice deep breathing - 4 counts in, 6 counts out",
                "📝 Write out your feelings, then tear up the paper",
                "🧹 Channel energy into cleaning or organizing"
            ]
        },
        "fear": {
            "songs": [
                "🎵 Calming Instrumentals - Max Richter, Ólafur Arnalds",
                "🎵 Empowering Songs - Beyoncé, Alicia Keys, Kelly Clarkson",
                "🎵 Meditation Music - Nature sounds or ambient tracks",
                "🎵 Confidence Builders - Songs that make you feel strong",
                "🎵 Familiar Comfort - Play music that feels safe and known"
            ],
            "quotes": [
                "Courage is not the absence of fear, but action in spite of it.",
                "You are braver than you believe, stronger than you seem, and smarter than you think. - A.A. Milne",
                "Feel the fear and do it anyway. - Susan Jeffers",
                "The cave you fear to enter holds the treasure you seek. - Joseph Campbell",
                "Everything you've ever wanted is on the other side of fear. - George Addair"
            ],
            "activities": [
                "🧘 Practice mindfulness or guided meditation",
                "📚 Read inspiring stories of people overcoming challenges",
                "💪 List 10 things you've successfully overcome before",
                "🤝 Talk to someone you trust about what's worrying you",
                "🌬️ Try the 5-4-3-2-1 grounding technique"
            ]
        },
        "surprise": {
            "songs": [
                "🎵 Discovery Mode - Try a completely new genre today",
                "🎵 World Music - Explore sounds from different cultures",
                "🎵 Throwback Hits - Songs from a decade you don't usually listen to",
                "🎵 Experimental Music - Jazz fusion, art rock, or electronic",
                "🎵 Random Shuffle - Let algorithms surprise you"
            ],
            "quotes": [
                "Life is full of surprises - embrace them all.",
                "The unexpected can be the most beautiful part of life.",
                "Stay curious and open to new experiences.",
                "Surprises keep life interesting and full of possibilities.",
                "Every day holds the potential for something amazing."
            ],
            "activities": [
                "🎲 Try something completely new today - a food, place, or hobby",
                "🌍 Explore a neighborhood in your city you've never visited",
                "🎨 Experiment with a new art form or creative medium",
                "📱 Learn something random on YouTube for 30 minutes",
                "🎪 Be spontaneous - do the first fun thing that comes to mind"
            ]
        },
        "disgust": {
            "songs": [
                "🎵 Cleansing Music - Fresh, uplifting indie or pop",
                "🎵 Reset Playlist - Music for a fresh start and new perspective",
                "🎵 Nature Sounds - Rain, ocean waves, or forest ambiance",
                "🎵 Positive Energy - Upbeat songs that lift your mood",
                "🎵 Gentle Transition - Soft music to shift your mindset"
            ],
            "quotes": [
                "Sometimes you need distance to see things clearly.",
                "A fresh perspective can transform any situation.",
                "Focus on what you can control and let go of what you can't.",
                "This feeling will pass. Choose to focus on something beautiful.",
                "Clean surroundings lead to a clearer mind."
            ],
            "activities": [
                "🧹 Clean and organize your immediate space",
                "🚿 Take a refreshing shower and change into clean clothes",
                "🌿 Spend time in nature - fresh air helps reset your mood",
                "🔄 Do something to completely change your environment",
                "📱 Watch something wholesome or funny to shift your mindset"
            ]
        },
        "neutral": {
            "songs": [
                "🎵 Background Music - Lo-fi, ambient, or instrumental",
                "🎵 Study/Focus Music - Minimal beats or classical",
                "🎵 Whatever's Familiar - Your usual go-to music",
                "🎵 Seasonal Music - Something that matches the current weather",
                "🎵 Nostalgic Tunes - Songs that bring back good memories"
            ],
            "quotes": [
                "In stillness, we find clarity.",
                "Sometimes doing nothing is doing something.",
                "Peace comes from within. Do not seek it without. - Buddha",
                "The present moment is the only time over which we have dominion. - Thích Nhất Hạnh",
                "Contentment is natural wealth, luxury is artificial poverty. - Socrates"
            ],
            "activities": [
                "📖 Read quietly - fiction, non-fiction, or poetry",
                "☕ Enjoy a drink mindfully without distractions",
                "🌅 Watch the sky - clouds, sunset, or stars",
                "🎯 Focus on a simple, satisfying task",
                "🧘 Just sit quietly and observe your thoughts"
            ]
        }
    }
    
    @staticmethod
    def get_recommendation(emotion: str, rec_type: str) -> str:
        """Get a random recommendation for the given emotion and type"""
        emotion = emotion.lower()
        
        # for handling edge cases
        if not emotion or not rec_type:
            return "Please specify both emotion and recommendation type"
        
        if emotion not in RecommendationEngine.RECOMMENDATIONS:
            return f"No recommendations available for emotion: {emotion}"
        
        recommendations = RecommendationEngine.RECOMMENDATIONS[emotion].get(rec_type, [])
        
        if not recommendations:
            return f"No {rec_type} recommendations available for {emotion}"
        
        return random.choice(recommendations)
    
    @staticmethod
    def get_all_recommendations(emotion: str) -> Dict[str, str]:
        """Get one recommendation of each type for an emotion"""
        return {
            'songs': RecommendationEngine.get_recommendation(emotion, 'songs'),
            'quotes': RecommendationEngine.get_recommendation(emotion, 'quotes'),
            'activities': RecommendationEngine.get_recommendation(emotion, 'activities')
        }
    
    @staticmethod
    def add_custom_recommendation(emotion: str, rec_type: str, recommendation: str) -> bool:
        """Add a custom recommendation for future personalization"""
        if not all([emotion, rec_type, recommendation]):
            return False
            
        emotion = emotion.lower()
        
        if emotion in RecommendationEngine.RECOMMENDATIONS:
            if rec_type in RecommendationEngine.RECOMMENDATIONS[emotion]:
                RecommendationEngine.RECOMMENDATIONS[emotion][rec_type].append(recommendation)
                return True
        return False
    
    @staticmethod
    def get_available_emotions() -> List[str]:
        """Get list of all available emotions"""
        return list(RecommendationEngine.RECOMMENDATIONS.keys())
    
    @staticmethod
    def get_available_types() -> List[str]:
        """Get list of all recommendation types"""
        return ['songs', 'quotes', 'activities']