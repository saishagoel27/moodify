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
        logger.error(f"Azure client initialization failed: {e}")
        return None

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Moodify",
        page_icon="🧠",
        layout="wide"
    )
    
    # Initialize session state for clear functionality
    if 'user_text' not in st.session_state:
        st.session_state.user_text = ""
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    if 'last_emotion' not in st.session_state:
        st.session_state.last_emotion = ""
    if 'last_recommendation' not in st.session_state:
        st.session_state.last_recommendation = ""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    
    # Initialize Azure client
    azure_client = initialize_azure_client()
    if not azure_client:
        st.stop()
    
    # Fixed CSS with proper text colors - specifically fixing emotion box text
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            color: #1E88E5;
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }
        .emotion-box {
            padding: 1rem;
            border-radius: 8px;
            background-color: #e3f2fd;
            border-left: 5px solid #1E88E5;
            margin: 1rem 0;
            color: #000000 ;
        }
        .emotion-box h2 {
            color: #000000 ;
            margin: 0;
        }
        .emotion-box p {
            color: #666666 ;
            margin: 0.5rem 0 0 0;
        }
        .recommendation-box {
            background-color: #f0f8ff;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #1E88E5;
            color: #000000;
            margin: 1rem 0;
        }
        .recommendation-box h3 {
            color: #1E88E5 ;
            margin-bottom: 0.5rem;
        }
        .recommendation-box p {
            color: #000000 ;
            margin: 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">🧠 Moodify</h1>', unsafe_allow_html=True)
    st.markdown("**Mood analysis powered by Azure AI Language Service**")
    
    # Sidebar
    st.sidebar.header("🔧 Settings")
    
    recommendation_type = st.sidebar.selectbox(
        "What do you want?",
        ["songs", "quotes", "activities"],
        help="Pick your recommendation type"
    )
    
    # Feature toggles in expander
    with st.sidebar.expander("🔬 Advanced Features"):
        show_sentiment = st.checkbox("Sentiment Analysis", value=True)
        show_keyphrases = st.checkbox("Key Phrases", value=True)
        show_entities = st.checkbox("Named Entities", value=False)
        show_language = st.checkbox("Language Detection", value=False)
        show_pii = st.checkbox("PII Detection", value=False)
    
    # Main input area
    st.subheader("💭 How are you feeling?")
    user_text = st.text_area(
        "Tell me about your mood:",
        value=st.session_state.user_text,
        placeholder="I'm feeling excited about my new project but also a bit anxious about the deadline...",
        height=100,
        help="Describe your emotions, experiences, or thoughts",
        key="text_input"
    )
    
    # Action buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        analyze_button = st.button("🔍 Analyze My Mood", type="primary")
    with col2:
        # Random recommendation feature
        if st.button("🎲 Random"):
            emotions = ["joy", "sadness", "anger", "fear", "surprise", "neutral"]
            import random
            random_emotion = random.choice(emotions)
            rec = RecommendationEngine.get_recommendation(random_emotion, recommendation_type)
            st.info(f"**Random {recommendation_type}:** {rec}")
    with col3:
        # Enhanced clear button functionality
        if st.button("🗑️ Clear"):
            # Clear all session state
            st.session_state.user_text = ""
            st.session_state.show_results = False
            st.session_state.last_emotion = ""
            st.session_state.last_recommendation = ""
            st.session_state.analysis_results = None
            st.rerun()
    
    # Update session state with current text
    st.session_state.user_text = user_text
    
    # Main analysis logic
    if analyze_button:
        if not user_text.strip():
            st.warning("⚠️ Please enter some text first!")
            return
            
        with st.spinner("Analyzing with Azure AI..."):
            try:
                # Get Azure analysis
                analysis_results = azure_client.analyze_text_comprehensive(user_text)
                
                if not analysis_results:
                    st.error("❌ Analysis failed. Check your Azure connection.")
                    return
                
                # Get emotion
                primary_emotion = EmotionAnalyzer.determine_primary_emotion(analysis_results)
                
                # Store results in session state
                st.session_state.last_emotion = primary_emotion
                st.session_state.show_results = True
                st.session_state.analysis_results = analysis_results
                
                # Display main result
                display_main_result(primary_emotion, recommendation_type)
                
                # Show detailed analysis if requested
                if any([show_sentiment, show_keyphrases, show_entities, show_language, show_pii]):
                    display_detailed_analysis(analysis_results, show_sentiment, show_keyphrases, 
                                            show_entities, show_language, show_pii)
                
            except Exception as e:
                logger.error(f"Analysis error: {e}")
                st.error(f"❌ Something went wrong: {str(e)}")
    
    # Display previous results
    elif st.session_state.show_results and st.session_state.last_emotion:
        display_main_result(st.session_state.last_emotion, recommendation_type)
        
        # Show detailed analysis if requested and data exists
        if (st.session_state.analysis_results and 
            any([show_sentiment, show_keyphrases, show_entities, show_language, show_pii])):
            display_detailed_analysis(st.session_state.analysis_results, show_sentiment, show_keyphrases, 
                                    show_entities, show_language, show_pii)

def display_main_result(emotion, rec_type):
    """Show the main emotion and recommendation"""
    
    # Emotion result with fixed text color
    st.markdown(f"""
    <div class="emotion-box">
        <h2>🎭 Detected Emotion: <span style="text-transform: uppercase; color: #000000 !important;">{emotion}</span></h2>
        <p style="color: #666666 !important;">Based on Azure AI Language Service analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get recommendation
    recommendation = RecommendationEngine.get_recommendation(emotion, rec_type)
    st.session_state.last_recommendation = recommendation
    
    st.markdown(f"""
    <div class="recommendation-box">
        <h3 style="color: #1E88E5 !important;">💡 {rec_type.title()} Recommendation:</h3>
        <p style="color: #000000 !important;">{recommendation}</p>
    </div>
    """, unsafe_allow_html=True)

def display_detailed_analysis(analysis_results, show_sentiment, show_keyphrases, 
                            show_entities, show_language, show_pii):
    """Display detailed Azure AI analysis results"""
    
    st.subheader("📊 Detailed Analysis")
    
    # Two column layout for better organization
    col1, col2 = st.columns(2)
    
    with col1:
        # Sentiment analysis
        if show_sentiment and 'sentiment' in analysis_results:
            with st.expander("💭 Sentiment Analysis", expanded=True):
                sentiment_data = analysis_results['sentiment']
                
                # Show scores as metrics
                score_cols = st.columns(3)
                scores = sentiment_data['scores']
                
                with score_cols[0]:
                    st.metric("Positive", f"{scores['positive']:.2f}")
                with score_cols[1]:
                    st.metric("Neutral", f"{scores['neutral']:.2f}")
                with score_cols[2]:
                    st.metric("Negative", f"{scores['negative']:.2f}")
                
                st.write(f"**Overall:** {sentiment_data['label'].title()}")
        
        # Key phrases
        if show_keyphrases and 'key_phrases' in analysis_results:
            with st.expander("🔑 Key Phrases", expanded=True):
                phrases = analysis_results['key_phrases']
                if phrases:
                    for i, phrase in enumerate(phrases[:8], 1):  
                        st.write(f"**{i}.** {phrase}")
                else:
                    st.write("No key phrases found")
    
    with col2:
        # Named entities
        if show_entities and 'entities' in analysis_results:
            with st.expander("🏷️ Named Entities", expanded=True):
                entities = analysis_results['entities']
                if entities:
                    for text, category, confidence in entities[:10]:  
                        st.write(f"**{text}** ({category}) - {confidence:.2f}")
                else:
                    st.write("No entities detected")
        
        # Language detection
        if show_language and 'language' in analysis_results:
            with st.expander("🌍 Language", expanded=True):
                lang_data = analysis_results['language']
                st.write(f"**Language:** {lang_data['name']} ({lang_data['code']})")
                st.write(f"**Confidence:** {lang_data['confidence']:.2f}")
    
    # PII detection 
    if show_pii and 'pii_entities' in analysis_results:
        with st.expander("🔒 Privacy Check"):
            pii_entities = analysis_results['pii_entities']
            if pii_entities:
                st.warning("⚠️ Personal information detected:")
                for text, category in pii_entities:
                    st.write(f"- **{text}** (Type: {category})")
            else:
                st.success("✅ No personal information found")

if __name__ == "__main__":
    main()