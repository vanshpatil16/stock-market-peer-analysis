"""
Test script to check if news APIs are working.
This script tests Finnhub, NewsAPI, and yfinance news endpoints.
"""

import requests
import yfinance as yf
from datetime import datetime, timedelta
import sys
import os

# Try to import streamlit secrets (if available)
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    print("[!] Streamlit not available - will test APIs without keys\n")

def get_api_keys():
    """Get API keys from streamlit secrets or environment variables."""
    finnhub_key = None
    newsapi_key = None
    
    if HAS_STREAMLIT:
        try:
            finnhub_key = st.secrets.get("FINNHUB_API_KEY", None)
            newsapi_key = st.secrets.get("NEWSAPI_KEY", None)
        except Exception:
            pass
    
    # Fallback to environment variables
    if not finnhub_key:
        finnhub_key = os.getenv("FINNHUB_API_KEY", None)
    if not newsapi_key:
        newsapi_key = os.getenv("NEWSAPI_KEY", None)
    
    return finnhub_key, newsapi_key

def test_finnhub_api(api_key=None):
    """Test Finnhub API."""
    print("=" * 60)
    print("Testing Finnhub API")
    print("=" * 60)
    
    if not api_key:
        print("[X] No API key found (FINNHUB_API_KEY)")
        print("   Status: NOT CONFIGURED")
        print("   Note: Finnhub requires an API key for most endpoints")
        return False
    
    print(f"[OK] API key found: {api_key[:8]}...{api_key[-4:]}")
    
    try:
        # Test with a common stock symbol (RELIANCE)
        symbol = "RELIANCE"
        url = "https://finnhub.io/api/v1/company-news"
        params = {
            'symbol': symbol,
            'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'to': datetime.now().strftime('%Y-%m-%d'),
            'token': api_key
        }
        
        print(f"   Testing endpoint: {url}")
        print(f"   Symbol: {symbol}")
        
        response = requests.get(url, params=params, timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                article_count = len(data)
                print(f"[OK] API is WORKING")
                print(f"   Found {article_count} articles")
                if article_count > 0:
                    print(f"   Sample article: {data[0].get('headline', 'N/A')[:60]}...")
                return True
            else:
                print(f"[!] Unexpected response format: {type(data)}")
                print(f"   Response: {str(data)[:200]}")
                return False
        elif response.status_code == 401:
            print("[X] API is NOT WORKING - Invalid API key")
            return False
        elif response.status_code == 429:
            print("[!] API is RATE LIMITED - Too many requests")
            return False
        else:
            print(f"[X] API returned error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("[X] API is NOT WORKING - Request timeout")
        return False
    except requests.exceptions.ConnectionError:
        print("[X] API is NOT WORKING - Connection error")
        return False
    except Exception as e:
        print(f"[X] API is NOT WORKING - Error: {str(e)}")
        return False

def test_tavily(api_key=None):
    """Test Tavily API."""
    print("\n" + "=" * 60)
    print("Testing Tavily API")
    print("=" * 60)
    
    if not api_key:
        print("[X] No API key found (NEWSAPI_KEY)")
        print("   Status: NOT CONFIGURED")
        print("   Note: Tavily requires an API key")
        return False
    
    print(f"[OK] API key found: {api_key[:8]}...{api_key[-4:]}")
    
    try:
        # Test with Tavily API endpoint
        url = "https://api.tavily.com/search"
        payload = {
            'api_key': api_key,
            'query': 'RELIANCE stock news',
            'topic': 'news',
            'max_results': 5,
            'search_depth': 'basic'
        }
        
        print(f"   Testing endpoint: {url}")
        print(f"   Query: RELIANCE stock news")
        
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                article_count = len(data.get('results', []))
                print(f"[OK] API is WORKING")
                print(f"   Found {article_count} articles")
                if article_count > 0:
                    print(f"   Sample article: {data['results'][0].get('title', 'N/A')[:60]}...")
                return True
            else:
                print(f"[!] API returned no results")
                print(f"   Response: {str(data)[:200]}")
                return False
        elif response.status_code == 401:
            print("[X] API is NOT WORKING - Invalid API key")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('error', response.text[:200])}")
            except:
                print(f"   Response: {response.text[:200]}")
            return False
        elif response.status_code == 429:
            print("[!] API is RATE LIMITED - Too many requests")
            return False
        else:
            print(f"[X] API returned error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('error', response.text[:200])}")
            except:
                print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("[X] API is NOT WORKING - Request timeout")
        return False
    except requests.exceptions.ConnectionError:
        print("[X] API is NOT WORKING - Connection error")
        return False
    except Exception as e:
        print(f"[X] API is NOT WORKING - Error: {str(e)}")
        return False

def test_yfinance_news():
    """Test yfinance news (fallback, no API key needed)."""
    print("\n" + "=" * 60)
    print("Testing yfinance News (Fallback)")
    print("=" * 60)
    
    try:
        print("   Testing with ticker: RELIANCE.NS")
        ticker = yf.Ticker("RELIANCE.NS")
        
        try:
            news = ticker.news
        except Exception as e:
            print(f"[X] yfinance is NOT WORKING - Error fetching news: {str(e)}")
            return False
        
        if news is None:
            print("[!] yfinance returned None (no news available)")
            return False
        
        if isinstance(news, list):
            article_count = len(news)
            print(f"[OK] yfinance is WORKING")
            print(f"   Found {article_count} articles")
            if article_count > 0:
                print(f"   Sample article: {news[0].get('title', 'N/A')[:60]}...")
            return True
        else:
            print(f"[!] Unexpected response format: {type(news)}")
            return False
            
    except Exception as e:
        print(f"[X] yfinance is NOT WORKING - Error: {str(e)}")
        return False

def main():
    """Run all API tests."""
    print("\n" + "NEWS API DIAGNOSTIC TEST" + "\n")
    print("This script tests all news APIs used in the application.\n")
    
    # Get API keys
    finnhub_key, newsapi_key = get_api_keys()
    
    # Test each API
    results = {
        'Finnhub': test_finnhub_api(finnhub_key),
        'Tavily': test_tavily(newsapi_key),
        'yfinance': test_yfinance_news()
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for api_name, status in results.items():
        if status:
            print(f"[OK] {api_name}: WORKING")
        else:
            print(f"[X] {api_name}: NOT WORKING or NOT CONFIGURED")
    
    working_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n{working_count}/{total_count} APIs are working")
    
    if working_count == 0:
        print("\n[!] WARNING: No news APIs are working!")
        print("   The app will still work for stock analysis, but news features won't be available.")
    elif working_count < total_count:
        print("\n[!] Some APIs are not working, but the app can still fetch news from working sources.")
    else:
        print("\n[OK] All APIs are working! News features should work properly.")
    
    print("\n" + "=" * 60)
    print("Configuration Help")
    print("=" * 60)
    print("\nTo configure API keys:")
    print("1. Create .streamlit/secrets.toml file (for local development)")
    print("2. Add your keys:")
    print("   FINNHUB_API_KEY = \"your-key-here\"")
    print("   NEWSAPI_KEY = \"your-tavily-key-here\"")
    print("\nOr set environment variables:")
    print("   export FINNHUB_API_KEY=\"your-key-here\"")
    print("   export NEWSAPI_KEY=\"your-tavily-key-here\"")
    print("\nGet API keys:")
    print("  - Finnhub: https://finnhub.io (free tier available)")
    print("  - Tavily: https://tavily.com (free tier available)")
    print("\nNote: yfinance doesn't require an API key and works as a fallback.")
    print("Note: NEWSAPI_KEY is used for Tavily API (kept for backward compatibility).")

if __name__ == "__main__":
    main()

