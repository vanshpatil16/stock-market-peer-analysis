# WealthLens Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a portfolio-grade quantitative analytics engine (weighted holdings → risk metrics → grounded AI commentary → PDF report) to the existing Streamlit dashboard, as a new "WealthLens" view.

**Architecture:** New logic lives in a pure, Streamlit-free package `wealthlens/` (unit-testable pandas/numpy in, numbers out). A thin Streamlit view (`views/portfolio_view.py`) renders it. The existing `streamlit_app.py` gets a minimal top-level nav router; the current dashboard is untouched.

**Tech Stack:** Python 3.10+, pandas/numpy, Altair, Streamlit, reportlab (PDF), openai + google-generativeai (AI), pytest + pytest-cov. Managed via `uv` / `pyproject.toml` + `requirements.txt`.

## Global Constraints

- Python floor: `requires-python = ">=3.10"` (do not use 3.11+-only syntax).
- `wealthlens/analytics.py` and `wealthlens/portfolio.py` MUST NOT import `streamlit`.
- No API keys hardcoded; read from `st.secrets` or environment (`OPENAI_API_KEY` / `GEMINI_API_KEY`).
- Immutability: models are `@dataclass(frozen=True)`; functions never mutate their inputs.
- Constants live in `wealthlens/config.py` — no magic numbers elsewhere: `TRADING_DAYS = 252`, `BENCHMARK = "^NSEI"`, `RISK_FREE_RATE = 0.065`, `VAR_CONFIDENCE = 0.95`.
- Coverage target: ≥ 80% on the `wealthlens/` package.
- Existing `load_data(tickers, period)` in `streamlit_app.py` returns a DataFrame of Close prices — reuse the pattern; do not re-implement inside the pure package.
- Commit type prefixes: `feat`, `test`, `chore`, `docs`. No attribution trailer (disabled globally).

---

### Task 1: Dependencies & package scaffold

**Files:**
- Modify: `pyproject.toml:7-12` (dependencies)
- Modify: `requirements.txt`
- Create: `wealthlens/__init__.py`
- Create: `wealthlens/config.py`
- Create: `views/__init__.py`
- Create: `tests/__init__.py`

**Interfaces:**
- Produces: `wealthlens.config.TRADING_DAYS: int`, `BENCHMARK: str`, `RISK_FREE_RATE: float`, `VAR_CONFIDENCE: float`, `DEFAULT_PROVIDER: str`.

- [ ] **Step 1: Add runtime + dev dependencies to `pyproject.toml`**

Replace the `dependencies` list and add a dev group:

```toml
dependencies = [
    "altair>=5.5.0",
    "pandas>=2.2.3",
    "numpy>=1.26",
    "streamlit>=1.44.2",
    "yfinance>=0.2.55",
    "requests>=2.31.0",
    "reportlab>=4.2",
    "openai>=1.40",
    "google-generativeai>=0.8",
]

[dependency-groups]
dev = ["pytest>=8.0", "pytest-cov>=5.0"]
```

- [ ] **Step 2: Mirror runtime deps into `requirements.txt`** (for Streamlit Cloud)

```
altair>=5.5.0
pandas>=2.2.3
numpy>=1.26
streamlit>=1.44.2
yfinance>=0.2.55
requests>=2.31.0
reportlab>=4.2
openai>=1.40
google-generativeai>=0.8
```

- [ ] **Step 3: Install**

Run: `uv sync` (Expected: resolves and installs reportlab, openai, google-generativeai, pytest, pytest-cov)

- [ ] **Step 4: Create `wealthlens/config.py`**

```python
"""Central constants for the WealthLens analytics package."""
import os

TRADING_DAYS: int = 252
BENCHMARK: str = "^NSEI"          # Nifty 50
RISK_FREE_RATE: float = 0.065     # ~6.5% India risk-free default
VAR_CONFIDENCE: float = 0.95
DEFAULT_PROVIDER: str = os.getenv("WEALTHLENS_PROVIDER", "openai")
```

- [ ] **Step 5: Create empty `wealthlens/__init__.py`, `views/__init__.py`, `tests/__init__.py`**

Each: a single line `"""WealthLens package."""` (adjust docstring per folder).

- [ ] **Step 6: Verify pytest runs**

