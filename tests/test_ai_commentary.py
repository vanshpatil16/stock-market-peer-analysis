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
