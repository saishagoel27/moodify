import random
from typing import Dict, List

class RecommendationEngine:
    """Handles mood-based recommendations"""
    
    RECOMMENDATIONS = {
        "joy": {
            "songs": [
                "🎵 Feel Good Hits: https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
                "🎵 Pop Rising: https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd",
                "🎵 Good Vibes: https://open.spotify.com/playlist/37i9dQZF1DX4VqfSk8VmCi"
            ],
            "quotes": [
                "The best time to plant a tree was 20 years ago. The second best time is now.",
                "Life is what happens to you while you're busy making other plans. - John Lennon",
                "The only way to do great work is to love what you do. - Steve Jobs"
            ],
            "activities": [
                "📞 Call a friend you haven't talked to in a while",
                "🌳 Take a walk in nature",
                "🎨 Try a creative hobby"
            ]
        },
        "sadness": {
            "songs": [
                "🎵 Healing Vibes: https://open.spotify.com/playlist/37i9dQZF1DX59NCqCqJtoH",
                "🎵 Comfort Zone: https://open.spotify.com/playlist/37i9dQZF1DWZUAeYvs88zc",
                "🎵 Gentle Acoustic: https://open.spotify.com/playlist/37i9dQZF1DX1s9knjP51Oa"
            ],
            "quotes": [
                "This too shall pass.",
                "You are stronger than you think and more resilient than you know.",
                "Every storm runs out of rain. - Maya Angelou"
            ],
            "activities": [
                "🛁 Take a warm bath or shower",
                "📝 Write in a journal",
                "🫖 Make your favorite warm drink"
            ]
        },
        "anger": {
            "songs": [
                "🎵 Workout Beats: https://open.spotify.com/playlist/37i9dQZF1DX76Wlfdnj7AP",
                "🎵 Rock Anthems: https://open.spotify.com/playlist/37i9dQZF1DX8FwnYE6PRvL",
                "🎵 Release Energy: https://open.spotify.com/playlist/37i9dQZF1DX32NsLKyzScr"
            ],
            "quotes": [
                "Anger is an acid that can do more harm to the vessel than to anything it pours upon.",
                "The best fighter is never angry. - Lao Tzu",
                "You will not be punished for your anger; you will be punished by your anger."
            ],
            "activities": [
                "🏃 Go for a run or intense workout",
                "🥊 Try a boxing workout",
                "🧘 Practice deep breathing exercises"
            ]
        },
        "fear": {
            "songs": [
                "🎵 Calming Instrumentals: https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwAYIy1",
                "🎵 Confidence Boosters: https://open.spotify.com/playlist/37i9dQZF1DX0BcQWzuB7ZO",
                "🎵 Empowerment: https://open.spotify.com/playlist/37i9dQZF1DX4fpCWaHOned"
            ],
            "quotes": [
                "Courage is not the absence of fear, but action despite it.",
                "The cave you fear to enter holds the treasure you seek.",
                "You are braver than you believe, stronger than you seem."
            ],
            "activities": [
                "🧘 Practice mindfulness meditation",
                "📚 Read inspiring success stories",
                "💪 List your past achievements"
            ]
        },
        "surprise": {
            "songs": [
                "🎵 Discovery Playlist: https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd",
                "🎵 World Music: https://open.spotify.com/playlist/37i9dQZF1DX0Urj5lo8vTp",
                "🎵 Eclectic Mix: https://open.spotify.com/playlist/37i9dQZF1DWWQRwui0ExPn"
            ],
            "quotes": [
                "Life is full of surprises, embrace them all.",
                "The unexpected is often the most beautiful part of life.",
                "Surprises are gifts from the universe."
            ],
            "activities": [
                "🎲 Try something completely new",
                "🌍 Explore a new place in your city",
                "🎨 Experiment with a new art form"
            ]
        },
        "disgust": {
            "songs": [
                "🎵 Cleansing Sounds: https://open.spotify.com/playlist/37i9dQZF1DX0Urj5lo8vTp",
                "🎵 Fresh Start: https://open.spotify.com/playlist/37i9dQZF1DX4VqfSk8VmCi",
                "🎵 Positive Vibes: https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC"
            ],
            "quotes": [
                "Sometimes you need to step back to see the beauty in chaos.",
                "Cleanliness is next to godliness.",
                "A fresh perspective can transform any situation."
            ],
            "activities": [
                "🧹 Organize and clean your space",
                "🚿 Take a refreshing shower",
                "🌿 Spend time in nature"
            ]
        },
        "neutral": {
            "songs": [
                "🎵 Ambient Chill: https://open.spotify.com/playlist/37i9dQZF1DWWQRwui0ExPn",
                "🎵 Lo-fi Study: https://open.spotify.com/playlist/37i9dQZF1DX0SM0LYsmbMT",
                "🎵 Background Instrumentals: https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwAYIy1"
            ],
            "quotes": [
                "In stillness, we find our center.",
                "Peace is not the absence of conflict, but the ability to cope with it.",
                "Sometimes the most profound thing you can do is nothing."
            ],
            "activities": [
                "📖 Read a book quietly",
                "☕ Enjoy a hot beverage mindfully",
                "🌅 Watch the sunrise or sunset"
            ]
        }
    }
    
    @staticmethod
    def get_recommendation(emotion: str, recommendation_type: str) -> str:
        """
        Get a recommendation based on emotion and type
        
        Args:
            emotion: Detected emotion
            recommendation_type: Type of recommendation (songs, quotes, activities)
            
        Returns:
            Random recommendation string
        """
        if emotion in RecommendationEngine.RECOMMENDATIONS:
            recommendations = RecommendationEngine.RECOMMENDATIONS[emotion].get(recommendation_type, [])
            if recommendations:
                return random.choice(recommendations)
        
        return f"No {recommendation_type} recommendations available for {emotion}"