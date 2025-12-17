import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
import time

st.set_page_config(
    page_title="Indian Stock Peer Analysis Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

"""
# :material/query_stats: Market Analysis Dashboard

Compare stocks, commodities, and bonds to track market trends and performance.
"""

# Display marquee with all stocks news at the top (after functions are defined below)
# This will be rendered after helper functions are loaded

""  # Add some space.

cols = st.columns([1, 3])
# Will declare right cell later to avoid showing it when no data.

STOCKS = [
    # Large Cap Stocks - Original Working List
    "RELIANCE.NS",
    "TCS.NS",
    "HDFCBANK.NS",
    "INFY.NS",
    "ICICIBANK.NS",
    "HINDUNILVR.NS",
    "ITC.NS",
    "SBIN.NS",
    "BHARTIARTL.NS",
    "KOTAKBANK.NS",
    "LT.NS",
    "HCLTECH.NS",
    "AXISBANK.NS",
    "ASIANPAINT.NS",
    "MARUTI.NS",
    "WIPRO.NS",
    "NESTLEIND.NS",
    "SUNPHARMA.NS",
    "BAJFINANCE.NS",
    "TITAN.NS",
    "ULTRACEMCO.NS",
    "ONGC.NS",
    "NTPC.NS",
    "POWERGRID.NS",
    "COALINDIA.NS",
    "ADANIPORTS.NS",
    "ADANIENT.NS",
    "JSWSTEEL.NS",
    "TATAMOTORS.NS",
    "TATASTEEL.NS",
    "M&M.NS",
    "TECHM.NS",
    "DIVISLAB.NS",
    "BAJAJFINSV.NS",
    "GRASIM.NS",
    "HDFCLIFE.NS",
    "BRITANNIA.NS",
    "INDUSINDBK.NS",
    "DRREDDY.NS",
    "CIPLA.NS",
    "EICHERMOT.NS",
    "HEROMOTOCO.NS",
    "DABUR.NS",
    "GODREJCP.NS",
    "MARICO.NS",
    "PIDILITIND.NS",
    "HAVELLS.NS",
    "VOLTAS.NS",
    "WHIRLPOOL.NS",
    "AMBUJACEM.NS",
    "SHREECEM.NS",
    "ACC.NS",
    "RAMCOCEM.NS",
    "VEDL.NS",
    "HINDALCO.NS",
    "NMDC.NS",
    "IOC.NS",
    "BPCL.NS",
    "GAIL.NS",
    "PETRONET.NS",
    "GSPL.NS",
    "IGL.NS",
    "MGL.NS",
    # Additional Large Cap Stocks
    "APOLLOHOSP.NS",
    "BAJAJ-AUTO.NS",
    "BANKBARODA.NS",
    "BHARATFORG.NS",
    "CANBK.NS",
    "CHOLAFIN.NS",
    "COLPAL.NS",
    "DALBHARAT.NS",
    "DLF.NS",
    "GODREJPROP.NS",
    "HDFCAMC.NS",
    "ICICIPRULI.NS",
    "ICICIGI.NS",
    "INDIGO.NS",
    "IRCTC.NS",
    "JINDALSTEL.NS",
    "LICI.NS",
    "LUPIN.NS",
    "NAUKRI.NS",
    "PAGEIND.NS",
    "PFC.NS",
    "PIIND.NS",
    "POLICYBZR.NS",
    "RECLTD.NS",
    "SAIL.NS",
    "SBILIFE.NS",
    "SIEMENS.NS",
    "TATACONSUM.NS",
    "TATAPOWER.NS",
    "TORNTPHARM.NS",
    "TVSMOTOR.NS",
    "UNIONBANK.NS",
    # Mid Cap Stocks
    "ABB.NS",
    "ADANIGREEN.NS",
    "ALKEM.NS",
    "APLLTD.NS",
    "AUBANK.NS",
    "BALKRISIND.NS",
    "BANDHANBNK.NS",
    "BERGEPAINT.NS",
    "BIOCON.NS",
    "BOSCHLTD.NS",
    "CAMS.NS",
    "CONCOR.NS",
    "CUMMINSIND.NS",
    "DIXON.NS",
    "ESCORTS.NS",
    "FEDERALBNK.NS",
    "GLENMARK.NS",
    "GODREJIND.NS",
    "GUJGASLTD.NS",
    "HAL.NS",
    "HINDCOPPER.NS",
    "IDFCFIRSTB.NS",
    "IEX.NS",
    "INDIAMART.NS",
    "INDIANB.NS",
    "JKCEMENT.NS",
    "JUBLFOOD.NS",
    "JUSTDIAL.NS",
    "KEI.NS",
    "LAURUSLABS.NS",
    "MANKIND.NS",
    "MAXHEALTH.NS",
    "MOTHERSON.NS",
    "MPHASIS.NS",
    "NYKAA.NS",
    "OBEROIRLTY.NS",
    "OFSS.NS",
    "PERSISTENT.NS",
    "POWERINDIA.NS",
    "RAJESHEXPO.NS",
    "RATNAMANI.NS",
    "RVNL.NS",
    "SCHAEFFLER.NS",
    "STARHEALTH.NS",
    "SUNDARMFIN.NS",
    "SUPREMEIND.NS",
    "TATACHEM.NS",
    "TATAELXSI.NS",
    "TATACOMM.NS",
    "TRENT.NS",
    "UNOMINDA.NS",
    "VBL.NS",
    "YESBANK.NS",
    "ZYDUSLIFE.NS",
    # Well-Known Small Cap Stocks
    "AARTIIND.NS",
    "AAVAS.NS",
    "ADANIPOWER.NS",
    "AFFLE.NS",
    "ANGELONE.NS",
    "ASHOKLEY.NS",
    "ASTERDM.NS",
    "ASTRAL.NS",
    "ATUL.NS",
    "BATAINDIA.NS",
    "BEL.NS",
    "BLUEDART.NS",
    "CERA.NS",
    "COFORGE.NS",
    "COROMANDEL.NS",
    "CRISIL.NS",
    "CYIENT.NS",
    "DEEPAKNTR.NS",
    "DELHIVERY.NS",
    "DEVYANI.NS",
    "EASEMYTRIP.NS",
    "EIHOTEL.NS",
    "ENDURANCE.NS",
    "EQUITAS.NS",
    "ERIS.NS",
    "FORTIS.NS",
    "GRANULES.NS",
    "HATSUN.NS",
    "HINDZINC.NS",
    "ICRA.NS",
    "IDEA.NS",
    "IIFL.NS",
    "INTELLECT.NS",
    "IOB.NS",
    "JSWENERGY.NS",
    "KPITTECH.NS",
    "KRBL.NS",
    "LATENTVIEW.NS",
    "LEMONTREE.NS",
    "LTIM.NS",
    "LTTS.NS",
    "MCX.NS",
    "MEDANTA.NS",
    "METROBRAND.NS",
    "METROPOLIS.NS",
    "MRF.NS",
    "MRPL.NS",
    "NATCOPHARM.NS",
    "NAZARA.NS",
    "NBCC.NS",
    "NCC.NS",
    "PNB.NS",
    "POLYCAB.NS",
    "PRESTIGE.NS",
    "RADICO.NS",
    "RAILTEL.NS",
    "RBLBANK.NS",
    "REDINGTON.NS",
    "RELAXO.NS",
    "RITES.NS",
    "ROUTE.NS",
    "SBICARD.NS",
    "SCHNEIDER.NS",
    "SRF.NS",
    "SYMPHONY.NS",
    "SYNGENE.NS",
    "THERMAX.NS",
    "THYROCARE.NS",
    "TIMKEN.NS",
    "UPL.NS",
    "VGUARD.NS",
    "VMART.NS",
    # BSE Stocks
    "RELIANCE.BO",
    "TCS.BO",
    "HDFCBANK.BO",
    "INFY.BO",
    "ICICIBANK.BO",
]

DEFAULT_STOCKS = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "HINDUNILVR.NS", "ITC.NS"]

