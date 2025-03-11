import argparse
from fetch_reviews import fetch_reviews
from process_reviews import analyze_sentiment, extract_words
from generate_report import plot_final_report


def main():
    # parser = argparse.ArgumentParser(description='Fetch and analyze IMDb reviews.')
    # parser.add_argument('url', type=str, help='The IMDb URL to fetch reviews from')
    # args = parser.parse_args()

    # url = args.url
    url = "https://www.imdb.com/title/tt0995832/reviews/?ref_=tt_ururv_sm"

    if 'imdb.com' not in url:
        print("Invalid URL. Please provide a valid IMDb URL.")
        return

    print(f"Fetching reviews from: {url}\\n")
    reviews, title = fetch_reviews(url)

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
