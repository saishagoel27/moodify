from typing import Dict, List

class EmotionAnalyzer:
    """Handles emotion detection and mapping"""
    
    EMOTION_KEYWORDS = {
        'joy': ['happy', 'excited', 'wonderful', 'amazing', 'love', 'great', 'fantastic', 'thrilled'],
        'sadness': ['sad', 'depressed', 'down', 'lonely', 'hurt', 'disappointed', 'devastated'],
        'anger': ['angry', 'mad', 'frustrated', 'annoyed', 'furious', 'irritated', 'outraged'],
        'fear': ['scared', 'afraid', 'worried', 'anxious', 'nervous', 'concerned', 'terrified'],
        'surprise': ['surprised', 'shocked', 'unexpected', 'sudden', 'amazed', 'astonished'],
        'disgust': ['disgusted', 'sick', 'awful', 'terrible', 'hate', 'revolted']
    }
    
    @staticmethod
    def determine_primary_emotion(analysis_results: Dict) -> str:
        """
        Determine primary emotion from analysis results
        
        Args:
            analysis_results: Results from Azure text analysis
            
        Returns:
            Primary emotion as string
        """
        sentiment_scores = analysis_results.get('sentiment', {}).get('scores', {})
        key_phrases = analysis_results.get('key_phrases', [])
        
        # Check for emotion keywords in key phrases
        text_lower = ' '.join(key_phrases).lower()
        
        emotion_scores = {}
        for emotion, keywords in EmotionAnalyzer.EMOTION_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            emotion_scores[emotion] = score
        
        # Return emotion with highest keyword match
        if emotion_scores and max(emotion_scores.values()) > 0:
            return max(emotion_scores, key=emotion_scores.get)
        
        # Fallback to sentiment-based emotion
        if sentiment_scores.get('positive', 0) > 0.7:
            return 'joy'
        elif sentiment_scores.get('negative', 0) > 0.6:
            return 'sadness'
        else:
            return 'neutral'