# Commodities list (using Yahoo Finance symbols)
COMMODITIES = [
    # Precious Metals
    "GC=F",      # Gold Futures
    "SI=F",      # Silver Futures
    "PL=F",      # Platinum Futures
    "PA=F",      # Palladium Futures
    # Energy
    "CL=F",      # Crude Oil (WTI)
    "BZ=F",      # Brent Crude
    "NG=F",      # Natural Gas
    "RB=F",      # RBOB Gasoline
    "HO=F",      # Heating Oil
    # Agricultural
    "ZC=F",      # Corn
    "ZS=F",      # Soybeans
    "ZW=F",      # Wheat
    "KC=F",      # Coffee
    "CC=F",      # Cocoa
    "CT=F",      # Cotton
    "SB=F",      # Sugar
    # Metals
    "HG=F",      # Copper
    "ZI=F",      # Zinc
]

# Commodity name mapping for user-friendly display
COMMODITY_NAMES = {
    "GC=F": "Gold",
    "SI=F": "Silver",
    "PL=F": "Platinum",
    "PA=F": "Palladium",
    "CL=F": "Crude Oil (WTI)",
    "BZ=F": "Brent Crude",
    "NG=F": "Natural Gas",
    "RB=F": "Gasoline",
    "HO=F": "Heating Oil",
    "ZC=F": "Corn",
    "ZS=F": "Soybeans",
    "ZW=F": "Wheat",
    "KC=F": "Coffee",
    "CC=F": "Cocoa",
    "CT=F": "Cotton",
    "SB=F": "Sugar",
    "HG=F": "Copper",
    "ZI=F": "Zinc",
}

DEFAULT_COMMODITIES = ["GC=F", "CL=F", "SI=F", "NG=F", "ZC=F"]

# Bonds list (using Yahoo Finance symbols)
BONDS = [
    # US Treasury Bonds
    "^TNX",      # 10-Year Treasury Yield
    "^IRX",      # 13 Week Treasury Bill
    "^FVX",      # 5-Year Treasury Yield
    "^TYX",      # 30-Year Treasury Yield
    # Indian ETFs (as bond alternatives/proxies)
    "GOLDBEES.NS",  # Gold ETF
    "SILVER.NS",    # Silver ETF
    "LIQUIDBEES.NS", # Liquid ETF
]

# Bond name mapping for user-friendly display
BOND_NAMES = {
    "^TNX": "10-Year Treasury Yield",
    "^IRX": "13 Week Treasury Bill",
    "^FVX": "5-Year Treasury Yield",
    "^TYX": "30-Year Treasury Yield",
    "GOLDBEES.NS": "Gold ETF",
    "SILVER.NS": "Silver ETF",
    "LIQUIDBEES.NS": "Liquid ETF",
}

DEFAULT_BONDS = ["^TNX", "^IRX", "^FVX", "^TYX"]

# Mutual Funds list (Indian ETFs - only verified working tickers)
# Note: Many ETFs are not available on Yahoo Finance
# Only including tickers that are confirmed to work
MUTUAL_FUNDS = [
    # Large Cap / Broad Market ETFs
    "NIFTYBEES.NS",       # Nifty 50 ETF (Nifty BeES)
    "JUNIORBEES.NS",      # Nifty Next 50 ETF
    
    # Mid Cap ETFs
    "MIDCAPBEES.NS",      # Mid-cap ETF
    
    # Sectoral ETFs
    "BANKBEES.NS",        # Banking ETF
    "ITBEES.NS",          # IT ETF
    "PHARMABEES.NS",      # Pharma ETF
    
    # Gold ETF
    "GOLDBEES.NS",        # Gold ETF
    
    # Debt/Liquid ETFs
    "LIQUIDBEES.NS",      # Liquid ETF
]

# Mutual Fund name mapping for user-friendly display
MUTUAL_FUND_NAMES = {
    "NIFTYBEES.NS": "Nifty 50 ETF (Nifty BeES)",
    "JUNIORBEES.NS": "Nifty Next 50 ETF",
    "MIDCAPBEES.NS": "Mid-cap ETF",
    "BANKBEES.NS": "Banking ETF",
    "ITBEES.NS": "IT ETF",
    "PHARMABEES.NS": "Pharma ETF",
    "GOLDBEES.NS": "Gold ETF",
    "LIQUIDBEES.NS": "Liquid ETF",
}

# Mutual Fund categories
MUTUAL_FUND_CATEGORIES = {
    "Large Cap / Broad Market": ["NIFTYBEES.NS", "JUNIORBEES.NS"],
    "Mid Cap": ["MIDCAPBEES.NS"],
    "Sectoral ETFs": ["BANKBEES.NS", "ITBEES.NS", "PHARMABEES.NS"],
    "Commodity ETFs": ["GOLDBEES.NS"],
    "Debt / Liquid": ["LIQUIDBEES.NS"],
}

DEFAULT_MUTUAL_FUNDS = ["NIFTYBEES.NS", "BANKBEES.NS", "ITBEES.NS"]


# Helper functions for news processing
def is_valid_article(article: Dict) -> bool:
    """Check if an article has valid data."""
    title = article.get('title', '').strip()
    # Filter out articles with no title or placeholder titles
    if not title or title.lower() in ['no title', 'untitled', '']:
        return False
    
    # Check for valid timestamp - be more lenient (allow 0 as fallback, but prefer valid timestamps)
    timestamp = article.get('providerPublishTime', 0)
    # Only reject if timestamp is clearly invalid (before 2000 and not 0)
    if timestamp != 0 and timestamp < 946684800:  # Before year 2000
        return False
    
    return True


def is_growth_related(title: str, summary: str = "") -> bool:
    """Check if news is related to growth or positive performance."""
    growth_keywords = [
        "growth", "surge", "rise", "gain", "profit", "revenue", "earnings beat",
        "outperform", "upgrade", "bullish", "rally", "soar", "jump", "climb",
        "increase", "expansion", "acquisition", "partnership", "deal", "positive",
        "strong", "record", "high", "beat", "exceed", "outperform"
    ]
    text = (title + " " + summary).lower()
    return any(keyword in text for keyword in growth_keywords)


def is_depreciation_related(title: str, summary: str = "") -> bool:
    """Check if news is related to depreciation or negative performance."""
    depreciation_keywords = [
        "fall", "drop", "decline", "loss", "downgrade", "bearish", "plunge",
        "crash", "slump", "decrease", "miss", "disappoint", "negative", "weak",
        "concern", "worry", "risk", "uncertainty", "challenge", "struggle",
        "underperform", "sell-off", "correction", "volatility"
    ]
    text = (title + " " + summary).lower()
    return any(keyword in text for keyword in depreciation_keywords)