Run: `uv run pytest -q` (Expected: "no tests ran" exit 5, confirming pytest is wired)

- [ ] **Step 7: Commit**

```bash
git add pyproject.toml requirements.txt wealthlens/ views/ tests/
git commit -m "chore: scaffold wealthlens package and add analytics dependencies"
```

---

### Task 2: Portfolio holdings model

**Files:**
- Create: `wealthlens/portfolio.py`
- Test: `tests/test_portfolio.py`

**Interfaces:**
- Produces:
  - `class Portfolio` — `@dataclass(frozen=True)` with `tickers: tuple[str, ...]`, `weights: tuple[float, ...]`.
  - `build_portfolio(rows: list[dict], mode: str = "weight", prices: dict[str, float] | None = None) -> Portfolio`
    - `rows` items: `{"ticker": str, "weight": float}` (weight mode) or `{"ticker": str, "shares": float}` (shares mode).
    - Raises `ValueError` if no valid holdings.

- [ ] **Step 1: Write failing tests**

```python
import pytest
from wealthlens.portfolio import build_portfolio, Portfolio

def test_weight_mode_normalizes_to_one():
    p = build_portfolio([{"ticker": "A", "weight": 1},
                         {"ticker": "B", "weight": 1},
                         {"ticker": "C", "weight": 2}])
    assert p.tickers == ("A", "B", "C")
    assert p.weights == (0.25, 0.25, 0.5)
    assert abs(sum(p.weights) - 1.0) < 1e-9

def test_shares_mode_uses_prices():
    p = build_portfolio([{"ticker": "A", "shares": 10},
                         {"ticker": "B", "shares": 10}],
                        mode="shares", prices={"A": 100.0, "B": 300.0})
    assert p.weights == (0.25, 0.75)

def test_drops_empty_and_dedupes():
    p = build_portfolio([{"ticker": "A", "weight": 1},
                         {"ticker": "", "weight": 5},
                         {"ticker": "A", "weight": 3}])
    assert p.tickers == ("A",)
    assert p.weights == (1.0,)

def test_no_valid_holdings_raises():
    with pytest.raises(ValueError):
        build_portfolio([{"ticker": "", "weight": 0}])

def test_negative_weight_rejected():
    with pytest.raises(ValueError):
        build_portfolio([{"ticker": "A", "weight": -1}])

def test_portfolio_is_frozen():
    p = build_portfolio([{"ticker": "A", "weight": 1}])
    with pytest.raises(Exception):
        p.weights = (2.0,)  # frozen dataclass
```

- [ ] **Step 2: Run to verify failure**

Run: `uv run pytest tests/test_portfolio.py -v` (Expected: FAIL, `ModuleNotFoundError: wealthlens.portfolio`)

- [ ] **Step 3: Implement `wealthlens/portfolio.py`**

```python
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
```

- [ ] **Step 4: Run to verify pass**

Run: `uv run pytest tests/test_portfolio.py -v` (Expected: 6 passed)

- [ ] **Step 5: Commit**

```bash
git add wealthlens/portfolio.py tests/test_portfolio.py
git commit -m "feat: add weighted-holdings portfolio model"
```

---

### Task 3: Analytics — returns & core performance metrics

**Files:**
- Create: `wealthlens/analytics.py`
- Test: `tests/test_analytics.py`

**Interfaces:**
- Produces:
  - `daily_returns(prices: pd.DataFrame) -> pd.DataFrame`
  - `portfolio_returns(asset_returns: pd.DataFrame, weights) -> pd.Series`
  - `total_return(r: pd.Series) -> float`
  - `annualized_return(r: pd.Series) -> float`
  - `annualized_volatility(r: pd.Series) -> float`

- [ ] **Step 1: Write failing tests**

```python
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
```

- [ ] **Step 2: Run to verify failure**

Run: `uv run pytest tests/test_analytics.py -v` (Expected: FAIL, module/attribute errors)

- [ ] **Step 3: Implement returns + core metrics in `wealthlens/analytics.py`**

```python
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
```

- [ ] **Step 4: Run to verify pass**

Run: `uv run pytest tests/test_analytics.py -v` (Expected: 5 passed)

- [ ] **Step 5: Commit**

