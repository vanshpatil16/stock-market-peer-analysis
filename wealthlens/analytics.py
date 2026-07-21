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


def sharpe_ratio(r: pd.Series, rf: float) -> float:
    vol = annualized_volatility(r)
    if vol == 0:
        return 0.0
    return float((annualized_return(r) - rf) / vol)


def sortino_ratio(r: pd.Series, rf: float) -> float:
    downside = r[r < 0]
    dd = float(downside.std(ddof=0) * np.sqrt(TRADING_DAYS))
    if dd == 0:
        return 0.0
    return float((annualized_return(r) - rf) / dd)


def max_drawdown(r: pd.Series) -> float:
    cum = (1.0 + r).cumprod()
    running_max = cum.cummax()
    drawdown = cum / running_max - 1.0
    return float(drawdown.min())
