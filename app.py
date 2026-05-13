"""
News Web App - Backend (Flask)
------------------------------
This file is the server. It:
  1. Loads your secret API key from the .env file (so it never appears in the browser)
  2. Provides API endpoints that the frontend (index.html) calls to get news
  3. Fetches articles from NewsAPI and returns them as JSON

Run with:  python3 app.py
Then open: http://127.0.0.1:5000
"""

from flask import Flask, render_template, jsonify
import requests
import os
from dotenv import load_dotenv

# Load the .env file so we can read NEWS_API_KEY
load_dotenv()

app = Flask(__name__)

# Read the API key from the .env file
API_KEY = os.getenv('NEWS_API_KEY')
BASE_URL = 'https://newsapi.org/v2'


def fetch_articles(endpoint, params):
    """
    Helper function that calls the NewsAPI.
    - endpoint: either 'top-headlines' or 'everything'
    - params: a dictionary of filters (category, query, language, etc.)
    Returns a list of article dictionaries.
    """
    # Always attach the API key to every request
    params['apiKey'] = API_KEY
    params['pageSize'] = 12  # max articles per section

    try:
        response = requests.get(f'{BASE_URL}/{endpoint}', params=params, timeout=10)
        data = response.json()
        # 'articles' is the list of news articles from the API
        return data.get('articles', [])
    except Exception as e:
        print(f'Error fetching news: {e}')
        return []


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template('index.html')


@app.route('/api/headlines')
def headlines():
    """
    Top US headlines of the day.
    Uses 'top-headlines' with country=us.
    """
    articles = fetch_articles('top-headlines', {'country': 'us'})
    return jsonify(articles)


@app.route('/api/sports')
def sports():
    """
    Sports news.
    Uses 'top-headlines' with category=sports.
    """
    articles = fetch_articles('top-headlines', {'category': 'sports', 'language': 'en'})
    return jsonify(articles)


@app.route('/api/world')
def world():
    """
    World news — general international stories.
    Uses 'top-headlines' with category=general, not filtered by country
    so we get international coverage.
    """
    articles = fetch_articles('top-headlines', {'category': 'general', 'language': 'en'})
    return jsonify(articles)


@app.route('/api/iran')
def iran():
    """
    US–Iran war updates.
    Uses 'everything' endpoint with a keyword search so we get the
    most recent articles matching these terms, sorted newest first.
    """
    articles = fetch_articles('everything', {
        'q': 'US Iran war OR Iran nuclear OR Iran missile',
        'sortBy': 'publishedAt',
        'language': 'en'
    })
    return jsonify(articles)


# ── Entry point ─────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    if not API_KEY:
        print('ERROR: NEWS_API_KEY not found. Check your .env file.')
    else:
        print('Starting News App → http://127.0.0.1:5000')
        app.run(debug=True)
