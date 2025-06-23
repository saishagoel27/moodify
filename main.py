import streamlit as st
from config import AzureConfig
from azure_service import AzureTextAnalyzer
from emotion_analyzer import EmotionAnalyzer
from recommend import RecommendationEngine
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@st.cache_resource
def initialize_azure_client():
    """Initialize Azure client with caching for performance"""
    try:
        config = AzureConfig.from_env()
        return AzureTextAnalyzer(config)
    except Exception as e:
        st.error(f"Failed to initialize Azure client: {e}")
        return None

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Moodify",
        page_icon="🧠",
        layout="wide"
    )
    
    # Initialize Azure client
    azure_client = initialize_azure_client()
    if not azure_client:
        st.stop()
    
    # Custom CSS
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            color: #1E88E5;
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }
        .analysis-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            margin: 1rem 0;
        }
        .feature-box {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #1E88E5;
            margin: 0.5rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">🧠 Moodify</h1>', unsafe_allow_html=True)
    st.markdown("**Mood analysis powered by Azure AI Language Service**")
    
    # Sidebar configuration
    st.sidebar.header("🔧 Configuration")
    
    # Feature toggles
    show_sentiment = st.sidebar.checkbox("Sentiment Analysis", value=True)
    show_keyphrases = st.sidebar.checkbox("Key Phrase Extraction", value=True)
    show_entities = st.sidebar.checkbox("Entity Recognition", value=True)
    show_language = st.sidebar.checkbox("Language Detection", value=True)
    show_pii = st.sidebar.checkbox("PII Detection", value=False, 
                                  help="Detect personally identifiable information")
    
    recommendation_type = st.sidebar.selectbox(
        "Recommendation Type",
        ["songs", "quotes", "activities"],
        help="Choose what type of recommendation you'd like"
    )
    
    # Main input area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💭 Share your thoughts:")
        user_text = st.text_area(
            "Describe your mood, feelings, or experiences:",
            placeholder="Today was challenging but rewarding. I completed a major project at work, but I'm feeling anxious about the presentation tomorrow...",
            height=120,
            key="user_input"
        )
    
    with col2:
        st.subheader("🎯 Quick Actions")
        analyze_button = st.button("🔍 Analyze Mood", type="primary", use_container_width=True)
        
        if st.button("🎲 Random Recommendation", use_container_width=True):
            import random
            random_emotion = random.choice(list(RecommendationEngine.RECOMMENDATIONS.keys()))
            random_rec = RecommendationEngine.get_recommendation(random_emotion, recommendation_type)
            st.info(f"**Random {recommendation_type.title()}:** {random_rec}")
    
    # Analysis execution
    if analyze_button:
        if not user_text.strip():
            st.error("⚠️ Please enter some text to analyze.")
        else:
            with st.spinner("🔄 Running comprehensive Azure AI analysis..."):
                try:
                    # Perform analysis
                    analysis_results = azure_client.analyze_text_comprehensive(user_text)
                    
                    if not analysis_results:
                        st.error("❌ Analysis failed. Please try again.")
                        return
                    
                    # Determine emotion
                    primary_emotion = EmotionAnalyzer.determine_primary_emotion(analysis_results)
                    
                    # Display results
                    display_results(analysis_results, primary_emotion, recommendation_type,
                                  show_sentiment, show_keyphrases, show_entities, 
                                  show_language, show_pii)
                    
                except Exception as e:
                    logger.error(f"Analysis error: {e}")
                    st.error(f"❌ An error occurred during analysis: {str(e)}")

def display_results(analysis_results, primary_emotion, recommendation_type,
                   show_sentiment, show_keyphrases, show_entities, 
                   show_language, show_pii):
    """Display analysis results in organized sections"""
    
    # Primary emotion and recommendation
    st.markdown(f"""
    <div class="analysis-card">
        <h2>🎯 Detected Emotion: {primary_emotion.upper()}</h2>
        <p>Based on advanced Azure AI analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get and display recommendation
    recommendation = RecommendationEngine.get_recommendation(primary_emotion, recommendation_type)
    st.success(f"**{recommendation_type.title()} Recommendation:** {recommendation}")
    
    # Detailed analysis sections
    st.subheader("📊 Detailed Analysis")
    
    # Create columns for organized display
    col1, col2 = st.columns(2)
    
    with col1:
        # Sentiment Analysis
        if show_sentiment and 'sentiment' in analysis_results:
            with st.expander("💭 Sentiment Analysis", expanded=True):
                sentiment_data = analysis_results['sentiment']
                
                # Metrics
                score_cols = st.columns(3)
                with score_cols[0]:
                    st.metric("Positive", f"{sentiment_data['scores']['positive']:.2f}")
                with score_cols[1]:
                    st.metric("Neutral", f"{sentiment_data['scores']['neutral']:.2f}")
                with score_cols[2]:
                    st.metric("Negative", f"{sentiment_data['scores']['negative']:.2f}")
                
                st.write(f"**Overall Sentiment:** {sentiment_data['label'].title()}")
        
        # Key Phrases
        if show_keyphrases and 'key_phrases' in analysis_results:
            with st.expander("🔑 Key Phrases", expanded=True):
                key_phrases = analysis_results['key_phrases']
                if key_phrases:
                    for i, phrase in enumerate(key_phrases, 1):
                        st.write(f"{i}. **{phrase}**")
                else:
                    st.write("No key phrases detected")
    
    with col2:
        # Entity Recognition
        if show_entities and 'entities' in analysis_results:
            with st.expander("🏷️ Named Entities", expanded=True):
                entities = analysis_results['entities']
                if entities:
                    for text, category, confidence in entities:
                        st.write(f"**{text}** ({category}) - {confidence:.2f}")
                else:
                    st.write("No entities detected")
        
        # Language Detection
        if show_language and 'language' in analysis_results:
            with st.expander("🌍 Language Analysis", expanded=True):
                lang_data = analysis_results['language']
                st.write(f"**Language:** {lang_data['name']} ({lang_data['code']})")
                st.write(f"**Confidence:** {lang_data['confidence']:.2f}")
    
    # PII Detection 
    if show_pii and 'pii_entities' in analysis_results:
        with st.expander("🔒 Privacy Analysis"):
            pii_entities = analysis_results['pii_entities']
            if pii_entities:
                st.warning("⚠️ Personal information detected:")
                for text, category in pii_entities:
                    st.write(f"- **{text}** (Type: {category})")
            else:
                st.success("✅ No personal information detected")

if __name__ == "__main__":
    main()