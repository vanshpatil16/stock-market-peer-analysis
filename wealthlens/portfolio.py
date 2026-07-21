"""Weighted-holdings portfolio model. No Streamlit imports."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Portfolio:
    tickers: tuple[str, ...]
    weights: tuple[float, ...]


def build_portfolio(rows, mode="weight", prices=None):
    # Aggregate raw magnitudes per ticker, dropping blanks; dedupe by summing.
    raw: dict[str, float] = {}
    for row in rows:
        ticker = str(row.get("ticker", "")).strip().upper()
        if not ticker:
            continue
        value = row.get("shares" if mode == "shares" else "weight", 0) or 0
        value = float(value)
        if value < 0:
            raise ValueError(f"Negative value for {ticker} is not allowed.")
        raw[ticker] = raw.get(ticker, 0.0) + value

    if mode == "shares":
        prices = prices or {}
        raw = {t: v * float(prices.get(t, 0.0)) for t, v in raw.items()}

    total = sum(raw.values())
    if not raw or total <= 0:
        raise ValueError("Provide at least one holding with a positive weight.")

    tickers = tuple(raw.keys())
    weights = tuple(raw[t] / total for t in tickers)
    return Portfolio(tickers=tickers, weights=weights)
