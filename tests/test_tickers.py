from wealthlens import tickers as t


def test_label_for_known_symbol():
    assert t.label_for("RELIANCE.NS") == "RELIANCE.NS — Reliance Industries"


def test_label_for_unknown_symbol_returns_symbol():
    assert t.label_for("FOO.NS") == "FOO.NS"


def test_labels_nonempty_and_unique():
    labels = t.labels()
    assert len(labels) > 10
    assert len(labels) == len(set(labels))


def test_symbol_from_label_roundtrip():
    for sym in t.TICKER_NAMES:
        assert t.symbol_from_label(t.label_for(sym)) == sym.upper()


def test_symbol_from_label_accepts_plain_symbol():
    assert t.symbol_from_label("INFY.NS") == "INFY.NS"


def test_symbol_from_label_handles_none_and_blank():
    assert t.symbol_from_label(None) == ""
    assert t.symbol_from_label("") == ""
    assert t.symbol_from_label("   ") == ""
    assert t.symbol_from_label(float("nan")) == ""
