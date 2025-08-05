# 🧠 Moodify

**Mood Analysis Powered by Azure AI Language Service**

Moodify is an intelligent mood analysis application that uses Microsoft Azure's AI Language Service to analyze text input and provide personalized recommendations based on detected emotions. Whether you're journaling, seeking mood insights, or looking for tailored suggestions, Moodify helps you understand and respond to your emotional state.

Try out the app : https://moooodify.streamlit.app/


## ✨ Features

### **Comprehensive Text Analysis**
- **Sentiment Analysis**: Detect positive, neutral, and negative sentiments with confidence scores
- **Key Phrase Extraction**: Identify the most important phrases and topics
- **Named Entity Recognition**: Extract people, places, organizations, and other entities
- **Language Detection**: Automatically identify the language of your text
- **PII Detection**: Identify and protect personally identifiable information

### **Emotion Detection**
- Advanced emotion mapping using keyword analysis and sentiment scores
- Detects: Joy, Sadness, Anger, Fear, Surprise, Disgust, and Neutral states
- Combines Azure AI results with custom emotion classification

### **Personalized Recommendations**
Based on your detected emotion, get tailored suggestions for:
- **🎵 Music Playlists**: Curated Spotify playlists to match or improve your mood
- **📚 Inspirational Quotes**: Motivational and relevant quotes
- **🏃 Activities**: Suggested actions to help process or enhance your emotional state



## Quick Start

### Prerequisites
- Python 3.8 or higher
- Azure for Students Subscription
- Required Python packages (see requirements below)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/saishagoel27/moodify
   cd moodify
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit azure-ai-textanalytics python-dotenv
   ```

3. **Set up Azure credentials**
   
   Create a `.env` file in the project root:
   ```env
   AZURE_LANGUAGE_ENDPOINT="your_azure_endpoint_here"
   AZURE_LANGUAGE_KEY="your_azure_key_here"
   ```

   To get these credentials:
   - Go to [Azure Portal](https://portal.azure.com)
   - Create your Language Service resource
   - Copy the endpoint and key from the "Keys and Endpoint" section

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501` to start using Moodify!

## 📖 Usage Guide

### Basic Usage
1. **Enter your text**: Describe your mood, feelings, or experiences in the text area
2. **Choose recommendation type**: Select whether you want song, quote, or activity suggestions
3. **Analyze**: Click "Analyze Mood" to get comprehensive results
4. **Explore results**: View your detected emotion and browse detailed analysis

### Example Inputs
- *"Today was challenging but rewarding. I completed a major project at work, but I'm feeling anxious about the presentation tomorrow."*
- *"I'm so excited about my upcoming vacation! Everything is going perfectly."*
- *"I've been feeling down lately and need some motivation to get back on track."*

### Features Configuration
- **Sentiment Analysis**: Overall emotional tone detection
- **Key Phrase Extraction**: Important topics and themes
- **Entity Recognition**: People, places, and organisations mentioned
- **Language Detection**: Automatic language identification
- **PII Detection**: Privacy-focused personal information detection

## 🏗️ Project Structure

```
moodify/
├── main.py                 # Main Streamlit application
├── azure_service.py        # Azure AI Language Service integration
├── config.py              # Configuration management
├── emotion_analyzer.py     # Emotion detection and mapping
├── recommendations.py      # Mood-based recommendation engine
├── test.py                # Simple testing script
├── .env                   # Environment variables (create this)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### Core Components

#### `AzureTextAnalyzer`
Handles all Azure AI Language Service operations including sentiment analysis, key phrase extraction, entity recognition, language detection, and PII detection.

#### `EmotionAnalyzer`
Maps Azure analysis results to specific emotions using keyword matching and sentiment score thresholds.

#### `RecommendationEngine`
Provides curated recommendations (music, quotes, activities) based on detected emotions.


## 🧪 Testing

Run the simple test script to verify your Azure connection:
```bash
python test.py
```


## 📄 License

This project is licensed under the MIT License - free to use and modify


Try Moodify with these sample texts:

**Positive Mood:**
> "I just got promoted at work! I'm so grateful for this opportunity and excited about the new challenges ahead."

**Mixed Emotions:**
> "Moving to a new city is exciting but also nerve-wracking. I'm looking forward to new adventures but worried about leaving friends behind."

**Seeking Support:**
> "I've been struggling with motivation lately. Work feels overwhelming and I'm not sure how to get back on track."

---

**Built with ❤️ using Azure AI and Streamlit**

*Moodify - Understanding emotions, one text at a time.*
