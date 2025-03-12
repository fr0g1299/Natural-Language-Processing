import matplotlib.pyplot as plt
from wordcloud import WordCloud
import textwrap


def generate_wordcloud(words, title, ax):
    """Generates a word cloud with horizontal words only."""

    wordcloud = WordCloud(width=500, height=300, prefer_horizontal=1.0, colormap='Dark2', background_color='#333333').generate_from_frequencies(words)

    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(title, fontsize=14, fontweight='bold', color='#eeeeee')

# Function to wrap text and determine row height dynamically
def wrap_text_and_get_height(text, width):
    """Wraps text to a specified width and determines the row height dynamically."""

    wrapped_text = "\n".join(textwrap.wrap(text, width))
    num_lines = wrapped_text.count("\n") + 1  # Count the number of lines

    row_height = 0.02 + (num_lines * 0.02)  # Adjust height based on lines
    return wrapped_text, row_height

def plot_final_report(url, title, sentiment_counts, most_used_words, longest_words):
    """Plots the final report with sentiment breakdown, most used words, longest words and word clouds."""

    # Convert sentiment counts to string
    sentiment_counts_str = ', '.join([f"{key} → {value}" for key, value in sentiment_counts.items()])

    # Wrap & Get Dynamic Height
    most_used_words_str = ', '.join([f"{word} → {count}" for word, count in most_used_words])
    wrapped_text, row_height = wrap_text_and_get_height(most_used_words_str, width=100)

    longest_words_str = ', '.join([f"{word} → {count}" for word, count in longest_words])
    wrapped_text_longest, row_height_longest = wrap_text_and_get_height(longest_words_str, width=100)

    fig, axs = plt.subplots(1, 2, figsize=(20, 11))

    fig.patch.set_facecolor('#333333')  # Dark background for the whole figure
    for ax in axs:
        ax.axis('off')  # Hide axis lines

    # Table
    table_data = [
        ["Title", f"$\\bf{{{title.replace(' ', '\\ ')}}}$"],
        ["URL", url],
        ["Number of Reviews", sum(sentiment_counts.values())],
        ["Sentiment", sentiment_counts_str],
        ["30 Most used words", wrapped_text],
        ["30 Longest words", wrapped_text_longest],
    ]

    table = axs[0].table(cellText=table_data, colWidths=[0.2, 0.8], cellLoc='left', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)

    # Dark mode for the table
    for key, cell in table.get_celld().items():
        cell.set_facecolor('#333333')
        cell.set_text_props(color='#eeeeee')

    # Adjust the row heights for bottom two rows
    table[(4, 0)].set_height(row_height)
    table[(4, 1)].set_height(row_height)
    table[(5, 0)].set_height(row_height_longest)
    table[(5, 1)].set_height(row_height_longest)

    # Word Clouds
    ax_wordcloud1 = fig.add_axes([0.7, 0.65, 0.23, 0.34])
    generate_wordcloud(sentiment_counts, "Sentiment Word Cloud", ax_wordcloud1)

    ax_wordcloud2 = fig.add_axes([0.7, 0.35, 0.23, 0.34])
    generate_wordcloud(dict(most_used_words), "30 Most Used Words Cloud", ax_wordcloud2)

    ax_wordcloud3 = fig.add_axes([0.7, 0, 0.23, 0.34])
    word_lengths = {word: len(word) for word, count in longest_words}
    generate_wordcloud(word_lengths, "30 Longest Words Cloud", ax_wordcloud3)

    # Adjust layout to remove blank spaces
    plt.subplots_adjust(left=0.03, right=1.4, top=0.95, bottom=0.05)

    # Lock window size by setting a fixed aspect ratio
    manager = plt.get_current_fig_manager()
    if hasattr(manager, 'window'):
        try:
            manager.window.resizable(False, False)  # Disable resizing
        except AttributeError:
            pass

    plt.show()
