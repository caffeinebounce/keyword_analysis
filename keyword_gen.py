import json, nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download("stopwords")
nltk.download("punkt")
nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer

def extract_keywords(text, top_n=10):
    # Load custom e-commerce common words
    with open('filter_list.txt', 'r') as f:
        ecommerce_common_words = set(word.strip() for word in f.readlines())

    stop_words = set(stopwords.words("english"))

    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    
    # Lemmatize custom e-commerce common words
    ecommerce_common_words = set(lemmatizer.lemmatize(word) for word in ecommerce_common_words)

    # Update the stopwords list with the custom e-commerce words
    stop_words.update(ecommerce_common_words)

    words = word_tokenize(text)

    # Filter out words that are not alphabetic
    words = [word.lower() for word in words if word.isalpha()]

    # Lemmatize words in the text
    words = [lemmatizer.lemmatize(word) for word in words]
    
    # Remove stopwords
    words = [word for word in words if word not in stop_words]

    freq = Counter(words)
    keywords = freq.most_common(top_n)

    return keywords

# Load the scraped data
with open("ecommerce_crawler/output.json", "r") as f:
    scraped_data = json.load(f)

# Combine all the text from the scraped pages
all_text = ' '.join([item['text'] for item in scraped_data])

# Extract keywords
keywords = extract_keywords(all_text)

print("Keywords:")
for keyword, frequency in keywords:
    print(f"{keyword}: {frequency}")
