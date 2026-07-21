import numpy as np
import pandas as pd
from wealthlens import analytics as a


def test_daily_returns_shape():
    prices = pd.DataFrame({"A": [100, 110, 121]})
    r = a.daily_returns(prices)
    assert len(r) == 2
    assert abs(r["A"].iloc[0] - 0.10) < 1e-9


def test_portfolio_returns_weighted():
    ar = pd.DataFrame({"A": [0.10, 0.00], "B": [0.00, 0.10]})
    pr = a.portfolio_returns(ar, [0.5, 0.5])
    assert abs(pr.iloc[0] - 0.05) < 1e-9
    assert abs(pr.iloc[1] - 0.05) < 1e-9


def test_total_return():
    r = pd.Series([0.10, 0.0])
    assert abs(a.total_return(r) - 0.10) < 1e-9


def test_annualized_volatility_constant_is_zero():
    r = pd.Series([0.01] * 50)
    assert abs(a.annualized_volatility(r)) < 1e-9


def test_annualized_return_positive():
    r = pd.Series([0.001] * 252)
    assert a.annualized_return(r) > 0


def test_sharpe_zero_vol_is_zero():
    r = pd.Series([0.01] * 50)
    assert a.sharpe_ratio(r, rf=0.0) == 0.0


def test_sharpe_positive_when_returns_beat_rf():
    r = pd.Series([0.001, 0.002, -0.001, 0.0015] * 20)
    assert a.sharpe_ratio(r, rf=0.0) > 0


def test_max_drawdown_half():
    r = pd.Series([0.0, -0.5])
    assert abs(a.max_drawdown(r) - (-0.5)) < 1e-9


def test_sortino_finite():
    r = pd.Series([0.001, -0.002, 0.003, -0.001] * 20)
    assert np.isfinite(a.sortino_ratio(r, rf=0.0))
