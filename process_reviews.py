import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter


# Check if the necessary NLTK data files are already downloaded
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    print("Downloading NLTK data files...")
    nltk.download('vader_lexicon')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading NLTK data files...")
    nltk.download('punkt')

def analyze_sentiment(reviews):
    """Analyzes sentiment of reviews and returns a breakdown."""

    sia = SentimentIntensityAnalyzer()
    sentiment_counts = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
    sentiment_scores = []

    # Analyze sentiment for each review
    for review in reviews:
        score = sia.polarity_scores(review)
        sentiment_scores.append(score)

        if score['compound'] >= 0.05:
            sentiment_counts['Positive'] += 1
        elif score['compound'] <= -0.05:
            sentiment_counts['Negative'] += 1
        else:
            sentiment_counts['Neutral'] += 1

    return sentiment_counts

def extract_words(reviews):
    """Extracts the most frequently used and longest words from the reviews."""

    all_words = nltk.word_tokenize(' '.join(reviews).lower())
    words_filtered = [word for word in all_words if word.isalpha()]  # Remove non-alphabetic characters

    # Get the most common words
    most_common_words = Counter(words_filtered).most_common(30)

    # Get the longest words
    longest_words = sorted(set(words_filtered), key=len, reverse=True)[:30]
    longest_words = [(word, words_filtered.count(word)) for word in longest_words]

    return most_common_words, longest_words
