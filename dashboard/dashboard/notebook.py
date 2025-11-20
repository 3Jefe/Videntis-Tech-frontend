"""
Videntis Dashboard Notebook (script version)

This script is a lightweight, notebook-style dashboard that:
- Loads market snapshot data from /data/market_snapshot.csv (if present)
- Or generates a small synthetic dataset if the file is missing
- Optionally runs the Videntis TrendPipeline + RiskEngine (if available)
- Produces simple visualisations saved into the /dashboard folder

Run from the repo root with:
    python dashboard/notebook.py
"""

from pathlib import Path
from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt

# Optional imports – script still works if these are missing
try:
    from engine.pipeline import TrendPipeline
    from profiles.risk_engine import RiskEngine
    from ai.model import TrendModel
except ImportError:
    TrendPipeline = None  # type: ignore
    RiskEngine = None     # type: ignore
    TrendModel = None     # type: ignore


# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = REPO_ROOT / "data" / "market_snapshot.csv"
OUTPUT_DIR = REPO_ROOT / "dashboard"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------------------------
# Data loading
# -------------------------------------------------------------------
def load_market_data() -> pd.DataFrame:
    """
    Loads market data from CSV if it exists.
    If not, creates a small synthetic dataset.
    """
    if DATA_PATH.exists():
        print(f"[info] Loading data from {DATA_PATH}")
        df = pd.read_csv(DATA_PATH)
        return df

    print("[info] No market_snapshot.csv found, generating synthetic data instead.")
    dates = pd.date_range("2025-01-01", periods=7, freq="D")
    data = {
        "date": list(dates) * 4,
        "sector": (
            ["AI & Tech"] * len(dates)
            + ["Energy Transition"] * len(dates)
            + ["Consumer Staples"] * len(dates)
            + ["Digital Assets"] * len(dates)
        ),
        "price_index": [
            100, 102, 101, 104, 108, 110, 115,      # AI & Tech
            95, 96, 97, 98, 99, 101, 102,           # Energy Transition
            98, 98.5, 99, 99.5, 100, 100.5, 101,    # Consumer Staples
            80, 78, 79, 81, 83, 85, 88,             # Digital Assets
        ],
        "sentiment": [
            0.7, 0.72, 0.68, 0.75, 0.8, 0.82, 0.85,     # AI & Tech
            0.55, 0.56, 0.57, 0.58, 0.6, 0.61, 0.62,    # Energy Transition
            0.5, 0.51, 0.51, 0.52, 0.53, 0.54, 0.55,    # Consumer Staples
            0.65, 0.6, 0.62, 0.64, 0.66, 0.68, 0.7,     # Digital Assets
        ],
    }
    df = pd.DataFrame(data)
    return df


# -------------------------------------------------------------------
# Optional: run TrendPipeline + RiskEngine if available
# -------------------------------------------------------------------
def run_videntis_engine(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    If the Videntis engine modules are available, generate
    a simple recommendation score per sector using the
    TrendPipeline + RiskEngine.

    Returns a DataFrame of sector-level scores, or None if
    the engine is not available.
    """
    if TrendPipeline is None or RiskEngine is None or TrendModel is None:
        print("[info] Engine modules not found. Skipping pipeline scoring.")
        return None

    print("[info] Running Videntis TrendPipeline + RiskEngine demo.")

    # Aggregate by sector to get a simple snapshot
    sector_groups = df.groupby("sector")
    sector_scores = []

    model = TrendModel()
    risk_engine = RiskEngine()
    pipeline = TrendPipeline(model=model, risk_engine=risk_engine)

    for sector, group in sector_groups:
        sector_df = group.sort_values("date")
        returns = sector_df["price_index"].pct_change().dropna().tolist()
        sentiment = float(sector_df["sentiment"].mean())

        score = pipeline.score_sector(returns=returns, sentiment=sentiment)
        sector_scores.append({"sector": sector, "videntis_score": score})

    result = pd.DataFrame(sector_scores).sort_values("videntis_score", ascending=False)
    return result


# -------------------------------------------------------------------
# Visualisations
# -------------------------------------------------------------------
def plot_sector_scores(df: pd.DataFrame, scores: Optional[pd.DataFrame]) -> None:
    """
    Creates a bar chart of sector scores.
    Uses engine scores if available, otherwise falls back
    to a simple price-return based metric.
    """
    if scores is None:
        # Fallback: simple total return metric per sector
        print("[info] Using fallback sector score (total return).")
        tmp = (
            df.sort_values("date")
            .groupby("sector")
            .apply(lambda g: (g["price_index"].iloc[-1] / g["price_index"].iloc[0]) - 1.0)
            .reset_index(name="score")
        )
        scores = tmp.rename(columns={"score": "videntis_score"})

    plt.figure(figsize=(8, 5))
    scores = scores.sort_values("videntis_score", ascending=True)
    plt.barh(scores["sector"], scores["videntis_score"])
    plt.xlabel("Videntis Score")
    plt.title("Videntis Sector Scores")
    plt.tight_layout()

    out_path = OUTPUT_DIR / "sector_scores.png"
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"[saved] {out_path}")


def plot_top_sector_timeseries(df: pd.DataFrame, scores: Optional[pd.DataFrame]) -> None:
    """
    Plots the price index over time for the top ranked sector.
    """
    if scores is None or scores.empty:
        print("[info] No scores available, skipping top-sector time series plot.")
        return

    top_sector = scores.sort_values("videntis_score", ascending=False)["sector"].iloc[0]
    sector_df = df[df["sector"] == top_sector].sort_values("date")

    plt.figure(figsize=(8, 5))
    plt.plot(sector_df["date"], sector_df["price_index"], marker="o")
    plt.title(f"{top_sector} – Price Index Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price Index")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    out_path = OUTPUT_DIR / "top_sector_timeseries.png"
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"[saved] {out_path}")


# -------------------------------------------------------------------
# Main entry
# -------------------------------------------------------------------
def main() -> None:
    df = load_market_data()
    print(f"[info] Loaded {len(df)} rows of market data.")

    scores = run_videntis_engine(df)
    if scores is not None:
        print("[info] Videntis sector scores:")
        print(scores.to_string(index=False))

    plot_sector_scores(df, scores)
    plot_top_sector_timeseries(df, scores)

    print("\nDashboard artefacts generated in the 'dashboard' folder:")
    print(" - sector_scores.png")
    print(" - top_sector_timeseries.png")
    print("\nYou can reference these images in your README if you want.")


if __name__ == "__main__":
    main()
