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


def historical_var(r: pd.Series, confidence: float = 0.95) -> float:
    q = float(np.percentile(r, (1.0 - confidence) * 100.0))
    return float(-q)  # positive loss magnitude


def parametric_var(r: pd.Series, confidence: float = 0.95) -> float:
    z = 1.645 if abs(confidence - 0.95) < 1e-6 else 2.326  # 95% / 99%
    mu, sigma = float(r.mean()), float(r.std(ddof=0))
    return float(-(mu - z * sigma))


def cvar(r: pd.Series, confidence: float = 0.95) -> float:
    q = float(np.percentile(r, (1.0 - confidence) * 100.0))
    tail = r[r <= q]
    if len(tail) == 0:
        return float(-q)
    return float(-tail.mean())


def beta(portfolio_r: pd.Series, benchmark_r: pd.Series) -> float:
    df = pd.concat([portfolio_r, benchmark_r], axis=1).dropna()
    if len(df) < 2:
        return float("nan")
    p, b = df.iloc[:, 0], df.iloc[:, 1]
    var_b = float(b.var(ddof=0))
    if var_b == 0:
        return float("nan")
    cov = float(np.cov(p, b, ddof=0)[0, 1])
    return float(cov / var_b)
