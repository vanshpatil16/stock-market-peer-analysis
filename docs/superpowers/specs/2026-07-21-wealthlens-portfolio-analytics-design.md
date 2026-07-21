# WealthLens — Portfolio Risk & Insight Cockpit

**Design spec** · 2026-07-21 · Author: Vansh Patil
**Context:** New feature set for the existing Streamlit market-analysis dashboard, built to showcase skills for the **UBS 2027 Graduate Talent Program — Group Technology Office (GTO)** internship.

---

## 1. Purpose

Extend the existing multi-asset dashboard with a **portfolio-grade quantitative analytics engine**, a **grounded AI commentary layer**, and a **one-click management report**. The goal is a demo and codebase that maps directly onto UBS's stated priorities and the internship JD.

### Why this, for this role

| UBS / JD signal | How this project answers it |
|---|---|
| "Experimental and **responsible use of AI** to improve outcomes" | AI narrates *deterministically-computed* numbers; it never invents figures. Deterministic math + explanatory AI = responsible AI. |
| "Contribute to **automation and process improvement**" | One-click PDF report automates what an analyst would assemble by hand. |
| "Gather, analyze and **report progress data to senior management**" | The PDF "Portfolio Review" is exactly a management-ready report. |
| UBS is the world's largest **wealth manager** | Weighted holdings, risk contribution, VaR/CVaR, beta — real wealth-management analytics. |
| Proficiency in **Python**; clean engineering (their OA tests OOP/DSA) | Pure, framework-agnostic modules with unit tests and 80%+ coverage, extracted cleanly from a monolith. |

## 2. Scope

**In scope (1–2 week build):**
- Weighted-holdings portfolio model (weights, or shares → weights).
- Quant engine: return, volatility, Sharpe, Sortino, max drawdown, VaR & CVaR, beta, correlation matrix, per-asset risk contribution.
- Charts: growth curve, drawdown (underwater) chart, correlation heatmap, risk-contribution bar.
- Provider-agnostic AI commentary (OpenAI or Gemini) with a deterministic no-key fallback.
- One-click PDF portfolio review.
- Unit tests for the pure analytics/portfolio modules, 80%+ coverage on the `wealthlens/` package.

**Explicitly deferred (Future Work — mention in interview, do not build now):**
- Efficient-frontier / mean-variance optimization.
- Monte Carlo simulation.
- Historical strategy backtesting.
- Full refactor of the existing 1789-line `streamlit_app.py`.

## 3. Architecture

Keep the existing dashboard fully intact. Add a top-level navigation (`st.sidebar` radio) selecting between:
- **Market Explorer** — the current app, unchanged.
- **WealthLens · Portfolio Analytics** — the new view.

All new logic lives in a pure, importable package. `analytics.py` and `portfolio.py` import **no Streamlit** — pandas/numpy in, numbers out — which is what makes them unit-testable.

```
stock_market_analysis/
├── streamlit_app.py          # existing UI + thin nav router (minimal edits)
├── wealthlens/               # NEW — pure, framework-agnostic package
│   ├── __init__.py
│   ├── portfolio.py          # Holdings model: normalize weights / shares→weights
│   ├── analytics.py          # Quant engine (pure functions on returns DataFrame)
│   ├── ai_commentary.py      # Provider-agnostic LLM wrapper + no-key fallback
│   ├── report.py             # PDF "portfolio review" generator
│   └── config.py             # Constants: benchmark, risk-free rate, trading days, provider
├── views/
│   └── portfolio_view.py     # Streamlit rendering for the WealthLens tab
├── tests/
│   ├── test_portfolio.py
│   └── test_analytics.py     # deterministic math tests → easy 80%+ coverage
└── docs/superpowers/specs/   # this spec
```

### Data flow

```
User holdings (st.data_editor: ticker, weight% or shares)
        │
        ▼
portfolio.build_portfolio()  ──► normalized weights (sum = 1.0)
        │
        ▼
load_data(tickers, period)   ──► Close prices  [REUSE existing cached fn]
        │
        ▼
analytics.compute_metrics(prices, weights, benchmark_prices, rf)
        │      └─► return, vol, Sharpe, Sortino, drawdown, VaR/CVaR, beta, corr, risk-contrib
        ▼
portfolio_view renders  ──►  metric cards + Altair charts
        │
        ├──► ai_commentary.generate(metrics, holdings)  ──► analyst narrative
        └──► report.build_pdf(metrics, narrative, charts) ──► downloadable review
```

## 4. Module specifications

### 4.1 `portfolio.py`
- `build_portfolio(rows) -> Portfolio`: takes editable-table rows `{ticker, weight}` or `{ticker, shares}`.
  - Weight mode: renormalize so weights sum to 1.0.
  - Shares mode: `weightᵢ = sharesᵢ · priceᵢ / Σ(shares · price)`.
  - Validation: drop empty rows, reject negative weights/shares, dedupe tickers, require ≥1 valid holding.
