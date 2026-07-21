"""Central constants for the WealthLens analytics package."""
import os

TRADING_DAYS: int = 252
BENCHMARK: str = "^NSEI"          # Nifty 50
RISK_FREE_RATE: float = 0.065     # ~6.5% India risk-free default
VAR_CONFIDENCE: float = 0.95
DEFAULT_PROVIDER: str = os.getenv("WEALTHLENS_PROVIDER", "openai")
