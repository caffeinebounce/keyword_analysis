import json, nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download("stopwords")
nltk.download("punkt")

def extract_keywords(text, top_n=10):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)

    words = [word.lower() for word in words if word.isalnum()]
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
