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