```bash
git add wealthlens/analytics.py tests/test_analytics.py
git commit -m "feat: add returns and core performance metrics"
```

---

### Task 4: Analytics — risk-adjusted ratios & drawdown

**Files:**
- Modify: `wealthlens/analytics.py`
- Test: `tests/test_analytics.py` (append)

**Interfaces:**
- Produces:
  - `sharpe_ratio(r: pd.Series, rf: float) -> float`
  - `sortino_ratio(r: pd.Series, rf: float) -> float`
  - `max_drawdown(r: pd.Series) -> float`  (negative number; -0.5 == 50% drawdown)

- [ ] **Step 1: Append failing tests**

```python
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
```

- [ ] **Step 2: Run to verify failure**

Run: `uv run pytest tests/test_analytics.py -k "sharpe or drawdown or sortino" -v` (Expected: FAIL)

- [ ] **Step 3: Append implementation to `wealthlens/analytics.py`**

```python
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
```

- [ ] **Step 4: Run to verify pass**

Run: `uv run pytest tests/test_analytics.py -v` (Expected: all passed)

- [ ] **Step 5: Commit**

```bash
git add wealthlens/analytics.py tests/test_analytics.py
git commit -m "feat: add Sharpe, Sortino, and max drawdown"
```

---

### Task 5: Analytics — VaR, CVaR & beta

**Files:**
- Modify: `wealthlens/analytics.py`
- Test: `tests/test_analytics.py` (append)

**Interfaces:**
- Produces (VaR/CVaR returned as positive loss magnitudes):
  - `historical_var(r: pd.Series, confidence: float = 0.95) -> float`
  - `parametric_var(r: pd.Series, confidence: float = 0.95) -> float`
  - `cvar(r: pd.Series, confidence: float = 0.95) -> float`
  - `beta(portfolio_r: pd.Series, benchmark_r: pd.Series) -> float`

- [ ] **Step 1: Append failing tests**

```python
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
```

- [ ] **Step 2: Run to verify failure**

Run: `uv run pytest tests/test_analytics.py -k "var or cvar or beta" -v` (Expected: FAIL)

- [ ] **Step 3: Append implementation to `wealthlens/analytics.py`**

> NOTE: No SciPy dependency — the normal z-score for VaR is hardcoded (1.645 for 95%, 2.326 for 99%).

```python
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
```

- [ ] **Step 4: Run to verify pass**

Run: `uv run pytest tests/test_analytics.py -v` (Expected: all passed)

- [ ] **Step 5: Commit**

```bash
git add wealthlens/analytics.py tests/test_analytics.py
git commit -m "feat: add VaR, CVaR, and beta"
```

---

### Task 6: Analytics — correlation, risk contribution & `compute_metrics`

**Files:**
- Modify: `wealthlens/analytics.py`
- Test: `tests/test_analytics.py` (append)

**Interfaces:**
- Produces:
  - `correlation_matrix(asset_returns: pd.DataFrame) -> pd.DataFrame`
  - `risk_contribution(asset_returns: pd.DataFrame, weights) -> pd.Series` (sums to 1.0)
  - `class Metrics` — `@dataclass(frozen=True)` with fields: `total_return, annualized_return, annualized_volatility, sharpe, sortino, max_drawdown, hist_var, param_var, cvar, beta` (all `float`), `correlation: pd.DataFrame`, `risk_contribution: pd.Series`, `portfolio_returns: pd.Series`.
  - `compute_metrics(prices: pd.DataFrame, weights, benchmark_prices: pd.Series | None, rf: float) -> Metrics`

- [ ] **Step 1: Append failing tests**

```python
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
```

- [ ] **Step 2: Run to verify failure**

Run: `uv run pytest tests/test_analytics.py -k "correlation or risk or compute" -v` (Expected: FAIL)

- [ ] **Step 3: Append implementation to `wealthlens/analytics.py`**

