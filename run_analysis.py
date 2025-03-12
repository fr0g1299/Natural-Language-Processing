import argparse
from fetch_reviews import fetch_reviews
from process_reviews import analyze_sentiment, extract_words
from generate_report import plot_final_report


def main():
    parser = argparse.ArgumentParser(description='Fetch and analyze IMDb reviews.')
    parser.add_argument('url', type=str, help='The IMDb URL to fetch reviews from')
    parser.add_argument('--limit', type=int, default=1000, help='The limit of reviews to fetch (default: 1000). Use -1 to fetch all reviews.')
    args = parser.parse_args()

    url = args.url
    limit = args.limit

    if 'imdb.com' not in url:
        print("Invalid URL. Please provide a valid IMDb URL.")
        return

    if limit < 25 and limit != -1:
        print("The limit should be at least 25 or -1 to fetch all reviews.")
        return

    print(f"Fetching reviews from: {url}\n")
    reviews, title = fetch_reviews(url, limit)

    if not reviews:
        print("No reviews found.")
        return

    # Analyze sentiment
    sentiment_counts = analyze_sentiment(reviews)
    most_common_words, longest_words = extract_words(reviews)

    # Print the report
    plot_final_report(url, title, sentiment_counts, most_common_words, longest_words)


if __name__ == "__main__":
    main()
