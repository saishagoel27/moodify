from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from typing import Dict, List, Tuple, Optional
import logging

class AzureConfig:
    def __init__(self, endpoint: str, key: str):
        self.endpoint = endpoint
        self.key = key

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AzureTextAnalyzer:
    """Handles Azure AI Language Service operations"""
    
    def __init__(self, config: AzureConfig):
        self.client = TextAnalyticsClient(
            endpoint=config.endpoint,
            credential=AzureKeyCredential(config.key)
        )
    
    def analyze_text_comprehensive(self, text: str) -> Optional[Dict]:
        """
        Comprehensive text analysis using multiple Azure AI features
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing all analysis results or None if error
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for analysis")
            return None
        
        results = {}
        
        try:
            # Sentiment Analysis
            results['sentiment'] = self._analyze_sentiment(text)
            
            # Key Phrase Extraction
            results['key_phrases'] = self._extract_key_phrases(text)
            
            # Entity Recognition
            results['entities'] = self._recognize_entities(text)
            
            # Language Detection
            results['language'] = self._detect_language(text)
            
            # PII Detection
            results['pii_entities'] = self._detect_pii(text)
            
            logger.info(f"Successfully analyzed text with {len(results)} features")
            return results
            
        except AzureError as e:
            logger.error(f"Azure service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during analysis: {e}")
            return None
    
    def _analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of text"""
        try:
            result = self.client.analyze_sentiment(documents=[text])[0]
            return {
                'label': result.sentiment,
                'scores': {
                    'positive': result.confidence_scores.positive,
                    'neutral': result.confidence_scores.neutral,
                    'negative': result.confidence_scores.negative
                }
            }
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {'label': 'neutral', 'scores': {'positive': 0, 'neutral': 1, 'negative': 0}}
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases from text"""
        try:
            result = self.client.extract_key_phrases(documents=[text])[0]
            return result.key_phrases
        except Exception as e:
            logger.error(f"Key phrase extraction failed: {e}")
            return []
    
    def _recognize_entities(self, text: str) -> List[Tuple[str, str, float]]:
        """Recognize named entities in text"""
        try:
            result = self.client.recognize_entities(documents=[text])[0]
            return [(entity.text, entity.category, entity.confidence_score) 
                   for entity in result.entities]
        except Exception as e:
            logger.error(f"Entity recognition failed: {e}")
            return []
    
    def _detect_language(self, text: str) -> Dict:
        """Detect language of text"""
        try:
            result = self.client.detect_language(documents=[text])[0]
            return {
                'name': result.primary_language.name,
                'code': result.primary_language.iso6391_name,
                'confidence': result.primary_language.confidence_score
            }
        except Exception as e:
            logger.error(f"Language detection failed: {e}")
            return {'name': 'English', 'code': 'en', 'confidence': 0.0}
    
    def _detect_pii(self, text: str) -> List[Tuple[str, str]]:
        """Detect personally identifiable information"""
        try:
            result = self.client.recognize_pii_entities(documents=[text])[0]
            return [(entity.text, entity.category) for entity in result.entities]
        except Exception as e:
            logger.error(f"PII detection failed: {e}")
            return []