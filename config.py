import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional

@dataclass
class AzureConfig:
    """Configuration class for Azure AI services"""
    endpoint: str
    key: str
    
    @classmethod
    def from_env(cls) -> 'AzureConfig':
        """Load configuration from environment variables"""
        load_dotenv()
        endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
        key = os.getenv("AZURE_LANGUAGE_KEY")
        
        if not endpoint or not key:
            raise ValueError("Azure credentials not found in environment variables")
        
        return cls(endpoint=endpoint, key=key)