"""
LDA Topic Modeling Script
Author: Sol Stappard
Course: POLI30300
"""

import pandas as pd
import re
import nltk
import random
import numpy as np

from collections import defaultdict
from datetime import datetime

from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.models.coherencemodel import CoherenceModel
import pyLDAvis.gensim_models as gensimvis  # optional for visualization

from nltk.corpus import stopwords

# ---------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------

# Download NLTK stopwords (only runs once)
nltk.download('stopwords')

# Set random seeds for reproducibility
random.seed(42)
np.random.seed(42)

# Load English stopwords and extend with custom stopwords
stop_words = set(stopwords.words("english"))
custom_stop_words = {
    "according", "said", "also", "new", "percent", "th",
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself", "she", "her", "hers", "herself",
    "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    "what", "which", "who", "whom", "this", "that", "these", "those",
    "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing",
    "a", "an", "the", "but", "if", "or", "because", "as", "until", "while",
    "of", "at", "by", "for", "with", "about", "against", "between", "into",
    "through", "during", "before", "after", "above", "below", "to", "from",
    "up", "down", "in", "out", "on", "off", "over", "under",
    "again", "further", "then", "once", "here", "there",
    "when", "where", "why", "how", "all", "any", "both", "each", "few",
    "more", "most", "other", "some", "such", "no", "nor", "not", "only",
    "own", "same", "so", "than", "too", "very", "s", "t", "can", "will",
    "just", "don", "should", "now", "two", "day", "week", "three", "month",
    "research", "showed", "year", "held", "first", "many", "open", "last",
    "monday", "one"
}
stop_words = stop_words.union(custom_stop_words)

# ---------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------


def load_and_preprocess_text(csv_file):
    """
    Load articles from CSV and preprocess into tokenized documents.
    Returns:
        documents: list of token lists
        metadata: list of dicts with date/title
    """
    documents = []
    metadata = []

    df = pd.read_csv(csv_file)

    for index, row in df.iterrows():
        text = str(row["content"])

        # Try parsing dates with multiple formats
        try:
            date = pd.to_datetime(row["date"],
                                  format="%H:%M, %B %d, %Y",
                                  errors="coerce")
            if pd.isna(date):
                date = pd.to_datetime(row["date"],
                                      format="%B %d, %Y",
                                      errors="coerce")
        except Exception:
            date = None

        title = str(row["title"]) if "title" in df.columns else f"Untitled Article {index}"

        metadata.append({"date": date, "title": title})

        # Text preprocessing
        text = text.lower()
        text = re.sub(r"[^a-z\s]", "", text)
        tokens = [word for word in text.split() if word not in stop_words and len(word) > 1]

        documents.append(tokens)

    return documents, metadata


def prepare_corpus(documents):
    """
    Create dictionary and BoW corpus for LDA.
    """
    dictionary = corpora.Dictionary(documents)
    dictionary.add_documents([[]])
    dictionary.filter_extremes(no_below=5, no_above=0.45)
    corpus = [dictionary.doc2bow(doc) for doc in documents]
    return dictionary, corpus


def perform_topic_analysis(corpus, dictionary, num_topics=10):
    """
    Train LDA model and print topics.
    """
    lda_model = LdaModel(
        corpus=corpus,
        num_topics=num_topics,
        id2word=dictionary,
        passes=10,
        random_state=42
    )

    topics = lda_model.show_topics(
        num_topics=num_topics, num_words=10, formatted=False
    )

    for topic_num, topic_words in topics:
        words = ", ".join([word for word, prob in topic_words])
        print(f"Topic {topic_num}: {words}")

    return lda_model, topics


def calculate_coherence(lda_model, texts, dictionary, coherence="c_v"):
    """
    Compute coherence score for LDA model.
    """
    coherence_model = CoherenceModel(
        model=lda_model,
        texts=texts,
        dictionary=dictionary,
        coherence=coherence
    )
    return coherence_model.get_coherence()


def get_top_articles_by_topic(lda_model, corpus, metadata, num_topics, top_n=10):
    """
    Retrieve top article titles most associated with each topic.
    Returns:
        dict: topic_id -> list of (title, probability)
    """
    topic_articles = defaultdict(list)

    for i, bow in enumerate(corpus):
        topic_distribution = lda_model.get_document_topics(bow)
        for topic_id, prob in topic_distribution:
            topic_articles[topic_id].append((i, prob))

    # Print article count per topic
    for topic_id in range(num_topics):
        count = len(topic_articles[topic_id])
        print(f"Topic {topic_id} is associated with {count} articles")

    top_titles = {}
    for topic_id in range(num_topics):
        sorted_articles = sorted(
            topic_articles[topic_id],
            key=lambda x: x[1],
            reverse=True
        )[:top_n]

        titles_probs = [
            (metadata[i]["title"], prob) for i, prob in sorted_articles
        ]
        top_titles[topic_id] = titles_probs

    return top_titles


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

if __name__ == "__main__":
    # Path to CSV file
    csv_file = "C:/Users/sol stappard/PycharmProjects/pythonProject/web_Scraper/updated_articles_cleaned_date_for_text.csv"

    # Load and preprocess
    documents, metadata = load_and_preprocess_text(csv_file)
    dictionary, corpus = prepare_corpus(documents)

    # Number of topics
    num_topics = 10
    print(f"\nRunning LDA with {num_topics} topics...")

    lda_model, topics = perform_topic_analysis(corpus, dictionary, num_topics=num_topics)

    # Calculate coherence
    coherence_score = calculate_coherence(lda_model, documents, dictionary)
    print(f"\nCoherence Score for {num_topics} topics: {coherence_score:.4f}")

    # Get top article titles
    top_titles_by_topic = get_top_articles_by_topic(
        lda_model, corpus, metadata, num_topics=num_topics, top_n=10
    )

    for topic_id, titles_probs in top_titles_by_topic.items():
        print(f"\nTop 10 article titles for Topic {topic_id}:")
        for title, prob in titles_probs:
            print(f" - {title} (association score: {prob:.4f})")