```python
from dataclasses import dataclass


def correlation_matrix(asset_returns: pd.DataFrame) -> pd.DataFrame:
    return asset_returns.corr()


def risk_contribution(asset_returns: pd.DataFrame, weights) -> pd.Series:
    w = np.asarray(weights, dtype=float)
    cov = asset_returns.cov().to_numpy()
    port_var = float(w @ cov @ w)
    if port_var == 0:
        return pd.Series(w, index=asset_returns.columns)
    marginal = cov @ w
    contrib = w * marginal             # component contributions to variance
    contrib = contrib / contrib.sum()  # normalize to 1.0
    return pd.Series(contrib, index=asset_returns.columns)


@dataclass(frozen=True)
class Metrics:
    total_return: float
    annualized_return: float
    annualized_volatility: float
    sharpe: float
    sortino: float
    max_drawdown: float
    hist_var: float
    param_var: float
    cvar: float
    beta: float
    correlation: pd.DataFrame
    risk_contribution: pd.Series
    portfolio_returns: pd.Series


def compute_metrics(prices, weights, benchmark_prices, rf) -> Metrics:
    ar = daily_returns(prices)
    pr = portfolio_returns(ar, weights)
    if benchmark_prices is not None:
        br = benchmark_prices.pct_change().dropna()
        b = beta(pr, br)
    else:
        b = float("nan")
    return Metrics(
        total_return=total_return(pr),
        annualized_return=annualized_return(pr),
        annualized_volatility=annualized_volatility(pr),
        sharpe=sharpe_ratio(pr, rf),
        sortino=sortino_ratio(pr, rf),
        max_drawdown=max_drawdown(pr),
        hist_var=historical_var(pr),
        param_var=parametric_var(pr),
        cvar=cvar(pr),
        beta=b,
        correlation=correlation_matrix(ar),
        risk_contribution=risk_contribution(ar, weights),
        portfolio_returns=pr,
    )
```

- [ ] **Step 4: Run to verify pass + coverage snapshot**

Run: `uv run pytest tests/ --cov=wealthlens --cov-report=term-missing -v`
Expected: all passed; `analytics.py` + `portfolio.py` well above 80%.

- [ ] **Step 5: Commit**

```bash
git add wealthlens/analytics.py tests/test_analytics.py
git commit -m "feat: add correlation, risk contribution, and metrics bundle"
```

---

### Task 7: AI commentary (grounded, with fallback)

**Files:**
- Create: `wealthlens/ai_commentary.py`
- Test: `tests/test_ai_commentary.py`

**Interfaces:**
- Consumes: `Metrics` (Task 6), `Portfolio` (Task 2).
- Produces:
  - `build_prompt(metrics, portfolio) -> str`
  - `fallback_summary(metrics, portfolio) -> str`
  - `generate(metrics, portfolio, provider=None, api_key=None) -> str`  (uses fallback when no key or on error)

- [ ] **Step 1: Write failing tests**

```python
import pandas as pd
from wealthlens.portfolio import build_portfolio
from wealthlens.analytics import compute_metrics
from wealthlens import ai_commentary as ai

def _metrics():
    prices = pd.DataFrame({"A": [100, 101, 102, 101, 103],
                           "B": [50, 49, 51, 52, 50]})
    return compute_metrics(prices, [0.6, 0.4], None, rf=0.0)

def test_fallback_mentions_sharpe_and_risk():
    m = _metrics()
    p = build_portfolio([{"ticker": "A", "weight": 0.6}, {"ticker": "B", "weight": 0.4}])
    text = ai.fallback_summary(m, p)
    assert "Sharpe" in text
    assert "%" in text

def test_generate_uses_fallback_without_key():
    m = _metrics()
    p = build_portfolio([{"ticker": "A", "weight": 1}])
    text = ai.generate(m, p, provider="openai", api_key=None)
    assert isinstance(text, str) and len(text) > 0

def test_build_prompt_includes_numbers():
    m = _metrics()
    p = build_portfolio([{"ticker": "A", "weight": 1}])
    prompt = ai.build_prompt(m, p)
    assert "Sharpe" in prompt and "drawdown" in prompt.lower()
```

- [ ] **Step 2: Run to verify failure**

Run: `uv run pytest tests/test_ai_commentary.py -v` (Expected: FAIL)

- [ ] **Step 3: Implement `wealthlens/ai_commentary.py`**

