import matplotlib.pyplot as plt
from wordcloud import WordCloud
import textwrap


def generate_wordcloud(words, title):
    """Generates a word cloud with horizontal words only."""
    wordcloud = WordCloud(width=500, height=250, background_color='white', prefer_horizontal=1.0).generate_from_frequencies(words)
    
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=14, fontweight='bold')

# Function to wrap text and determine row height dynamically
def wrap_text_and_get_height(text, width, line_height_factor=0.5):
    wrapped_text = "\n".join(textwrap.wrap(text, width))
    num_lines = wrapped_text.count("\n") + 1  # Count the number of lines
    row_height = 1.2 + (num_lines * line_height_factor)  # Adjust height based on lines
    return wrapped_text, row_height

def plot_final_report(url, title, sentiment_counts, most_used_words, longest_words):
    """Plots the final report with sentiment breakdown, word cloud, and most used words."""

    fig, axs = plt.subplots(6, 1, figsize=(11, 9))

    # First Table
    axs[0].axis('off')  # Hide axes
    table_data = [
        ["URL", url],
        ["Title", title],
        ["Number of Reviews", sum(sentiment_counts.values())],
        ["Sentiment", sentiment_counts],
    ]

    table = axs[0].table(cellText=table_data, colWidths=[0.2, 0.8], cellLoc='left', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 3)  # Scale table size

    # First Word Cloud
    plt.sca(axs[1])  # Select second subplot
    generate_wordcloud(sentiment_counts, "Sentiment Word Cloud")









    # Second Table
    most_used_words_str = ', '.join([f"{word} → {count}" for word, count in most_used_words])
    wrapped_text, row_height = wrap_text_and_get_height(most_used_words_str, width=100)  # Wrap & Get Dynamic Height

    axs[2].axis('off')  # Hide axes
    table_data_bottom = [
        ["30 Most used words", wrapped_text],
    ]

    table_bottom = axs[2].table(cellText=table_data_bottom, colWidths=[0.2, 0.8], cellLoc='left', loc='center')
    table_bottom.auto_set_font_size(False)
    table_bottom.set_fontsize(10)


    table_bottom.scale(1.2, row_height * 2.5)

    # Second Word Cloud
    plt.sca(axs[3])  # Select second subplot
    generate_wordcloud(dict(most_used_words), "30 Most Used Words Cloud")













    # Third Table
    longest_words_str = ', '.join([f"{word} → {count}" for word, count in longest_words])
    wrapped_text_longest, row_height_longest = wrap_text_and_get_height(longest_words_str, width=100)
    axs[4].axis('off')  # Hide axes
    table_data_bottom = [
        ["30 Longest words", wrapped_text_longest],
    ]

    table_bottom = axs[4].table(cellText=table_data_bottom, colWidths=[0.2, 0.8], cellLoc='left', loc='center')
    table_bottom.auto_set_font_size(False)
    table_bottom.set_fontsize(10)

    table_bottom.scale(1.2, row_height_longest * 3)

    # Third Word Cloud
    plt.sca(axs[5])  # Select second subplot
    longest_words_dict = {word: 1 for word in longest_words}
    generate_wordcloud(dict(longest_words), "30 Longest Words Cloud")

    # Adjust layout & show
    plt.tight_layout()
    plt.show()