def format_news_date(timestamp: int) -> str:
    """Convert timestamp to readable relative time format (like '2h ago', '1d ago')."""
    try:
        if timestamp == 0 or timestamp < 946684800:  # Invalid timestamp
            return "Unknown date"
        
        dt = datetime.fromtimestamp(timestamp)
        now = datetime.now()
        
        # Check if date is reasonable
        if dt.year < 2000 or dt.year > datetime.now().year + 1:
            return "Unknown date"
        
        # Calculate relative time
        time_diff = now - dt.replace(tzinfo=None) if dt.tzinfo else now - dt
        
        if time_diff.total_seconds() < 60:
            return "Just now"
        elif time_diff.total_seconds() < 3600:
            minutes = int(time_diff.total_seconds() / 60)
            return f"{minutes}m ago"
        elif time_diff.total_seconds() < 86400:
            hours = int(time_diff.total_seconds() / 3600)
            return f"{hours}h ago"
        elif time_diff.days < 7:
            days = time_diff.days
            return f"{days}d ago"
        else:
            return dt.strftime("%Y-%m-%d")
    except:
        return "Unknown date"


# Load news for all stocks in marquee (runs in background)
@st.cache_resource(show_spinner=False, ttl="30m")
def load_all_stocks_news() -> List[Dict]:
    """Load news for all stocks in STOCKS list using multi-source approach."""
    all_news = []
    
    # Get API keys from streamlit secrets
    try:
        finnhub_key = st.secrets.get("FINNHUB_API_KEY", None)
        newsapi_key = st.secrets.get("NEWSAPI_KEY", None)
    except Exception:
        finnhub_key = None
        newsapi_key = None
    
    # Process stocks in batches to avoid rate limits
    batch_size = 10
    for i in range(0, len(STOCKS), batch_size):
        batch = STOCKS[i:i+batch_size]
        for ticker in batch:
            try:
                # Try Finnhub first
                finnhub_news = fetch_news_finnhub(ticker, finnhub_key)
                all_news.extend(finnhub_news)
                
                # Try Tavily if key available
                if newsapi_key:
                    tavily_news = fetch_news_tavily(ticker, newsapi_key)
                    all_news.extend(tavily_news)
                
                # Fallback to yfinance
                ticker_obj = yf.Ticker(ticker)
                yf_news = ticker_obj.news
                if yf_news:
                    for article in yf_news:
                        if is_valid_article(article):
                            article['ticker'] = ticker
                            all_news.append(article)
            except Exception:
                continue
        
        # Small delay between batches to respect rate limits
        if i + batch_size < len(STOCKS):
            time.sleep(0.5)
    
    # Remove duplicates
    seen_titles = set()
    unique_news = []
    for article in all_news:
        title_lower = article.get('title', '').lower().strip()
        if title_lower and title_lower not in seen_titles:
            unique_news.append(article)
            seen_titles.add(title_lower)
    
    # Sort by date (newest first)
    unique_news.sort(key=lambda x: x.get('providerPublishTime', 0), reverse=True)
    return unique_news[:100]  # Limit to 100 most recent articles


# Load marquee news (will be displayed after asset_type is defined)
try:
    _marquee_news = load_all_stocks_news()
except Exception:
    _marquee_news = []


def stocks_to_str(stocks):
    return ",".join(stocks)


def get_display_name(ticker: str, asset_type: str) -> str:
    """Get user-friendly display name for a ticker."""
    if asset_type == "Commodities":
        return COMMODITY_NAMES.get(ticker, ticker)
    elif asset_type == "Bonds":
        return BOND_NAMES.get(ticker, ticker)
    elif asset_type == "Mutual Funds":
        return MUTUAL_FUND_NAMES.get(ticker, ticker)
    else:
        return ticker


# Asset type selector (Tabs)
asset_type = st.radio(
    "Select Asset Type",
    ["Stocks", "Commodities", "Bonds", "Mutual Funds"],
    horizontal=True,
    key="asset_type"
)

# Select appropriate list and defaults based on asset type
if asset_type == "Commodities":
    ASSET_LIST = COMMODITIES
    DEFAULT_ASSETS = DEFAULT_COMMODITIES
    asset_label = "Commodity"
elif asset_type == "Bonds":
    ASSET_LIST = BONDS
    DEFAULT_ASSETS = DEFAULT_BONDS
    asset_label = "Bond"
elif asset_type == "Mutual Funds":
    ASSET_LIST = MUTUAL_FUNDS
    DEFAULT_ASSETS = DEFAULT_MUTUAL_FUNDS
    asset_label = "Mutual Fund"
else:  # Stocks
    ASSET_LIST = STOCKS
    DEFAULT_ASSETS = DEFAULT_STOCKS
    asset_label = "Stock"

# Update session state key based on asset type
session_key = f"{asset_type.lower()}_tickers_input"

if session_key not in st.session_state:
    st.session_state[session_key] = st.query_params.get(
        f"{asset_type.lower()}_stocks", stocks_to_str(DEFAULT_ASSETS)
    ).split(",")


# Callback to update query param when input changes
def update_query_param():
    asset_type_val = st.session_state.get("asset_type", "Stocks")
    session_key_val = f"{asset_type_val.lower()}_tickers_input"
    
    if st.session_state.get(session_key_val):
        st.query_params[f"{asset_type_val.lower()}_stocks"] = stocks_to_str(st.session_state[session_key_val])
    else:
        st.query_params.pop(f"{asset_type_val.lower()}_stocks", None)


top_left_cell = cols[0].container(
    border=True, height="stretch", vertical_alignment="center"
)