- Returns an immutable structure (`@dataclass(frozen=True)`) holding tickers and a normalized weight vector. No mutation of inputs.

### 4.2 `analytics.py` (pure functions; `TRADING_DAYS = 252`)
All operate on a daily-returns DataFrame and a weight vector.

| Function | Formula (essence) |
|---|---|
| `portfolio_returns(prices, weights)` | weighted sum of per-asset daily returns |
| `total_return(r)` / `annualized_return(r)` | `(1+r).prod()−1` / `mean(r)·252` |
| `annualized_volatility(r)` | `std(r)·√252` |
| `sharpe(r, rf)` | `(ann_ret − rf) / ann_vol` |
| `sortino(r, rf)` | `(ann_ret − rf) / (downside_std·√252)` |
| `max_drawdown(r)` | `min(cum/cummax − 1)` |
| `historical_var(r, 0.95)` / `parametric_var(r, 0.95)` | 5th percentile / `μ − 1.645σ` |
| `cvar(r, 0.95)` | mean of losses beyond VaR |
| `beta(rp, rb)` | `cov(rp, rb)/var(rb)` |
| `correlation_matrix(returns)` | `returns.corr()` |
| `risk_contribution(returns, weights)` | `wᵢ·(Σw)ᵢ / σₚ`, normalized to 100% |

`compute_metrics(...)` orchestrates these into one immutable `Metrics` result object consumed by the view, AI, and report layers.

### 4.3 `ai_commentary.py`
- `generate(metrics, holdings) -> str`.
- `PROVIDER` config switch: `"openai"` | `"gemini"`. API key read from `st.secrets` or environment variable — **never hardcoded**.
- Prompt passes the *computed numbers* and asks the model to explain concentration risk, diversification, and risk-adjusted performance in plain English. The model is instructed not to introduce new figures.
- **Fallback:** on missing key or API error, return a deterministic rule-based summary (template driven by the metrics). The app never breaks in a demo.

### 4.4 `report.py`
- `build_pdf(metrics, narrative, chart_images) -> bytes` using **reportlab** (pure-Python, deploys cleanly on Streamlit Cloud).
- Sections: title/date header, holdings table, metrics table, AI narrative, embedded charts.
- Surfaced as a `st.download_button` ("Download Portfolio Review (PDF)").

### 4.5 `config.py`
Centralized constants: `BENCHMARK = "^NSEI"` (Nifty 50), `RISK_FREE_RATE` default, `TRADING_DAYS = 252`, `VAR_CONFIDENCE = 0.95`, `PROVIDER`. No magic numbers elsewhere.

### 4.6 `views/portfolio_view.py`
Streamlit rendering only. Holdings `data_editor` (Ticker | Weight% with optional Shares mode), benchmark selector (default Nifty 50), risk-free-rate input, metric cards, the four Altair charts, AI-commentary panel, and the PDF download button.

## 5. Portfolio input UX
- Editable table (`st.data_editor`) with add/remove rows.
- Weight mode renormalizes to 100% with a visible note; Shares mode converts via latest price.
- Invalid tickers flagged inline; empty state shows guidance; fail-fast with clear messages.

## 6. Error handling
- All external I/O (yfinance, LLM API) wrapped with explicit, user-friendly messages; reuse the existing rate-limit handling pattern.
- Boundary validation in `portfolio.build_portfolio` and the data_editor.
- No silent failures: every caught error either recovers with a stated fallback or surfaces a message.

## 7. Testing
- `test_analytics.py`: known synthetic series with hand-computed expected values (constant-return series → known Sharpe; anti-correlated pair → corr ≈ −1; monotonic decline → known max drawdown). Deterministic, no network.
- `test_portfolio.py`: weight normalization, shares→weights, invalid/empty/duplicate input.
- `ai_commentary` / `report`: test the fallback path and prompt/PDF assembly with the network call mocked.
- Tooling: `pytest` + `pytest-cov`, coverage gate **≥ 80%** on `wealthlens/`.

## 8. Success criteria
- App runs end-to-end with **no API key** (fallback commentary) and with a key (live AI).
- A user can enter weighted holdings and get all metrics, four charts, AI commentary, and a downloadable PDF.
- `pytest` passes with ≥ 80% coverage on `wealthlens/`.
- Existing Market Explorer view is unchanged and still works.
- README updated with a "WealthLens" section and a UBS-alignment note.

## 9. Risks & mitigations
- **yfinance rate limits / benchmark data gaps** → reuse existing caching; handle missing benchmark by disabling beta with a clear note.
- **LLM latency/cost** → cache commentary per metrics hash; fallback path always available.
- **Timeline overrun** → optimization/Monte Carlo/backtesting are deferred, not in scope.
- **reportlab chart embedding** → render Altair charts to PNG via a vendored static export or matplotlib fallback for the PDF only.

## 10. Future work (interview "what's next" slide)
Efficient-frontier optimization, Monte Carlo simulation, strategy backtesting, and a full modularization of the existing dashboard.
