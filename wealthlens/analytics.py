"""Pure quantitative analytics. No Streamlit imports."""
from __future__ import annotations
import numpy as np
import pandas as pd
from wealthlens.config import TRADING_DAYS


def daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna(how="all")


def portfolio_returns(asset_returns: pd.DataFrame, weights) -> pd.Series:
    w = np.asarray(weights, dtype=float)
    return asset_returns.mul(w, axis=1).sum(axis=1)


def total_return(r: pd.Series) -> float:
    return float((1.0 + r).prod() - 1.0)


def annualized_return(r: pd.Series) -> float:
    return float(r.mean() * TRADING_DAYS)


def annualized_volatility(r: pd.Series) -> float:
    return float(r.std(ddof=0) * np.sqrt(TRADING_DAYS))