with top_left_cell:
    # Create formatted options for commodities and bonds with friendly names
    if asset_type == "Commodities":
        # Format options as "GC=F - Gold"
        formatted_options = {}
        options_list = sorted(set(ASSET_LIST) | set(st.session_state[session_key]))
        for symbol in options_list:
            friendly_name = COMMODITY_NAMES.get(symbol, symbol)
            formatted_options[f"{symbol} - {friendly_name}"] = symbol
        
        # Display info about commodity symbols
        with st.expander("ℹ️ What do these symbols mean?", expanded=False):
            st.markdown("""
            **Commodity Symbols Explained:**
            - **GC=F** = Gold Futures
            - **CL=F** = Crude Oil (WTI)
            - **SI=F** = Silver Futures
            - **NG=F** = Natural Gas
            - **ZC=F** = Corn
            - **KC=F** = Coffee
            - **BZ=F** = Brent Crude
            - **HG=F** = Copper
            - **ZS=F** = Soybeans
            - **ZW=F** = Wheat
            
            *All symbols ending with "=F" are futures contracts traded on commodity exchanges.*
            """)
        
        # Multiselect with formatted options
        selected_display = [f"{t} - {COMMODITY_NAMES.get(t, t)}" for t in st.session_state[session_key] if t in ASSET_LIST]
        selected_display.extend([t for t in st.session_state[session_key] if t not in ASSET_LIST])
        
        selected_options = st.multiselect(
            f"{asset_label} tickers",
            options=list(formatted_options.keys()),
            default=selected_display,
            placeholder=f"Choose {asset_label.lower()}s to compare. Example: GC=F - Gold",
            accept_new_options=True,
            key=f"{asset_type}_selector"
        )
        
        # Map back to actual symbols
        tickers = []
        for option in selected_options:
            if option in formatted_options:
                tickers.append(formatted_options[option])
            else:
                # User entered a custom option
                tickers.append(option.split(" - ")[0] if " - " in option else option)
        
    elif asset_type == "Bonds":
        # Format options as "^TNX - 10-Year Treasury Yield"
        formatted_options = {}
        options_list = sorted(set(ASSET_LIST) | set(st.session_state[session_key]))
        for symbol in options_list:
            friendly_name = BOND_NAMES.get(symbol, symbol)
            formatted_options[f"{symbol} - {friendly_name}"] = symbol
        
        # Display info about bond symbols
        with st.expander("ℹ️ What do these symbols mean?", expanded=False):
            st.markdown("""
            **Bond Symbols Explained:**
            - **^TNX** = 10-Year US Treasury Yield
            - **^IRX** = 13 Week US Treasury Bill
            - **^FVX** = 5-Year US Treasury Yield
            - **^TYX** = 30-Year US Treasury Yield
            
            *Symbols starting with "^" are indices. Higher yields typically indicate higher interest rates.*
            """)
        
        # Multiselect with formatted options
        selected_display = [f"{t} - {BOND_NAMES.get(t, t)}" for t in st.session_state[session_key] if t in ASSET_LIST]
        selected_display.extend([t for t in st.session_state[session_key] if t not in ASSET_LIST])
        
        selected_options = st.multiselect(
            f"{asset_label} tickers",
            options=list(formatted_options.keys()),
            default=selected_display,
            placeholder=f"Choose {asset_label.lower()}s to compare. Example: ^TNX - 10-Year Treasury Yield",
            accept_new_options=True,
            key=f"{asset_type}_selector"
        )
        
        # Map back to actual symbols
        tickers = []
        for option in selected_options:
            if option in formatted_options:
                tickers.append(formatted_options[option])
            else:
                # User entered a custom option
                tickers.append(option.split(" - ")[0] if " - " in option else option)
    elif asset_type == "Mutual Funds":
        # Format options as "HDFCEQUITY.NS - HDFC Equity Fund"
        formatted_options = {}
        options_list = sorted(set(ASSET_LIST) | set(st.session_state[session_key]))
        for symbol in options_list:
            friendly_name = MUTUAL_FUND_NAMES.get(symbol, symbol)
            formatted_options[f"{symbol} - {friendly_name}"] = symbol
        
        # Display info about mutual funds
        with st.expander("ℹ️ About Mutual Funds & ETFs", expanded=False):
            st.markdown("""
            **ETF Categories:**
            - **Large Cap / Broad Market**: Track major indices (Nifty 50, Nifty Next 50, Sensex)
            - **Mid & Small Cap**: Focus on mid and small-cap companies
            - **Sectoral ETFs**: Track specific sectors (Banking, IT, Pharma, Energy, FMCG, etc.)
            - **Thematic ETFs**: Track themes (Consumption, Infrastructure)
            - **Commodity ETFs**: Gold, Silver ETFs
            - **Debt / Liquid**: Liquid ETFs for short-term investments
            
            **Note**: 
            - ETFs trade like stocks and have real-time prices during market hours
            - Many traditional mutual funds are not available on Yahoo Finance
            - This list focuses on ETFs which are more reliably available
            - Historical data shows end-of-day prices
            """)
        
        # Category filter (optional enhancement)
        selected_category = st.selectbox(
            "Filter by Category (Optional)",
            ["All Categories"] + list(MUTUAL_FUND_CATEGORIES.keys()),
            key="mf_category_filter"
        )
        
        if selected_category != "All Categories":
            category_funds = MUTUAL_FUND_CATEGORIES.get(selected_category, [])
            options_list = [f for f in options_list if f in category_funds]
            formatted_options = {k: v for k, v in formatted_options.items() if v in category_funds}
        
        # Multiselect with formatted options
        # Filter out invalid tickers from session state that don't exist in current ASSET_LIST
        valid_session_tickers = [t for t in st.session_state[session_key] if t in ASSET_LIST]
        
        # Build selected_display with only valid tickers that exist in formatted_options
        selected_display = []
        for t in valid_session_tickers:
            formatted_option = f"{t} - {MUTUAL_FUND_NAMES.get(t, t)}"
            if formatted_option in formatted_options:
                selected_display.append(formatted_option)
        
        selected_options = st.multiselect(
            f"{asset_label} tickers",
            options=list(formatted_options.keys()),
            default=selected_display,
            placeholder=f"Choose {asset_label.lower()}s to compare. Example: NIFTYBEES.NS - Nifty 50 ETF",
            accept_new_options=True,
            key=f"{asset_type}_selector"
        )
        
        # Map back to actual symbols
        tickers = []
        for option in selected_options:
            if option in formatted_options:
                tickers.append(formatted_options[option])
            else:
                tickers.append(option.split(" - ")[0] if " - " in option else option)
    else:
        # Stocks - no formatting needed
        example_placeholder = "RELIANCE.NS"
        tickers = st.multiselect(
            f"{asset_label} tickers",
            options=sorted(set(ASSET_LIST) | set(st.session_state[session_key])),
            default=st.session_state[session_key],
            placeholder=f"Choose {asset_label.lower()}s to compare. Example: {example_placeholder}",
            accept_new_options=True,
            key=f"{asset_type}_selector"
        )
    
    # Update session state
    st.session_state[session_key] = tickers

# Display marquee with all stocks news at the top (only for stocks)
if asset_type == "Stocks" and _marquee_news:
    try:
        # Create marquee HTML
        news_items = []
        for article in _marquee_news:
            title = article.get('title', '').strip()
            ticker = article.get('ticker', '')
            link = article.get('link', '#')
            publish_time = article.get('providerPublishTime', 0)
            date_str = format_news_date(publish_time)
            
            # Determine sentiment color
            summary = article.get('summary', '')
            is_growth = is_growth_related(title, summary)
            is_depreciation = is_depreciation_related(title, summary)
            
            if is_growth:
                color = "#00cc00"
                icon = "📈"
            elif is_depreciation:
                color = "#ff4444"
                icon = "📉"
            else:
                color = "#888888"
                icon = "📰"
            
            news_items.append(
                f'<span style="color: {color}; margin-right: 30px;">{icon} <strong>{ticker}</strong>: '
                f'<a href="{link}" target="_blank" style="color: {color}; text-decoration: none;">{title}</a> '
                f'({date_str})</span>'
            )
        
        if news_items:
            marquee_html = f"""
            <div style="background: linear-gradient(90deg, #1e3a5f 0%, #2d4a6e 100%); 
                        padding: 12px 0; 
                        border-radius: 5px; 
                        margin-bottom: 20px;
                        overflow: hidden;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="display: flex; align-items: center;">
                    <span style="color: #ffd700; font-weight: bold; margin-right: 15px; white-space: nowrap; padding-left: 10px;">
                        📊 Market News:
                    </span>
                    <marquee behavior="scroll" direction="left" scrollamount="3" style="color: white; font-size: 14px;">
                        {' • '.join(news_items)}
                    </marquee>
                </div>
            </div>
            """
            st.markdown(marquee_html, unsafe_allow_html=True)
    except Exception:
        # Silently fail if marquee news can't be displayed
        pass

# Time horizon selector
horizon_map = {
    "1 Months": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "5 Years": "5y",
    "10 Years": "10y",
    "20 Years": "20y",
}

with top_left_cell:
    # Buttons for picking time horizon
    horizon = st.pills(
        "Time horizon",
        options=list(horizon_map.keys()),
        default="6 Months",
    )

tickers = [t.upper() for t in tickers]

# Update query param when text input changes
if tickers:
    st.query_params[f"{asset_type.lower()}_stocks"] = stocks_to_str(tickers)
else:
    # Clear the param if input is empty
    st.query_params.pop(f"{asset_type.lower()}_stocks", None)

if not tickers:
    top_left_cell.info(f"Pick some {asset_label.lower()}s to compare", icon=":material/info:")
    st.stop()


right_cell = cols[1].container(
    border=True, height="stretch", vertical_alignment="center"
)


