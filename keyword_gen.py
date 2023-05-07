# import necessary python libraries
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter

# download NLTK data
nltk.download("stopwords")
nltk.download("punkt")

# Define a function to scrape web pages:
def get_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return text

# Define a function to extract keywords:
def extract_keywords(text, top_n=10):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    
    # Filter out punctuation and convert to lower case
    words = [word.lower() for word in words if word.isalnum()]
    
    # Remove stopwords
    words = [word for word in words if word not in stop_words]
    
    # Get the most common words
    freq = Counter(words)
    keywords = freq.most_common(top_n)
    
    return keywords

#Use the functions to get keywords associated with a company:
# Replace 'company_name' with the actual company name
company_name = "Radical Skincare"

# Get company related information from a reputable source
# Replace 'url' with the URL of the desired webpage
url = "https://radicalskincare.com/".format(company_name)

text = get_text_from_url(url)
keywords = extract_keywords(text)

print("Keywords associated with {}:".format(company_name))
for keyword, frequency in keywords:
    print("{}: {}".format(keyword, frequency))
