#Importing necessary libraries
from dotenv import load_dotenv
import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Loading credentials
load_dotenv()
endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
key = os.getenv("AZURE_LANGUAGE_KEY")

# Creating client
client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Function to analyze sentiment
def analyze_sentiment(text: str):
    docs = [text]
    result = client.analyze_sentiment(documents=docs)[0]
    return result.sentiment, result.confidence_scores

# Main function to run the app
if __name__ == "__main__":
    text = input("How are you feeling? ")
    sentiment, scores = analyze_sentiment(text)
    print(f"Overall sentiment: {sentiment}")
    print(f"Scores ➤ Positive: {scores.positive:.2f}, Neutral: {scores.neutral:.2f}, Negative: {scores.negative:.2f}")