@st.cache_resource(show_spinner=False, ttl="6h")
def load_data(tickers, period):
    tickers_obj = yf.Tickers(tickers)
    data = tickers_obj.history(period=period)
    if data is None:
        raise RuntimeError("YFinance returned no data.")
    return data["Close"]


def fetch_news_finnhub(ticker: str, api_key: Optional[str] = None) -> List[Dict]:
    """Fetch news from Finnhub API (free tier available)."""
    articles = []
    try:
        # Remove .NS or .BO suffix for Finnhub
        symbol = ticker.split('.')[0]
        url = f"https://finnhub.io/api/v1/company-news"
        params = {
            'symbol': symbol,
            'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'to': datetime.now().strftime('%Y-%m-%d')
        }
        # Always use API key if provided (required for better rate limits)
        if api_key:
            params['token'] = api_key
        else:
            # Without API key, Finnhub has very limited access
            return articles
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                for item in data[:20]:  # Limit to 20 articles
                    article = {
                        'title': item.get('headline', ''),
                        'summary': item.get('summary', ''),
                        'link': item.get('url', ''),
                        'publisher': item.get('source', 'Finnhub'),
                        'providerPublishTime': item.get('datetime', 0),
                        'ticker': ticker
                    }
                    if is_valid_article(article):
                        articles.append(article)
    except Exception:
        pass
    return articles


def fetch_news_tavily(ticker: str, api_key: Optional[str] = None) -> List[Dict]:
    """Fetch news from Tavily API (AI-powered news search)."""
    articles = []
    if not api_key:
        return articles
    
    try:
        # Remove .NS or .BO suffix for search
        symbol = ticker.split('.')[0]
        
        # Tavily API endpoint
        url = "https://api.tavily.com/search"
        payload = {
            'api_key': api_key,
            'query': f"{symbol} stock news",
            'topic': 'news',
            'max_results': 20,
            'search_depth': 'basic',
            'include_answer': False,
            'include_raw_content': False
        }
        
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                for item in data.get('results', [])[:20]:
                    # Tavily doesn't always provide published date, use current time as fallback
                    timestamp = int(time.time())
                    try:
                        # Check if there's a published_date field
                        if 'published_date' in item:
                            pub_date_str = item.get('published_date', '')
                            if pub_date_str:
                                try:
                                    pub_date = datetime.fromisoformat(pub_date_str.replace('Z', '+00:00'))
                                    timestamp = int(pub_date.timestamp())
                                except:
                                    pass
                    except:
                        pass
                    
                    article = {
                        'title': item.get('title', ''),
                        'summary': item.get('content', '')[:500],  # Limit summary length
                        'link': item.get('url', ''),
                        'publisher': item.get('source', 'Tavily'),
                        'providerPublishTime': timestamp,
                        'ticker': ticker
                    }
                    if is_valid_article(article):
                        articles.append(article)
    except Exception:
        pass
    return articles


@st.cache_resource(show_spinner=False, ttl="30m")
def load_news_multi_source(tickers: List[str]) -> Dict[str, List[Dict]]:
    """Load news from multiple sources for better coverage."""
    news_data = {}
    
    # Get API keys from streamlit secrets
    try:
        finnhub_key = st.secrets.get("FINNHUB_API_KEY", None)
        newsapi_key = st.secrets.get("NEWSAPI_KEY", None)
    except Exception as e:
        # On Streamlit Cloud, if secrets aren't configured, this is expected
        finnhub_key = None
        newsapi_key = None
    
    for ticker in tickers:
        all_articles = []
        
        # Try Finnhub first (free tier, no key required for limited requests)
        try:
            finnhub_news = fetch_news_finnhub(ticker, finnhub_key)
            if finnhub_news:
                all_articles.extend(finnhub_news)
        except Exception as e:
            # Silently continue to next source
            pass
        
        # Try Tavily if key is available
        if newsapi_key:
            try:
                tavily_news = fetch_news_tavily(ticker, newsapi_key)
                if tavily_news:
                    all_articles.extend(tavily_news)
            except Exception as e:
                # Silently continue to next source
                pass
        
        # Fallback to yfinance (this should always work)
        try:
            ticker_obj = yf.Ticker(ticker)
            # Try to get news - yfinance.news might return None, empty list, or raise exception
            try:
                yf_news = ticker_obj.news
            except:
                yf_news = None
            
            # yfinance.news might return None or empty list
            if yf_news is None:
                yf_news = []
            
            # Also try without .NS suffix for Indian stocks (some APIs work better this way)
            if (not yf_news or len(yf_news) == 0) and ticker.endswith('.NS'):
                try:
                    base_ticker = ticker.replace('.NS', '')
                    base_ticker_obj = yf.Ticker(base_ticker)
                    try:
                        yf_news = base_ticker_obj.news
                        if yf_news is None:
                            yf_news = []
                    except:
                        pass
                except:
                    pass
            
            if yf_news and isinstance(yf_news, list) and len(yf_news) > 0:
                for article in yf_news:
                    if not isinstance(article, dict):
                        continue
                    
                    # Normalize yfinance article format
                    normalized_article = {
                        'title': article.get('title', ''),
                        'summary': article.get('summary', article.get('description', '')),
                        'link': article.get('link', article.get('url', '')),
                        'publisher': article.get('publisher', article.get('source', 'Yahoo Finance')),
                        'ticker': ticker
                    }
                    
                    # Handle timestamp - yfinance uses 'providerPublishTime' or 'pubDate'
                    timestamp = article.get('providerPublishTime', 0)
                    if timestamp == 0:
                        timestamp = article.get('pubDate', 0)
                    if timestamp == 0:
                        # Try to parse from 'publishedAt' if it's a string
                        pub_at = article.get('publishedAt', '')
                        if pub_at:
                            try:
                                # Try ISO format first
                                dt = datetime.fromisoformat(str(pub_at).replace('Z', '+00:00'))
                                timestamp = int(dt.timestamp())
                            except:
                                try:
                                    # Try common date formats
                                    dt = datetime.strptime(str(pub_at), '%Y-%m-%d %H:%M:%S')
                                    timestamp = int(dt.timestamp())
                                except:
                                    pass
                    if timestamp == 0:
                        # If no timestamp, use current time as fallback
                        timestamp = int(time.time())
                    
                    normalized_article['providerPublishTime'] = timestamp
                    
                    if is_valid_article(normalized_article):
                        all_articles.append(normalized_article)
        except Exception as e:
            # If yfinance fails, log but continue
            pass
        
        # Remove duplicates based on title similarity
        unique_articles = []
        seen_titles = set()
        for article in all_articles:
            title_lower = article.get('title', '').lower().strip()
            # Simple deduplication - check if similar title exists
            is_duplicate = False
            for seen in seen_titles:
                # Check if titles are very similar (simple approach)
                if title_lower and seen and (title_lower == seen or title_lower in seen or seen in title_lower):
                    is_duplicate = True
                    break
            if not is_duplicate and title_lower:
                unique_articles.append(article)
                seen_titles.add(title_lower)
        
        # Sort by date (newest first)
        unique_articles.sort(key=lambda x: x.get('providerPublishTime', 0), reverse=True)
        
        if unique_articles:
            news_data[ticker] = unique_articles[:30]  # Limit to 30 per ticker
        # Note: We don't add empty lists - only add tickers that have articles
    
    return news_data


@st.cache_resource(show_spinner=False, ttl="1h")
def load_news(tickers: List[str]) -> Dict[str, List[Dict]]:
    """Load news articles for given tickers (uses multi-source approach)."""
    try:
        return load_news_multi_source(tickers)
    except Exception as e:
        # Return empty dict on error, but log for debugging
        return {}


