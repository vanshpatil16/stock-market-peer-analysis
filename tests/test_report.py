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
