from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from typing import Dict, List, Tuple, Optional
import logging
from config import AzureConfig

logger = logging.getLogger(__name__)

class AzureTextAnalyzer:
    """Azure AI Language Service"""
    
    def __init__(self, config: AzureConfig):
        self.client = TextAnalyticsClient(
            endpoint=config.endpoint,
            credential=AzureKeyCredential(config.key)
        )
        self.logger = logger
    
    def analyze_text_comprehensive(self, text: str) -> Dict:
        """Run all available Azure AI analysis on the text"""
        if not text.strip():
            raise ValueError("Text cannot be empty")
        
        results = {
            'sentiment': self._get_sentiment(text),
            'key_phrases': self._get_key_phrases(text),
            'entities': self._get_entities(text),
            'language': self._detect_language(text),
            'pii_entities': self._get_pii(text)
        }
        
        self.logger.info(f"Analyzed text with {len(results)} features")
        return results
    
    def _get_sentiment(self, text: str) -> Dict:
        """Get sentiment analysis results"""
        result = self.client.analyze_sentiment(documents=[text])[0]
        return {
            'label': result.sentiment,
            'scores': {
                'positive': result.confidence_scores.positive,
                'neutral': result.confidence_scores.neutral,
                'negative': result.confidence_scores.negative
            }
        }
    
    def _get_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases"""
        result = self.client.extract_key_phrases(documents=[text])[0]
        return result.key_phrases
    
    def _get_entities(self, text: str) -> List[Tuple[str, str, float]]:
        """Get named entities with confidence scores"""
        result = self.client.recognize_entities(documents=[text])[0]
        return [(entity.text, entity.category, entity.confidence_score) 
                for entity in result.entities]
    
    def _detect_language(self, text: str) -> Dict:
        """Detect the language of the text"""
        result = self.client.detect_language(documents=[text])[0]
        return {
            'name': result.primary_language.name,
            'code': result.primary_language.iso6391_name,
            'confidence': result.primary_language.confidence_score
        }
    
    def _get_pii(self, text: str) -> List[Tuple[str, str]]:
        """Find personally identifiable information"""
        result = self.client.recognize_pii_entities(documents=[text])[0]
        return [(entity.text, entity.category) for entity in result.entities]