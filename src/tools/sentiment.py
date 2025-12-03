"""
Sentiment Analysis Tool

A simple sentiment analysis tool for demonstration purposes.
In production, this would use a proper NLP model or API.
"""

from langchain_core.tools import tool


@tool
def analyze_sentiment(text: str) -> str:
    """Analyze the sentiment of text. Returns positive, negative, or neutral.
    
    Args:
        text: The text to analyze for sentiment
        
    Returns:
        A sentiment classification (Positive, Negative, or Neutral)
        
    Example:
        >>> analyze_sentiment("This is an amazing product!")
        "Sentiment: Positive"
        
    Note:
        This is a simple keyword-based implementation for demonstration.
        Production systems should use proper NLP models like:
        - Hugging Face Transformers (e.g., distilbert-base-uncased-finetuned-sst-2-english)
        - OpenAI API
        - Google Cloud Natural Language API
    """
    # Simple sentiment analysis simulation
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 
                      'fantastic', 'love', 'best', 'awesome', 'perfect']
    negative_words = ['bad', 'terrible', 'awful', 'poor', 'horrible', 
                      'worst', 'hate', 'disappointing', 'useless', 'trash']
    
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        return "Sentiment: Positive"
    elif neg_count > pos_count:
        return "Sentiment: Negative"
    else:
        return "Sentiment: Neutral"