# Load the data
try:
    data = load_data(tickers, horizon_map[horizon])
except yf.exceptions.YFRateLimitError as e:
    st.warning("YFinance is rate-limiting us :(\nTry again later.")
    load_data.clear()  # Remove the bad cache entry.
    st.stop()

empty_columns = data.columns[data.isna().all()].tolist()

if empty_columns:
    st.error(f"Error loading data for the tickers: {', '.join(empty_columns)}.")
    st.stop()

# Normalize prices (start at 1)
# Handle cases where first value might be 0 or NaN
normalized = data.div(data.iloc[0].replace(0, pd.NA))
# Replace inf values (from division by zero) with NaN
normalized = normalized.replace([float('inf'), float('-inf')], pd.NA)

# Filter out NaN values and get latest normalized values
latest_norm_values = {}
for ticker in tickers:
    latest_value = normalized[ticker].iat[-1]
    if pd.notna(latest_value) and pd.notna(normalized[ticker].iloc[0]):
        latest_norm_values[latest_value] = ticker

# Only show metrics if we have valid data
if latest_norm_values:
    max_norm_value = max(latest_norm_values.items())
    min_norm_value = min(latest_norm_values.items())
    
    bottom_left_cell = cols[0].container(
        border=True, height="stretch", vertical_alignment="center"
    )
    
    with bottom_left_cell:
        cols = st.columns(2)
        # Safely calculate delta, handling NaN cases
        max_delta = max_norm_value[0] * 100 if pd.notna(max_norm_value[0]) else 0
        min_delta = min_norm_value[0] * 100 if pd.notna(min_norm_value[0]) else 0
        
        cols[0].metric(
            "Best stock",
            max_norm_value[1],
            delta=f"{round(max_delta)}%",
            width="content",
        )
        cols[1].metric(
            "Worst stock",
            min_norm_value[1],
            delta=f"{round(min_delta)}%",
            width="content",
        )
else:
    bottom_left_cell = cols[0].container(
        border=True, height="stretch", vertical_alignment="center"
    )
    with bottom_left_cell:
        st.warning("Unable to calculate performance metrics. Some stocks may have missing data.")

# Performance Leaderboard
st.markdown("---")
leaderboard_container = st.container(border=True)

with leaderboard_container:
    st.markdown("## Performance Leaderboard")
    
    # Dropdown to select leaderboard type (only for stocks)
    if asset_type == "Stocks":
        leaderboard_type = st.selectbox(
            "Select Leaderboard Type",
            ["Current Selected Stocks", "Top Indian Stocks"],
            key="leaderboard_type"
        )
        
        # Define top Indian stocks (major large-cap stocks)
        top_indian_stocks = [
            "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
            "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS",
            "LT.NS", "HCLTECH.NS", "AXISBANK.NS", "ASIANPAINT.NS", "MARUTI.NS",
            "WIPRO.NS", "NESTLEIND.NS", "SUNPHARMA.NS", "BAJFINANCE.NS", "TITAN.NS"
        ]
        
        # Determine which stocks to show in leaderboard
        if leaderboard_type == "Top Indian Stocks":
            assets_for_leaderboard = top_indian_stocks
            st.caption(f"Ranking of top {len(top_indian_stocks)} Indian stocks by their performance over the selected time period.")
            
            # Load data for top Indian stocks
            try:
                top_stocks_data = load_data(assets_for_leaderboard, horizon_map[horizon])
                
                # Normalize prices
                top_stocks_normalized = top_stocks_data.div(top_stocks_data.iloc[0].replace(0, pd.NA))
                top_stocks_normalized = top_stocks_normalized.replace([float('inf'), float('-inf')], pd.NA)
                
                # Get latest normalized values for top stocks
                top_stocks_norm_values = {}
                for ticker in assets_for_leaderboard:
                    if ticker in top_stocks_normalized.columns:
                        latest_value = top_stocks_normalized[ticker].iat[-1]
                        if pd.notna(latest_value) and pd.notna(top_stocks_normalized[ticker].iloc[0]):
                            top_stocks_norm_values[latest_value] = ticker
                
                leaderboard_norm_values = top_stocks_norm_values
            except Exception as e:
                st.error(f"Error loading data for top Indian stocks: {str(e)}")
                leaderboard_norm_values = latest_norm_values if latest_norm_values else {}
        else:
            assets_for_leaderboard = tickers
            st.caption("Ranking of all selected stocks by their performance over the selected time period.")
            leaderboard_norm_values = latest_norm_values
    else:
        # For commodities, bonds, and mutual funds, just use selected items
        assets_for_leaderboard = tickers
        if asset_type == "Commodities":
            st.caption("Ranking of selected commodities by their performance over the selected time period.")
        elif asset_type == "Bonds":
            st.caption("Ranking of selected bonds by their performance over the selected time period.")
        elif asset_type == "Mutual Funds":
            st.caption("Ranking of selected mutual funds by their performance over the selected time period.")
        leaderboard_norm_values = latest_norm_values
    
    if leaderboard_norm_values and len(leaderboard_norm_values) > 1:
        # Create leaderboard data
        leaderboard_data = []
        for norm_value, ticker in leaderboard_norm_values.items():
            if pd.notna(norm_value):
                performance_pct = (norm_value - 1.0) * 100
                # Use friendly name for display
                display_name = get_display_name(ticker, asset_type)
                leaderboard_data.append({
                    'Asset': f"{ticker} - {display_name}" if asset_type in ["Commodities", "Bonds", "Mutual Funds"] and display_name != ticker else ticker,
                    'Asset_Original': ticker,  # Keep original for sorting/filtering
                    'Performance %': round(performance_pct, 2),
                    'Normalized Value': round(norm_value, 4)
                })
        
        # Sort by performance (descending)
        leaderboard_data.sort(key=lambda x: x['Performance %'], reverse=True)
        leaderboard_df = pd.DataFrame(leaderboard_data)
        
        # Add rank column
        leaderboard_df.insert(0, 'Rank', range(1, len(leaderboard_df) + 1))
        
        # Create horizontal bar chart
        chart_data = leaderboard_df.copy()
        
        # Color bars based on performance (green for positive, red for negative)
        chart_data['Color'] = chart_data['Performance %'].apply(
            lambda x: '#10B981' if x >= 0 else '#EF4444'
        )
        
        # Create the bar chart
        bars = alt.Chart(chart_data).mark_bar(
            cornerRadiusTopRight=5,
            cornerRadiusBottomRight=5
        ).encode(
            y=alt.Y(
                'Asset:N',
                sort=alt.EncodingSortField(field='Performance %', order='descending'),
                title=asset_label,
                axis=alt.Axis(labelLimit=300)
            ),
            x=alt.X(
                'Performance %:Q',
                title='Performance (%)',
                axis=alt.Axis(format='.1f')
            ),
            color=alt.Color(
                'Color:N',
                scale=None,
                legend=None
            ),
            tooltip=[
                alt.Tooltip('Rank:O', title='Rank'),
                alt.Tooltip('Asset:N', title=asset_label),
                alt.Tooltip('Performance %:Q', title='Performance', format='.2f'),
                alt.Tooltip('Normalized Value:Q', title='Normalized Value', format='.4f')
            ]
        ).properties(
            height=max(400, len(leaderboard_df) * 40),
            title=f'{asset_label} Performance Ranking'
        )
        
        # Add text labels on bars
        text = bars.mark_text(
            align='left',
            baseline='middle',
            dx=3,
            color='white',
            fontSize=11,
            fontWeight='bold'
        ).encode(
            text=alt.Text('Performance %:Q', format='+.2f')
        )
        
        # Combine chart and text
        leaderboard_chart = (bars + text).configure_view(
            strokeWidth=0
        ).configure_axis(
            gridColor='#333333',
            domainColor='#666666',
            labelColor='#CCCCCC',
            titleColor='#CCCCCC'
        )
        
        # Display chart
        st.altair_chart(leaderboard_chart, use_container_width=True)
        
        # Also show as a table below the chart
        with st.expander("View Leaderboard Table", expanded=False):
            # Format the dataframe for display
            display_df = leaderboard_df.copy()
            display_df['Performance %'] = display_df['Performance %'].apply(lambda x: f"{x:+.2f}%")
            display_df['Normalized Value'] = display_df['Normalized Value'].apply(lambda x: f"{x:.4f}")
            display_df = display_df.rename(columns={
                'Rank': 'Rank',
                'Asset': asset_label,
                'Performance %': 'Performance',
                'Normalized Value': 'Normalized Value'
            })
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
    elif leaderboard_norm_values and len(leaderboard_norm_values) == 1:
        st.info(f"Select at least 2 {asset_label.lower()}s to view the leaderboard.")
    else:
        st.info(f"Unable to generate leaderboard. Some {asset_label.lower()}s may have missing data.")


