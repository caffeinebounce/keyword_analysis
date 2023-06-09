# config.py
from urllib.parse import urlparse

base_url = "https://mysunday2sunday.com/"

# Extract the domain from the base_url
parsed_url = urlparse(base_url)
base_domain = parsed_url.netloc

# Minimum frequency for the bigrams and keyword scrape
min_count = 10

# Top N keywords and bigrams to extract
top = 20