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