# Plot normalized prices
with right_cell:
    st.altair_chart(
        alt.Chart(
            normalized.reset_index().melt(
                id_vars=["Date"], var_name="Stock", value_name="Normalized price"
            )
        )
        .mark_line()
        .encode(
            alt.X("Date:T"),
            alt.Y("Normalized price:Q").scale(zero=False),
            alt.Color("Stock:N"),
        )
        .properties(height=400)
    )

""
""

# Plot individual stock vs peer average
"""
## Individual assets vs peer average

For the analysis below, the "peer average" when analyzing asset X always
excludes X itself.
"""

if len(tickers) <= 1:
    st.warning("Pick 2 or more tickers to compare them")
    st.stop()

NUM_COLS = 4
cols = st.columns(NUM_COLS)

# Color palette: orange, dark blue, green, and other complementary colors
color_palette = [
    "#FF6B35",  # Orange
    "#1E3A8A",  # Dark Blue
    "#10B981",  # Green
    "#F59E0B",  # Amber/Orange-Yellow
    "#3B82F6",  # Blue
    "#8B5CF6",  # Purple
    "#EC4899",  # Pink
    "#14B8A6",  # Teal
]

for i, ticker in enumerate(tickers):
    # Skip if ticker doesn't exist in normalized data or has no valid data
    if ticker not in normalized.columns or normalized[ticker].isna().all():
        continue
    
    # Calculate peer average (excluding current stock)
    peers = normalized.drop(columns=[ticker])
    # Only calculate peer average if there are other valid peers
    if peers.empty or peers.isna().all().all():
        continue
    peer_avg = peers.mean(axis=1)

    # Select color for this stock (rotate through palette)
    stock_color = color_palette[i % len(color_palette)]
    peer_color = "#6B7280"  # Gray for peer average

    # Create DataFrame with peer average.
    plot_data = pd.DataFrame(
        {
            "Date": normalized.index,
            ticker: normalized[ticker],
            "Peer average": peer_avg,
        }
    ).melt(id_vars=["Date"], var_name="Series", value_name="Price")

    chart = (
        alt.Chart(plot_data)
        .mark_line(strokeWidth=2.5)
        .encode(
            alt.X("Date:T"),
            alt.Y("Price:Q").scale(zero=False),
            alt.Color(
                "Series:N",
                scale=alt.Scale(
                    domain=[ticker, "Peer average"], 
                    range=[stock_color, peer_color]
                ),
                legend=alt.Legend(orient="bottom", title="Series"),
            ),
            alt.Tooltip(["Date", "Series", "Price"]),
        )
        .properties(title=f"{ticker} vs peer average", height=300)
    )

    cell = cols[(i * 2) % NUM_COLS].container(border=True)
    cell.write("")
    cell.altair_chart(chart, use_container_width=True)

    # Create Delta chart with matching color
    plot_data = pd.DataFrame(
        {
            "Date": normalized.index,
            "Delta": normalized[ticker] - peer_avg,
        }
    )

    chart = (
        alt.Chart(plot_data)
        .mark_area(
            color=stock_color,
            opacity=0.6,
            interpolate='monotone'
        )
        .encode(
            alt.X("Date:T"),
            alt.Y("Delta:Q").scale(zero=False),
            alt.Tooltip(["Date", "Delta"]),
        )
        .properties(title=f"{ticker} minus peer average", height=300)
    )

    cell = cols[(i * 2 + 1) % NUM_COLS].container(border=True)
    cell.write("")
    cell.altair_chart(chart, use_container_width=True)

""
""

"""
## Raw data
"""

data

"""
---
## 📰 Latest News & Market Updates
"""