```python
"""Grounded AI commentary layer. Explains computed metrics; never invents numbers."""
from __future__ import annotations
from wealthlens.config import DEFAULT_PROVIDER

_SYSTEM = (
    "You are a buy-side portfolio analyst. Explain ONLY the metrics provided. "
    "Do not invent any numbers. Keep it to 4-6 sentences: comment on risk-adjusted "
    "performance (Sharpe/Sortino), drawdown/VaR risk, and concentration/diversification."
)


def build_prompt(metrics, portfolio) -> str:
    top = metrics.risk_contribution.sort_values(ascending=False)
    top_line = ", ".join(f"{t}: {w*100:.0f}%" for t, w in top.items())
    holdings = ", ".join(f"{t} {w*100:.1f}%"
                         for t, w in zip(portfolio.tickers, portfolio.weights))
    return (
        f"Holdings & weights: {holdings}\n"
        f"Total return: {metrics.total_return*100:.2f}%\n"
        f"Annualized return: {metrics.annualized_return*100:.2f}%\n"
        f"Annualized volatility: {metrics.annualized_volatility*100:.2f}%\n"
        f"Sharpe: {metrics.sharpe:.2f} | Sortino: {metrics.sortino:.2f}\n"
        f"Max drawdown: {metrics.max_drawdown*100:.2f}%\n"
        f"95% VaR (hist): {metrics.hist_var*100:.2f}% | CVaR: {metrics.cvar*100:.2f}%\n"
        f"Beta vs benchmark: {metrics.beta:.2f}\n"
        f"Risk contribution: {top_line}\n"
    )


def fallback_summary(metrics, portfolio) -> str:
    top_t = metrics.risk_contribution.idxmax()
    top_w = metrics.risk_contribution.max() * 100
    verdict = "strong" if metrics.sharpe > 1 else "modest" if metrics.sharpe > 0 else "weak"
    return (
        f"The portfolio returned {metrics.total_return*100:.1f}% over the period with "
        f"annualized volatility of {metrics.annualized_volatility*100:.1f}%. "
        f"Its risk-adjusted performance is {verdict} (Sharpe {metrics.sharpe:.2f}, "
        f"Sortino {metrics.sortino:.2f}). Tail risk: 95% VaR of {metrics.hist_var*100:.1f}% "
        f"and a worst drawdown of {metrics.max_drawdown*100:.1f}%. "
        f"Risk is most concentrated in {top_t} ({top_w:.0f}% of total risk); "
        f"consider whether that concentration matches your risk tolerance."
    )


def generate(metrics, portfolio, provider=None, api_key=None) -> str:
    provider = provider or DEFAULT_PROVIDER
    if not api_key:
        return fallback_summary(metrics, portfolio)
    prompt = build_prompt(metrics, portfolio)
    try:
        if provider == "openai":
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": _SYSTEM},
                          {"role": "user", "content": prompt}],
                temperature=0.3,
            )
            return resp.choices[0].message.content.strip()
        elif provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            resp = model.generate_content(_SYSTEM + "\n\n" + prompt)
            return resp.text.strip()
    except Exception:
        return fallback_summary(metrics, portfolio)
    return fallback_summary(metrics, portfolio)
```

- [ ] **Step 4: Run to verify pass**

Run: `uv run pytest tests/test_ai_commentary.py -v` (Expected: 3 passed — no network hit, key is None)

- [ ] **Step 5: Commit**

```bash
git add wealthlens/ai_commentary.py tests/test_ai_commentary.py
git commit -m "feat: add grounded AI commentary with deterministic fallback"
```

---

### Task 8: PDF report generator

**Files:**
- Create: `wealthlens/report.py`
- Test: `tests/test_report.py`

**Interfaces:**
- Consumes: `Portfolio`, `Metrics`, narrative `str`.
- Produces: `build_pdf(portfolio, metrics, narrative, chart_pngs: dict[str, bytes] | None = None) -> bytes`

- [ ] **Step 1: Write failing test**

```python
import pandas as pd
from wealthlens.portfolio import build_portfolio
from wealthlens.analytics import compute_metrics
from wealthlens.report import build_pdf

def test_build_pdf_returns_pdf_bytes():
    prices = pd.DataFrame({"A": [100, 101, 102, 101, 103],
                           "B": [50, 49, 51, 52, 50]})
    m = compute_metrics(prices, [0.6, 0.4], None, rf=0.0)
    p = build_portfolio([{"ticker": "A", "weight": 0.6}, {"ticker": "B", "weight": 0.4}])
    pdf = build_pdf(p, m, "Test narrative.")
    assert isinstance(pdf, bytes)
    assert pdf[:4] == b"%PDF"  # PDF magic number
    assert len(pdf) > 500
```

