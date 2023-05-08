import requests

def is_shopify_store(url):
    try:
        response = requests.head(url)
        return 'X-ShopId' in response.headers
    except requests.exceptions.RequestException as e:
        print(f"Error while checking if the website is a Shopify store: {e}")
        return False
