"""Streamlit rendering for the WealthLens portfolio-analytics tab."""
import os
import altair as alt
import pandas as pd
import streamlit as st

from wealthlens import ai_commentary, config, tickers as wl_tickers
from wealthlens.analytics import compute_metrics, correlation_long
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

    seed = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"]
    default = pd.DataFrame({"ticker": [wl_tickers.label_for(s) for s in seed],
                            "weight": [40.0, 35.0, 25.0]})
    edited = st.data_editor(
        default, num_rows="dynamic", key="wl_holdings", use_container_width=True,
        column_config={
            "ticker": st.column_config.SelectboxColumn(
                "Holding", width="large", required=True,
                options=wl_tickers.labels(),
                help="Search by company name or symbol — no need to memorise Yahoo tickers."),
            "weight": st.column_config.NumberColumn(
                "Weight", min_value=0.0, step=1.0, format="%.1f",
                help="Relative weights — any positive numbers work and are "
                     "auto-normalized; percentages summing to 100 recommended."),
        })

    col1, col2, col3 = st.columns(3)
    period = col1.selectbox("Period", ["6mo", "1y", "2y", "5y"], index=1)
    benchmark = col2.text_input("Benchmark", config.BENCHMARK)
    rf = col3.number_input("Risk-free rate", value=config.RISK_FREE_RATE,
                           step=0.005, format="%.3f")

    rows = edited.to_dict("records")
    # SelectboxColumn stores the "SYMBOL — Name" label; map back to raw Yahoo
    # symbols before validation and price fetch.
    for r in rows:
        r["ticker"] = wl_tickers.symbol_from_label(r.get("ticker"))
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
    corr = correlation_long(m.correlation)
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