- [ ] **Step 2: Run to verify failure**

Run: `uv run pytest tests/test_report.py -v` (Expected: FAIL)

- [ ] **Step 3: Implement `wealthlens/report.py`**

```python
"""One-click PDF portfolio review. Pure-Python via reportlab."""
from __future__ import annotations
import io
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Image)
from reportlab.lib.styles import getSampleStyleSheet


def _metrics_rows(m):
    return [
        ["Total return", f"{m.total_return*100:.2f}%"],
        ["Annualized return", f"{m.annualized_return*100:.2f}%"],
        ["Annualized volatility", f"{m.annualized_volatility*100:.2f}%"],
        ["Sharpe ratio", f"{m.sharpe:.2f}"],
        ["Sortino ratio", f"{m.sortino:.2f}"],
        ["Max drawdown", f"{m.max_drawdown*100:.2f}%"],
        ["95% VaR (historical)", f"{m.hist_var*100:.2f}%"],
        ["95% CVaR", f"{m.cvar*100:.2f}%"],
        ["Beta vs benchmark", f"{m.beta:.2f}"],
    ]


def build_pdf(portfolio, metrics, narrative, chart_pngs=None) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, title="WealthLens Portfolio Review")
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("WealthLens — Portfolio Review", styles["Title"]))
    story.append(Paragraph(date.today().isoformat(), styles["Normal"]))
    story.append(Spacer(1, 0.6 * cm))

    story.append(Paragraph("Holdings", styles["Heading2"]))
    holdings = [["Ticker", "Weight"]] + [
        [t, f"{w*100:.1f}%"] for t, w in zip(portfolio.tickers, portfolio.weights)]
    h_table = Table(holdings, hAlign="LEFT")
    h_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0E1626")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(h_table)
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("Risk & performance metrics", styles["Heading2"]))
    m_table = Table([["Metric", "Value"]] + _metrics_rows(metrics), hAlign="LEFT")
    m_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0E1626")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(m_table)
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("AI commentary", styles["Heading2"]))
    story.append(Paragraph(narrative, styles["Normal"]))

    for _, png in (chart_pngs or {}).items():
        story.append(Spacer(1, 0.4 * cm))
        story.append(Image(io.BytesIO(png), width=15 * cm, height=8 * cm))

    doc.build(story)
    return buf.getvalue()
```

- [ ] **Step 4: Run to verify pass**

Run: `uv run pytest tests/test_report.py -v` (Expected: 1 passed)

- [ ] **Step 5: Commit**

```bash
git add wealthlens/report.py tests/test_report.py
git commit -m "feat: add PDF portfolio-review generator"
```

---

### Task 9: Streamlit portfolio view

**Files:**
- Create: `views/portfolio_view.py`

**Interfaces:**
- Consumes: `load_data` (passed in from `streamlit_app.py`), all `wealthlens` modules.
- Produces: `render(load_data)` — draws the entire WealthLens tab.

> This task is UI glue; it is verified by a manual smoke run, not unit tests (Streamlit rendering is not unit-testable here). Keep all math in `wealthlens/` — this file only wires widgets to functions.

- [ ] **Step 1: Implement `views/portfolio_view.py`**

