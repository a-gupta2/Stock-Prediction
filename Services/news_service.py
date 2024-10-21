import pandas as pd
import requests


def get_latest_stock_news(url, api_key, query='stock'):
    """Fetch news articles related to the stock using a direct HTTP request."""

    url = f"{url}?q={query}&language=en&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        if 'articles' in data:
            articles = pd.DataFrame(data['articles'])
            return articles
    else:
        print(f"Error fetching news: {response.status_code}")

    return pd.DataFrame()