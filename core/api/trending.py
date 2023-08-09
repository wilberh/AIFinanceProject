import pandas as pd
import numpy as np

from pytrends.request import TrendReq
from google.cloud import bigquery

import yfinance as yf

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from newsapi import NewsApiClient

from datetime import date
import sys, traceback
import requests
import os


NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')


def get_stock_price(stock, strt_dt, end_dt):
    """
    :Parameters:
        stock : str, list
            List of tickers to download
        strt_dt: str
            Download start date string (YYYY-MM-DD) or _datetime, inclusive.
            Default is 29 days ago
            E.g. for end_dt="2023-08-01", the strt_dt="2023-07-02"
        end_dt: str
            Download end date string (YYYY-MM-DD) or _datetime, exclusive.
            Default is now
    'closing price' or 'adjusted closing price' is used because - gives you the most info you need to focus for a day 
    DONNOT use the following:
    *opening price is not reliable (subject to manipulation because of timelag between Asian and US markets; so there will be a huge difference)
    *low and high price doesn't give you the big picture
    # stock = ['^GSPC','AAPL','MSFT','INTC']
    """
    try:
        SP = yf.download(stock,start=strt_dt,end=end_dt,interval='1d')
        
        if not isinstance(SP, pd.DataFrame):
            return {"error": "Bad response from API"}
        
        SP.index = SP.index.strftime('%Y%m%d')
        SP_close = SP.Close

        return SP_close.to_dict()
    except Exception as ex:
        formatted_lines = traceback.format_exc().splitlines()
        return {"error": formatted_lines[0]+' \n'+formatted_lines[-1]}


def trending_by_country(company, country, strt_dt, end_dt):
    """
    :Parameters:
        company : str
            The company name.
            E.g. "apple" or "microsoft" 
        country: str
            The country code to search for news articles data
            E.g. "us" or "uk"
        strt_dt: str
            Download start date string (YYYY-MM-DD) or _datetime, inclusive.
            Default is 29 days ago
            E.g. for end_dt="2023-08-01", the strt_dt="2023-07-02"
        end_dt: str
            Download end date string (YYYY-MM-DD) or _datetime, exclusive.
            Default is now
    https://github.com/cjhutto/vaderSentiment
    VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and 
    rule-based sentiment analysis tool that is specifically attuned to sentiments 
    expressed in social media. It is fully open-sourced.

    NLTK provides us with a VADER implementation for easy use -
    Sentiment analyzer expects a full sentence as input and returns scores along thes dimensions:
    'compound' value gives you the average score for the text
    ranges from -1 to 1
    {'neg': 0.0, 'neu': 0.0, 'pos': 1.0, 'compound': 0.4404}
    """
    newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

    language = 'en'

    try:
        sources = newsapi.get_sources()
        sources_records = sources['sources']
        sources_df = pd.DataFrame.from_records(sources_records)
        sources_country = sources_df[(sources_df['language'] == language) 
                                    & (sources_df['category'] == 'business')
                                    & (sources_df['country'] == country)]
        max_sources_api = ','.join(list(sources_country['id'].iloc[:20]))  # 20 max sources allowed by api

        page = 1
        params = {'q': company, 
                   'sources': max_sources_api,
                   'from': strt_dt,
                   'to': end_dt,
                   'language': language,
                   'searchIn': 'title',
                   'sortBy': 'relevancy',
                   'page': page                  
                   }
        headers = {'Authorization': f'Bearer {NEWSAPI_KEY}'}
        total_results = 1
        total_per_pages = 0
        all_articles = []

        while total_results > total_per_pages:
            params['page']: page
            resp = requests.get('https://newsapi.org/v2/everything', params=params, headers=headers)
            resp_all_articles = resp.json()
            all_articles.extend(resp_all_articles['articles'])
            total_results = resp_all_articles['totalResults']
            total_per_pages += len(resp_all_articles['articles'])
            page += 1

        news_articles = pd.DataFrame.from_dict(all_articles)

        columns = ['date', 'source', 'title', 'compound']
        titles_sentiment = pd.DataFrame([], columns=columns)
        sentiment = SentimentIntensityAnalyzer()

        for date, source, title in zip(news_articles['publishedAt'], news_articles['source'], news_articles['title']):
            score = sentiment.polarity_scores(title)
            new_row = pd.Series({'date': date[:10].replace('-', ''),
                                 'source': source['name'],
                                 'title': title,
                                 'compound': score['compound']})
            titles_sentiment = pd.concat([titles_sentiment, new_row.to_frame().T], ignore_index=True)

        titles_sentiment.drop_duplicates(subset=['date', 'source', 'title'])
        return titles_sentiment.to_dict('records')
    except Exception as ex:
        formatted_lines = traceback.format_exc().splitlines()
        return {"error": formatted_lines[0]+' \n'+formatted_lines[-1]}