```python
"""Streamlit rendering for the WealthLens portfolio-analytics tab."""
import os
import altair as alt
import pandas as pd
import streamlit as st

from wealthlens import ai_commentary, config
from wealthlens.analytics import compute_metrics
from wealthlens.portfolio import build_portfolio
from wealthlens.report import build_pdf


def _get_api_key(provider: str):
    key_name = "OPENAI_API_KEY" if provider == "openai" else "GEMINI_API_KEY"
    try:
        return st.secrets.get(key_name) or os.getenv(key_name)
    except Exception:
        return os.getenv(key_name)


def render(load_data):
    st.header("WealthLens · Portfolio Analytics")
    st.caption("Enter weighted holdings to compute institutional-style risk analytics.")

    default = pd.DataFrame({"ticker": ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"],
                            "weight": [40.0, 35.0, 25.0]})
    edited = st.data_editor(default, num_rows="dynamic", key="wl_holdings",
                            use_container_width=True)

    col1, col2, col3 = st.columns(3)
    period = col1.selectbox("Period", ["6mo", "1y", "2y", "5y"], index=1)
    benchmark = col2.text_input("Benchmark", config.BENCHMARK)
    rf = col3.number_input("Risk-free rate", value=config.RISK_FREE_RATE,
                           step=0.005, format="%.3f")

    rows = edited.to_dict("records")
    try:
        build_portfolio(rows, mode="weight")  # validate before fetching
    except ValueError as e:
        st.info(str(e))
        return

    tickers = [str(r.get("ticker", "")).strip().upper()
               for r in rows if str(r.get("ticker", "")).strip()]
    try:
        prices = load_data(list(dict.fromkeys(tickers)), period)
    except Exception as e:
        st.error(f"Could not load price data: {e}")
        return
    prices = prices.dropna(axis=1, how="all")
    if prices.empty:
        st.warning("No price data for the selected holdings.")
        return

    bench_prices = None
    try:
        bench_df = load_data([benchmark], period)
        bench_prices = bench_df[benchmark] if benchmark in bench_df else bench_df.iloc[:, 0]
    except Exception:
        st.caption("Benchmark unavailable — beta will show as N/A.")

    # Rebuild portfolio using only tickers that returned data, preserving weights.
    valid = build_portfolio([r for r in rows
                             if str(r.get("ticker", "")).strip().upper() in prices.columns])
    prices = prices[list(valid.tickers)]
    m = compute_metrics(prices, valid.weights, bench_prices, rf)

    # --- metric cards ---
    c = st.columns(4)
    c[0].metric("Total return", f"{m.total_return*100:.2f}%")
    c[1].metric("Ann. volatility", f"{m.annualized_volatility*100:.2f}%")
    c[2].metric("Sharpe", f"{m.sharpe:.2f}")
    c[3].metric("Max drawdown", f"{m.max_drawdown*100:.2f}%")
    c2 = st.columns(4)
    c2[0].metric("Sortino", f"{m.sortino:.2f}")
    c2[1].metric("95% VaR", f"{m.hist_var*100:.2f}%")
    c2[2].metric("95% CVaR", f"{m.cvar*100:.2f}%")
    c2[3].metric("Beta", "N/A" if pd.isna(m.beta) else f"{m.beta:.2f}")

    # --- growth curve ---
    growth = (1 + m.portfolio_returns).cumprod().reset_index()
    growth.columns = ["Date", "Growth"]
    st.altair_chart(alt.Chart(growth).mark_line().encode(
        x="Date:T", y="Growth:Q").properties(title="Portfolio growth (×)"),
        use_container_width=True)

    # --- drawdown underwater ---
    cum = (1 + m.portfolio_returns).cumprod()
    dd = (cum / cum.cummax() - 1).reset_index()
    dd.columns = ["Date", "Drawdown"]
    st.altair_chart(alt.Chart(dd).mark_area(color="#c0392b").encode(
        x="Date:T", y="Drawdown:Q").properties(title="Drawdown (underwater)"),
        use_container_width=True)

    # --- correlation heatmap ---
    corr = m.correlation.reset_index().melt(id_vars="index")
    corr.columns = ["Asset A", "Asset B", "Correlation"]
    st.altair_chart(alt.Chart(corr).mark_rect().encode(
        x="Asset A:O", y="Asset B:O",
        color=alt.Color("Correlation:Q",
                        scale=alt.Scale(scheme="redblue", domain=[-1, 1]))
        ).properties(title="Correlation matrix"), use_container_width=True)

    # --- risk contribution ---
    rc = m.risk_contribution.reset_index()
    rc.columns = ["Asset", "RiskShare"]
    st.altair_chart(alt.Chart(rc).mark_bar().encode(
        x=alt.X("RiskShare:Q", axis=alt.Axis(format="%")), y="Asset:O"
        ).properties(title="Risk contribution"), use_container_width=True)

    # --- AI commentary ---
    st.subheader("AI commentary")
    provider = config.DEFAULT_PROVIDER
    narrative = ai_commentary.generate(m, valid, provider=provider,
                                       api_key=_get_api_key(provider))
    st.write(narrative)

    # --- PDF ---
    pdf = build_pdf(valid, m, narrative)
    st.download_button("⬇️ Download Portfolio Review (PDF)", data=pdf,
                       file_name="wealthlens_review.pdf", mime="application/pdf")
```

