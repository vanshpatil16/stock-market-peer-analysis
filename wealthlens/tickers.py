"""Curated ticker universe for the WealthLens holdings picker.

Kept separate from the Streamlit app module (which has import-time UI side
effects) so it can be imported and unit-tested freely. Symbols are Yahoo
Finance NSE tickers; the picker shows ``"SYMBOL — Name"`` labels so users pick
a holding by company name instead of memorising exact tickers and suffixes.
"""
from __future__ import annotations

_LABEL_SEP = " — "

# Nifty-50-style large caps. Extend freely — the picker and label/symbol
# helpers derive everything from this single mapping.
TICKER_NAMES: dict[str, str] = {
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "HDFCBANK.NS": "HDFC Bank",
    "INFY.NS": "Infosys",
    "ICICIBANK.NS": "ICICI Bank",
    "HINDUNILVR.NS": "Hindustan Unilever",
    "ITC.NS": "ITC",
    "SBIN.NS": "State Bank of India",
    "BHARTIARTL.NS": "Bharti Airtel",
    "KOTAKBANK.NS": "Kotak Mahindra Bank",
    "LT.NS": "Larsen & Toubro",
    "HCLTECH.NS": "HCL Technologies",
    "AXISBANK.NS": "Axis Bank",
    "ASIANPAINT.NS": "Asian Paints",
    "MARUTI.NS": "Maruti Suzuki",
    "WIPRO.NS": "Wipro",
    "NESTLEIND.NS": "Nestle India",
    "SUNPHARMA.NS": "Sun Pharmaceutical",
    "BAJFINANCE.NS": "Bajaj Finance",
    "TITAN.NS": "Titan Company",
    "ULTRACEMCO.NS": "UltraTech Cement",
    "ONGC.NS": "Oil & Natural Gas Corp",
    "NTPC.NS": "NTPC",
    "POWERGRID.NS": "Power Grid Corp",
    "COALINDIA.NS": "Coal India",
    "ADANIPORTS.NS": "Adani Ports & SEZ",
    "ADANIENT.NS": "Adani Enterprises",
    "JSWSTEEL.NS": "JSW Steel",
    "TATAMOTORS.NS": "Tata Motors",
    "TATASTEEL.NS": "Tata Steel",
    "TECHM.NS": "Tech Mahindra",
    "BAJAJFINSV.NS": "Bajaj Finserv",
    "HDFCLIFE.NS": "HDFC Life Insurance",
    "BRITANNIA.NS": "Britannia Industries",
    "INDUSINDBK.NS": "IndusInd Bank",
    "DRREDDY.NS": "Dr. Reddy's Laboratories",
    "CIPLA.NS": "Cipla",
    "EICHERMOT.NS": "Eicher Motors",
    "HEROMOTOCO.NS": "Hero MotoCorp",
    "GRASIM.NS": "Grasim Industries",
    "DIVISLAB.NS": "Divi's Laboratories",
    "TATACONSUM.NS": "Tata Consumer Products",
    "BAJAJ-AUTO.NS": "Bajaj Auto",
    "APOLLOHOSP.NS": "Apollo Hospitals",
    "HINDALCO.NS": "Hindalco Industries",
    "SBILIFE.NS": "SBI Life Insurance",
    "M&M.NS": "Mahindra & Mahindra",
    "VEDL.NS": "Vedanta",
    "PIDILITIND.NS": "Pidilite Industries",
    "DABUR.NS": "Dabur India",
}


def label_for(symbol: str) -> str:
    """Return a ``'SYMBOL — Name'`` label, or the bare symbol if unknown."""
    name = TICKER_NAMES.get(symbol)
    return f"{symbol}{_LABEL_SEP}{name}" if name else symbol


def labels() -> list[str]:
    """All known holdings as ``'SYMBOL — Name'`` labels for a picker."""
    return [label_for(s) for s in TICKER_NAMES]


def symbol_from_label(label) -> str:
    """Extract the raw Yahoo symbol from a picker label; ``''`` for empty/None.

    Accepts either a full ``'SYMBOL — Name'`` label or a bare symbol, so it is
    safe to call on manually entered values too.
    """
    if not isinstance(label, str) or not label.strip():
        return ""
    return label.split(_LABEL_SEP, 1)[0].strip().upper()