# Only show news section for stocks
if asset_type == "Stocks":
    # Display color legend for news sentiment
    legend_col1, legend_col2, legend_col3 = st.columns(3)
    with legend_col1:
        st.markdown(
            """
            <div style="background: #1a3a1a; border-left: 4px solid #00cc00; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: #00cc00; font-size: 20px; font-weight: bold;">●</span>
                    <div>
                        <strong style="color: #00cc00;">Green - Growth/Positive</strong>
                        <p style="color: #aaa; font-size: 12px; margin: 4px 0 0 0;">Positive news, growth, profits, gains, upgrades</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with legend_col2:
        st.markdown(
            """
            <div style="background: #3a1a1a; border-left: 4px solid #ff4444; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: #ff4444; font-size: 20px; font-weight: bold;">●</span>
                    <div>
                        <strong style="color: #ff4444;">Red - Depreciation/Negative</strong>
                        <p style="color: #aaa; font-size: 12px; margin: 4px 0 0 0;">Negative news, losses, declines, downgrades</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with legend_col3:
        st.markdown(
            """
            <div style="background: #1a1a3a; border-left: 4px solid #4A90E2; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: #4A90E2; font-size: 20px; font-weight: bold;">●</span>
                    <div>
                        <strong style="color: #4A90E2;">Blue - General/Neutral</strong>
                        <p style="color: #aaa; font-size: 12px; margin: 4px 0 0 0;">General news, updates, neutral information</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Load and display news if at least one stock is selected
    if tickers:
        try:
            with st.spinner("Loading news articles..."):
                # Always clear cache first to ensure fresh data
                load_news.clear()
                load_news_multi_source.clear()
                
                # Try loading news
                news_data = load_news_multi_source(tickers)
                
                # If still empty, try direct yfinance fetch as last resort
                if not news_data or all(len(articles) == 0 for articles in news_data.values()):
                    # Direct fetch without cache
                    news_data = {}
                    for ticker in tickers:
                        try:
                            ticker_obj = yf.Ticker(ticker)
                            yf_news = ticker_obj.news
                            if yf_news and isinstance(yf_news, list) and len(yf_news) > 0:
                                articles = []
                                for article in yf_news:
                                    if not isinstance(article, dict):
                                        continue
                                    
                                    normalized_article = {
                                        'title': article.get('title', ''),
                                        'summary': article.get('summary', article.get('description', '')),
                                        'link': article.get('link', article.get('url', '')),
                                        'publisher': article.get('publisher', article.get('source', 'Yahoo Finance')),
                                        'ticker': ticker
                                    }
                                    
                                    timestamp = article.get('providerPublishTime', 0)
                                    if timestamp == 0:
                                        timestamp = article.get('pubDate', 0)
                                    if timestamp == 0:
                                        pub_at = article.get('publishedAt', '')
                                        if pub_at:
                                            try:
                                                dt = datetime.fromisoformat(str(pub_at).replace('Z', '+00:00'))
                                                timestamp = int(dt.timestamp())
                                            except:
                                                try:
                                                    dt = datetime.strptime(str(pub_at), '%Y-%m-%d %H:%M:%S')
                                                    timestamp = int(dt.timestamp())
                                                except:
                                                    timestamp = int(time.time())
                                    if timestamp == 0:
                                        timestamp = int(time.time())
                                    
                                    normalized_article['providerPublishTime'] = timestamp
                                    
                                    if is_valid_article(normalized_article):
                                        articles.append(normalized_article)
                                
                                if articles:
                                    news_data[ticker] = articles
                        except Exception as e:
                            continue
            
            # Collect all articles from all selected stocks
            all_articles = []
            total_fetched = 0
            total_validated = 0
            for ticker, articles in news_data.items():
                if articles:  # Check if articles list exists and is not empty
                    total_fetched += len(articles)
                    for article in articles:
                        if is_valid_article(article):
                            article['source_ticker'] = ticker
                            all_articles.append(article)
                            total_validated += 1
            
            # Debug info (only show if no articles found)
            if not all_articles:
                if total_fetched > 0:
                    st.warning(f"Fetched {total_fetched} articles but {total_validated} passed validation. This might indicate a data format issue.")
                    # Show debug info in expander
                    with st.expander("Debug: See fetched articles"):
                        for ticker, articles in news_data.items():
                            if articles:
                                st.write(f"**{ticker}**: {len(articles)} articles")
                                for i, article in enumerate(articles[:3]):  # Show first 3
                                    st.json({
                                        'title': article.get('title', 'N/A'),
                                        'has_link': bool(article.get('link')),
                                        'timestamp': article.get('providerPublishTime', 0),
                                        'valid': is_valid_article(article)
                                    })
                else:
                    # Show helpful message
                    st.info("No news articles found for the selected stocks. This could be due to:")
                    st.markdown("""
                    - **Temporary API unavailability**: News services may be temporarily down
                    - **No recent news**: The selected stocks may not have recent news articles
                    - **API rate limits**: Too many requests may have triggered rate limiting
                    - **Try**: Select different stocks or refresh the page in a few minutes
                    """)
                    # Show which tickers were tried
                    st.caption(f"Attempted to fetch news for: {', '.join(tickers)}")
            
            if all_articles:
                # Sort by sentiment (green first, then red, then blue), then by date (newest first)
                def get_sentiment_priority(article):
                    title = article.get('title', '').strip()
                    summary = article.get('summary', '').strip()
                    is_growth = is_growth_related(title, summary)
                    is_depreciation = is_depreciation_related(title, summary)
                    
                    # Priority: 0 = green (growth), 1 = red (depreciation), 2 = blue (general)
                    if is_growth:
                        return 0
                    elif is_depreciation:
                        return 1
                    else:
                        return 2
                
                # Sort by sentiment priority first, then by date (newest first)
                all_articles.sort(key=lambda x: (
                    get_sentiment_priority(x),
                    -x.get('providerPublishTime', 0)  # Negative for descending order (newest first)
                ))
                
                # Display in flashcard grid (3 columns)
                st.caption(f"Showing {len(all_articles)} news articles • Last updated: {datetime.now().strftime('%H:%M:%S')}")
                
                # Display articles in rows of 3 cards
                num_cols = 3
                for i in range(0, len(all_articles), num_cols):
                    cols = st.columns(num_cols)
                    batch = all_articles[i:i+num_cols]
                    
                    for col_idx, article in enumerate(batch):
                        if col_idx >= len(cols):
                            break
                        
                        with cols[col_idx]:
                            title = article.get('title', '').strip()
                            link = article.get('link', '#')
                            publisher = article.get('publisher', 'Unknown')
                            publish_time = article.get('providerPublishTime', 0)
                            summary = article.get('summary', '').strip()
                            ticker = article.get('source_ticker', article.get('ticker', ''))
                            
                            if not title:
                                continue
                            
                            # Determine sentiment and color
                            is_growth = is_growth_related(title, summary)
                            is_depreciation = is_depreciation_related(title, summary)
                            time_str = format_news_date(publish_time)
                            
                            # Color coding: green for growth, red for depreciation, blue for general
                            if is_growth:
                                ticker_color = "#00cc00"  # Green
                            elif is_depreciation:
                                ticker_color = "#ff4444"  # Red
                            else:
                                ticker_color = "#4A90E2"  # Blue
                            
                            # Create flashcard with dark theme styling (matching the image)
                            # Truncate summary for display
                            summary_display = summary[:150] + ('...' if len(summary) > 150 else '') if summary else ''
                            
                            # Escape HTML special characters to prevent XSS
                            import html
                            title_escaped = html.escape(title)
                            summary_escaped = html.escape(summary_display)
                            publisher_escaped = html.escape(publisher)
                            ticker_escaped = html.escape(ticker)
                            
                            card_html = f"""
                            <div style="
                                background: #2a2a2a;
                                border: 1px solid #3a3a3a;
                                border-radius: 10px;
                                padding: 20px;
                                margin-bottom: 20px;
                                height: 100%;
                                display: flex;
                                flex-direction: column;
                                box-shadow: 0 4px 6px rgba(0,0,0,0.4);
                                transition: transform 0.2s;
                            ">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                                    <span style="color: {ticker_color}; font-weight: 700; font-size: 20px; letter-spacing: 0.5px;">{ticker_escaped}</span>
                                    <span style="color: #999; font-size: 13px; font-weight: 400;">{time_str}</span>
                                </div>
                                <a href="{link}" target="_blank" style="text-decoration: none; color: #fff; display: block; margin-bottom: 12px;">
                                    <h3 style="color: #fff; font-size: 17px; font-weight: 700; margin: 0; line-height: 1.4; letter-spacing: -0.2px;">
                                        {title_escaped}
                                    </h3>
                                </a>
                                <p style="color: #bbb; font-size: 14px; line-height: 1.6; margin: 0 0 16px 0; flex-grow: 1; overflow: hidden;">
                                    {summary_escaped}
                                </p>
                                <div style="color: #888; font-size: 12px; margin-top: auto; border-top: 1px solid #3a3a3a; padding-top: 12px;">
                                    {publisher_escaped}
                                </div>
                            </div>
                            """
                            st.markdown(card_html, unsafe_allow_html=True)
            else:
                # Show helpful message if no articles found
                st.info("No news articles available for the selected stocks at this time.")
                st.caption(f"Attempted to load news for: {', '.join(tickers)}")
                st.caption("💡 Tip: Try selecting different stocks or check back later. News is fetched from multiple sources.")
        except Exception as e:
            # More detailed error message for debugging
            st.error(f"Error loading news: {str(e)}")
            st.caption("If this persists, the news service may be temporarily unavailable. The app will continue to work for stock analysis.")
            # Log the error for debugging (only visible in logs, not to user)
            import traceback
            st.code(traceback.format_exc(), language='python')
    else:
        st.info("Select at least one stock to view news articles.")
else:
    if asset_type == "Mutual Funds":
        st.info("📰 News is currently available only for stocks. Switch to 'Stocks' to view market news.")
    else:
        st.info("📰 News is currently available only for stocks. Switch to 'Stocks' to view market news.")
