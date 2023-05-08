import json, nltk, re, os
from time import sleep  
from datetime import datetime
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from config import min_count, top, base_domain
import pandas as pd
from tabulate import tabulate

# Setting display options for fancy_grid format
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

buffer = 2

clear()

nltk.download("stopwords")
nltk.download("punkt")
nltk.download('wordnet')

sleep(buffer)
clear()

from nltk.stem import WordNetLemmatizer

def extract_bigrams(filtered_words, min_freq=min_count, stop_words=set()):
    finder = BigramCollocationFinder.from_words(filtered_words)
    finder.apply_freq_filter(min_freq)

    # Filter out bigrams containing stopwords or words from the filter list
    finder.apply_ngram_filter(lambda w1, w2: w1 in stop_words or w2 in stop_words)
    
    bigram_freq = finder.ngram_fd.items()
    return bigram_freq

def is_valid_bigram(bigram):
    invalid_punctuation = r'[•\[\]()–—]'
    return not (re.search(invalid_punctuation, bigram[0]) or re.search(invalid_punctuation, bigram[1]))

def extract_keywords(text, top_n=top, min_freq=min_count):
    with open('filter_list.txt', 'r') as f:
        ecommerce_common_words = set(word.strip() for word in f.readlines())

    stop_words = set(stopwords.words("english"))

    lemmatizer = WordNetLemmatizer()
    ecommerce_common_words = set(lemmatizer.lemmatize(word) for word in ecommerce_common_words)

    stop_words.update(ecommerce_common_words)

    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalpha()]

    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

    filtered_words = [word for word in lemmatized_words if word not in stop_words]

    keywords = Counter(filtered_words).most_common()

    bigram_freq = extract_bigrams(filtered_words)

    for bigram, freq in bigram_freq:
        keywords = [(word, count - freq if word == bigram[0] or word == bigram[1] else count) for word, count in keywords]

    filtered_keywords = [(word, count) for word, count in keywords if count >= min_freq]

    combined = filtered_keywords + [(f"{bigram[0]} {bigram[1]}", freq) for bigram, freq in bigram_freq]

    combined_sorted = sorted(combined, key=lambda x: x[1], reverse=True)[:top_n]

    return combined_sorted

with open("ecommerce_crawler/output.json", "r") as f:
    scraped_data = json.load(f)

all_text = ' '.join([item['text'] for item in scraped_data])

keywords_and_bigrams = extract_keywords(all_text)

# Print keywords and bigrams as a DataFrame
keywords_df = pd.DataFrame(keywords_and_bigrams, columns=["Keyword/Bigram", "Frequency"])
print(f"Most common keywords for {base_domain}:\n")
print(tabulate(keywords_df, headers='keys', tablefmt='fancy_grid', showindex=False))
print("\n")

sleep(buffer * 2)
clear()

# Store keywords and bigrams in a DataFrame
keywords_df = pd.DataFrame(keywords_and_bigrams, columns=["Keyword", "Frequency"])

# Create the outputs directory if it doesn't exist
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# Add ID and Domain columns
keywords_df.insert(0, "ID", keywords_df.index + 1)
keywords_df.insert(1, "Domain", base_domain)

from pytrends.request import TrendReq

# Replace 'your_account@gmail.com' and 'your_password' with your Google account credentials
pytrends = TrendReq(hl='en-US', tz=360)

timeframes = {'7_days': 'now 7-d', '30_days': 'today 1-m', '90_days': 'today 3-m'}

def fetch_trends(keyword_or_bigram, timeframe):
    pytrends.build_payload([keyword_or_bigram], cat=0, timeframe=timeframe, geo='', gprop='')
    interest_over_time = pytrends.interest_over_time()
    return interest_over_time.mean()[0]

# Fetch the search trends for the keywords and bigrams
print("Fetching search trends...\n")
trends = []
for keyword_or_bigram, _ in keywords_and_bigrams:
    try:
        trend_data = {f"{period}_popularity": fetch_trends(keyword_or_bigram, timeframe) for period, timeframe in timeframes.items()}
        trend_data["Keyword"] = keyword_or_bigram
        trends.append(trend_data)
    except Exception as e:
        print(f"Error fetching trends for {keyword_or_bigram}: {e}")

# Create a DataFrame with the trends data
trends_df = pd.DataFrame(trends)

# Merge the keywords DataFrame with the trends DataFrame
keywords_trends_df = keywords_df.merge(trends_df, on="Keyword")

# Add Timestamp column
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
keywords_trends_df = keywords_trends_df.drop(columns=['Timestamp'], errors='ignore')
keywords_trends_df['Timestamp'] = now

# Rename Google Trends columns
column_rename = {f"{period}_popularity": f"gt_{period.split('_')[0]}_day" for period in timeframes.keys()}
keywords_trends_df.rename(columns=column_rename, inplace=True)

# Format Google Trends results to 2 decimal places
for column in column_rename.values():
    keywords_trends_df[column] = keywords_trends_df[column].map('{:,.2f}'.format)

# Print the trends
print("\nSearch Trends:")
print(tabulate(keywords_trends_df, headers='keys', tablefmt='fancy_grid', showindex=False))
print("\n")
print("Search Trends saved to outputs/keywords_trends.csv\n")
sleep(buffer * 2)

# Save the merged DataFrame to a CSV file
keywords_trends_df.to_csv("outputs/keywords_trends.csv", index=False)