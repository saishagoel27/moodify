import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class AzureConfig:
    """Azure AI Language Service configuration"""
    endpoint: str
    key: str
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        if not self.endpoint.startswith('https://'):
            raise ValueError("Azure endpoint must be a valid HTTPS URL")
        
        if len(self.key) < 30:
            logger.warning("Azure key seems short - double check if it's correct")
            print(f"Warning: Azure key length is {len(self.key)}, expected 32+")
    
    @classmethod
    def from_env(cls, env_file: str = '.env') -> 'AzureConfig':
        """Load configuration from environment variables"""
        # Load environment variables
        load_dotenv(env_file)
        
        endpoint = (os.getenv("AZURE_LANGUAGE_ENDPOINT") or 
                   os.getenv("AZURE_ENDPOINT") or 
                   os.getenv("LANGUAGE_ENDPOINT"))
        
        key = (os.getenv("AZURE_LANGUAGE_KEY") or 
               os.getenv("AZURE_KEY") or 
               os.getenv("LANGUAGE_KEY"))
        
        # error messages for debugging
        if not endpoint:
            print("ERROR: Azure endpoint not found!")
            print("Make sure your .env file has one of these:")
            print("  AZURE_LANGUAGE_ENDPOINT=your_endpoint_here")
            print("  AZURE_ENDPOINT=your_endpoint_here")
            print("  LANGUAGE_ENDPOINT=your_endpoint_here")
            raise ValueError("Azure endpoint not found in environment variables")
        
        if not key:
            print("ERROR: Azure key not found!")
            print("Make sure your .env file has one of these:")
            print("  AZURE_LANGUAGE_KEY=your_key_here")
            print("  AZURE_KEY=your_key_here")
            print("  LANGUAGE_KEY=your_key_here")
            raise ValueError("Azure key not found in environment variables")
        
        logger.info(f"Successfully loaded Azure config from {env_file}")
        return cls(endpoint=endpoint, key=key)
    
    def test_connection(self) -> bool:
        """Test if the Azure credentials actually work"""
        try:
            from azure.ai.textanalytics import TextAnalyticsClient
            from azure.core.credentials import AzureKeyCredential
            
            # Create test client
            client = TextAnalyticsClient(
                endpoint=self.endpoint,
                credential=AzureKeyCredential(self.key)
            )
            
            # simple operation
            test_result = client.detect_language(documents=["test connection"])
            print("✅ Azure connection test successful!")
            return True
            
        except Exception as e:
            print(f"❌ Azure connection test failed: {e}")
            logger.error(f"Azure connection test failed: {e}")
            return False
    
    def display_config_info(self):
        """Display configuration info for debugging"""
        print("=== Azure Configuration ===")
        print(f"Endpoint: {self.endpoint}")
        print(f"Key: {self.key[:8]}...{self.key[-4:]} (length: {len(self.key)})")
        print("=" * 30)

def load_azure_config_simple():
    """Function to load Azure config"""
    load_dotenv()
    
    endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
    key = os.getenv("AZURE_LANGUAGE_KEY")
    
    if not endpoint or not key:
        print("❌ Missing Azure credentials!")
        print("Create a .env file with:")
        print("AZURE_LANGUAGE_ENDPOINT=your_endpoint")
        print("AZURE_LANGUAGE_KEY=your_key")
        return None
    
    print(f"✅ Loaded Azure config (endpoint: {endpoint[:30]}...)")
    return {"endpoint": endpoint, "key": key}

if __name__ == "__main__":
    print("Testing Azure configuration...")
    try:
        config = AzureConfig.from_env()
        config.display_config_info()
        
        # Test connection 
        if config.test_connection():
            print("🎉 Everything looks good!")
        else:
            print("⚠️ Connection test failed - check your credentials")
            
    except Exception as e:
        print(f"Failed to load config: {e}")