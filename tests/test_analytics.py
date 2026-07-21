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


def test_historical_var_positive_magnitude():
    r = pd.Series(list(np.linspace(-0.05, 0.05, 100)))
    v = a.historical_var(r, 0.95)
    assert v > 0


def test_cvar_at_least_var():
    r = pd.Series(list(np.linspace(-0.05, 0.05, 100)))
    assert a.cvar(r, 0.95) >= a.historical_var(r, 0.95)


def test_beta_of_scaled_series_is_scale():
    bench = pd.Series([0.01, -0.02, 0.03, -0.015, 0.02])
    port = bench * 2.0
    assert abs(a.beta(port, bench) - 2.0) < 1e-9


def test_parametric_var_finite():
    r = pd.Series([0.001, -0.002, 0.003, -0.001] * 20)
    assert np.isfinite(a.parametric_var(r, 0.95))


def test_correlation_anti_correlated():
    ar = pd.DataFrame({"A": [0.01, -0.01, 0.01, -0.01],
                       "B": [-0.01, 0.01, -0.01, 0.01]})
    c = a.correlation_matrix(ar)
    assert abs(c.loc["A", "B"] - (-1.0)) < 1e-9


def test_risk_contribution_sums_to_one():
    ar = pd.DataFrame({"A": [0.01, -0.02, 0.03, -0.01],
                       "B": [0.02, 0.01, -0.01, 0.005]})
    rc = a.risk_contribution(ar, [0.5, 0.5])
    assert abs(rc.sum() - 1.0) < 1e-9


def test_compute_metrics_bundles_everything():
    prices = pd.DataFrame({"A": [100, 101, 102, 101, 103],
                           "B": [50, 49, 51, 52, 50]})
    bench = pd.Series([200, 201, 199, 202, 203])
    m = a.compute_metrics(prices, [0.6, 0.4], bench, rf=0.0)
    assert hasattr(m, "sharpe") and hasattr(m, "risk_contribution")
    assert abs(m.risk_contribution.sum() - 1.0) < 1e-9
    assert np.isfinite(m.max_drawdown)
