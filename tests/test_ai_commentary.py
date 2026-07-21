import types
from unittest import mock

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


def test_generate_openai_path_uses_client(monkeypatch):
    import openai
    m = _metrics()
    p = build_portfolio([{"ticker": "A", "weight": 1}])
    fake_resp = types.SimpleNamespace(
        choices=[types.SimpleNamespace(
            message=types.SimpleNamespace(content="  OpenAI narrative.  "))])
    fake_client = mock.MagicMock()
    fake_client.chat.completions.create.return_value = fake_resp
    monkeypatch.setattr(openai, "OpenAI", lambda api_key: fake_client)
    out = ai.generate(m, p, provider="openai", api_key="test-key")
    assert out == "OpenAI narrative."
    fake_client.chat.completions.create.assert_called_once()


def test_generate_gemini_path_uses_model(monkeypatch):
    import google.generativeai as genai
    m = _metrics()
    p = build_portfolio([{"ticker": "A", "weight": 1}])
    fake_model = mock.MagicMock()
    fake_model.generate_content.return_value = types.SimpleNamespace(
        text="  Gemini narrative.  ")
    monkeypatch.setattr(genai, "configure", lambda api_key: None)
    monkeypatch.setattr(genai, "GenerativeModel", lambda name: fake_model)
    out = ai.generate(m, p, provider="gemini", api_key="test-key")
    assert out == "Gemini narrative."
    fake_model.generate_content.assert_called_once()


def test_generate_falls_back_on_provider_error(monkeypatch):
    import openai
    m = _metrics()
    p = build_portfolio([{"ticker": "A", "weight": 1}])
    def boom(api_key):
        raise RuntimeError("network down")
    monkeypatch.setattr(openai, "OpenAI", boom)
    out = ai.generate(m, p, provider="openai", api_key="test-key")
    assert out == ai.fallback_summary(m, p)


def test_generate_unknown_provider_falls_back():
    m = _metrics()
    p = build_portfolio([{"ticker": "A", "weight": 1}])
    out = ai.generate(m, p, provider="anthropic", api_key="test-key")
    assert out == ai.fallback_summary(m, p)