- [ ] **Step 2: Commit**

```bash
git add views/portfolio_view.py
git commit -m "feat: add WealthLens Streamlit portfolio view"
```

---

### Task 10: Nav router integration

**Files:**
- Modify: `streamlit_app.py` (immediately after `st.set_page_config(...)`, around line 14)

**Interfaces:**
- Consumes: `views.portfolio_view.render`.

> The existing app defines its own `load_data` further down the file (after `st.stop()` points in the existing flow), so the WealthLens branch supplies its own cached loader. The nav must render the view only when selected, then `st.stop()` so the existing dashboard body does not also execute.

- [ ] **Step 1: Insert nav router right after `st.set_page_config(...)`**

Add at line ~15 (before the custom-CSS `st.markdown`):

```python
# --- Top-level navigation -------------------------------------------------
_view = st.sidebar.radio(
    "View", ["Market Explorer", "WealthLens · Portfolio Analytics"], key="app_view")
if _view.startswith("WealthLens"):
    import yfinance as _yf

    @st.cache_resource(show_spinner=False, ttl="6h")
    def _wl_load_data(tickers, period):
        data = _yf.Tickers(list(tickers)).history(period=period)
        if data is None:
            raise RuntimeError("YFinance returned no data.")
        close = data["Close"]
        return close.to_frame() if getattr(close, "ndim", 2) == 1 else close

    from views.portfolio_view import render as _render_wl
    _render_wl(_wl_load_data)
    st.stop()
# --- End navigation -------------------------------------------------------
```

- [ ] **Step 2: Smoke-test the app**

Run: `uv run streamlit run streamlit_app.py`
Manual check:
- Sidebar shows the "View" selector.
- "Market Explorer" → existing dashboard renders unchanged.
- "WealthLens" → holdings editor, 8 metric cards, 4 charts, AI commentary (fallback text when no key), and a working PDF download.

- [ ] **Step 3: Commit**

```bash
git add streamlit_app.py
git commit -m "feat: add top-level nav routing to WealthLens view"
```

---

### Task 11: Coverage gate & docs finalization

**Files:**
- Modify: `README.md` (flip WealthLens from "In Development" to shipped once verified)

- [ ] **Step 1: Run full suite with coverage**

Run: `uv run pytest tests/ --cov=wealthlens --cov-report=term-missing`
Expected: all tests pass; `wealthlens/` total coverage ≥ 80%. If `analytics.py`/`portfolio.py` are below, add a targeted test for the uncovered branch.

- [ ] **Step 2: Update README status**

In the "🧭 Roadmap: WealthLens" section, change the status blockquote from
`> **Status: In active development.** ... but not yet shipped.`
to
`> **Status: Shipped.** Available via the sidebar "View" selector.`

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: mark WealthLens as shipped"
```

---

## Self-Review

**Spec coverage:** Every spec section maps to a task — portfolio model (T2), full analytics catalog (T3–T6), AI commentary + fallback (T7), PDF report (T8), portfolio view/UX + error handling (T9), nav integration keeping Market Explorer intact (T10), testing/coverage + README (T1, T11). Deferred items (optimization/Monte Carlo/backtesting) intentionally excluded.

**Placeholder scan:** No TBD/TODO/"add error handling" placeholders. Every code step shows complete code.

**Type consistency:** `Metrics` field names used in T7/T8/T9 (`total_return`, `annualized_return`, `annualized_volatility`, `sharpe`, `sortino`, `max_drawdown`, `hist_var`, `param_var`, `cvar`, `beta`, `risk_contribution`, `portfolio_returns`, `correlation`) match their definition in T6. Signatures for `build_portfolio`, `compute_metrics`, `generate`, `build_pdf`, and `render` are consistent across producing and consuming tasks.
