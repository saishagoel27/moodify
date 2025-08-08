from typing import Dict, List, Optional

class EmotionAnalyzer:
    """Handles emotion detection and mapping"""
    
    POSITIVE_THRESHOLD = 0.7  
    NEGATIVE_THRESHOLD = 0.6  
    EMOTION_KEYWORDS = {
        'joy': ['happy', 'excited', 'wonderful', 'amazing', 'love', 'great', 'fantastic', 'thrilled', 'delighted', 'ecstatic'],
        'sadness': ['sad', 'depressed', 'down', 'lonely', 'hurt', 'disappointed', 'devastated', 'miserable', 'heartbroken'],
        'anger': ['angry', 'mad', 'frustrated', 'annoyed', 'furious', 'irritated', 'outraged', 'livid', 'enraged'],
        'fear': ['scared', 'afraid', 'worried', 'anxious', 'nervous', 'concerned', 'terrified', 'panicked', 'apprehensive'],
        'surprise': ['surprised', 'shocked', 'unexpected', 'sudden', 'amazed', 'astonished', 'stunned', 'bewildered'],
        'disgust': ['disgusted', 'sick', 'awful', 'terrible', 'hate', 'revolted', 'repulsed', 'nauseated']
    }
    
    @staticmethod
    def determine_primary_emotion(analysis_results: Dict) -> str:
        """Figure out the main emotion from Azure analysis results"""
        # Handles empty or invalid input
        if not analysis_results or not isinstance(analysis_results, dict):
            return 'neutral'
        
        # Extract data safely with fallbacks
        sentiment_data = analysis_results.get('sentiment', {})
        sentiment_scores = sentiment_data.get('scores', {}) if sentiment_data else {}
        key_phrases = analysis_results.get('key_phrases', [])
        entities = analysis_results.get('entities', [])
        
        # Combine text from key phrases and entities for keyword matching
        text_to_analyze = []
        
        # Add key phrases
        if key_phrases and isinstance(key_phrases, list):
            text_to_analyze.extend(key_phrases)
        
        # Add entity text 
        if entities and isinstance(entities, list):
            for entity in entities:
                if isinstance(entity, (list, tuple)) and len(entity) >= 1:
                    text_to_analyze.append(str(entity[0]))
        
        # Convert to lowercase for matching
        combined_text = ' '.join(text_to_analyze).lower()
        
        # Count emotion keywords
        emotion_scores = {}
        for emotion, keywords in EmotionAnalyzer.EMOTION_KEYWORDS.items():
            # Count how many keywords appear in the text
            keyword_count = sum(1 for keyword in keywords if keyword in combined_text)
            emotion_scores[emotion] = keyword_count
        
        # Return emotion with most keyword matches if any found
        max_score = max(emotion_scores.values()) if emotion_scores else 0
        if max_score > 0:
            return max(emotion_scores, key=emotion_scores.get)
        
        # Fallback to sentiment analysis when no keywords found
        positive_score = sentiment_scores.get('positive', 0)
        negative_score = sentiment_scores.get('negative', 0)
        
        if positive_score > EmotionAnalyzer.POSITIVE_THRESHOLD:
            return 'joy'
        elif negative_score > EmotionAnalyzer.NEGATIVE_THRESHOLD:
            return 'sadness'
        else:
            return 'neutral'
    
    @staticmethod
    def get_emotion_confidence(analysis_results: Dict, detected_emotion: str) -> float:
        """Get confidence score for the detected emotion"""
        if not analysis_results or not detected_emotion:
            return 0.0
        
        sentiment_data = analysis_results.get('sentiment', {})
        sentiment_scores = sentiment_data.get('scores', {}) if sentiment_data else {}
        
        # Map emotions to corresponding sentiment scores
        if detected_emotion == 'joy':
            return sentiment_scores.get('positive', 0.0)
        elif detected_emotion in ['sadness', 'anger', 'fear', 'disgust']:
            return sentiment_scores.get('negative', 0.0)
        elif detected_emotion == 'surprise':
            pos_score = sentiment_scores.get('positive', 0.0)
            neg_score = sentiment_scores.get('negative', 0.0)
            return max(pos_score, neg_score)
        else:  
            return sentiment_scores.get('neutral', 0.0)
    
    @staticmethod
    def get_emotion_breakdown(analysis_results: Dict) -> Dict[str, int]:
        """Get keyword count breakdown for all emotions"""
        if not analysis_results:
            return {}
        
        key_phrases = analysis_results.get('key_phrases', [])
        entities = analysis_results.get('entities', [])
        
        # Combine text sources
        text_to_analyze = []
        if key_phrases:
            text_to_analyze.extend(key_phrases)
        if entities:
            for entity in entities:
                if isinstance(entity, (list, tuple)) and len(entity) >= 1:
                    text_to_analyze.append(str(entity[0]))
        
        combined_text = ' '.join(text_to_analyze).lower()
        
        # Count keywords for each emotion
        breakdown = {}
        for emotion, keywords in EmotionAnalyzer.EMOTION_KEYWORDS.items():
            count = sum(1 for keyword in keywords if keyword in combined_text)
            breakdown[emotion] = count
        
        return breakdown