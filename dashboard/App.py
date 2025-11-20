import streamlit as st
import pandas as pd

# ---------------------------
# Fake but realistic sector data
# ---------------------------
def load_sector_data() -> pd.DataFrame:
    data = [
        # sector,         avg_return, volatility, sentiment
        ("AI & Automation",        0.18, 0.35, 0.80),
        ("Clean Energy",           0.14, 0.28, 0.75),
        ("Consumer Staples",       0.07, 0.15, 0.55),
        ("Healthcare & Biotech",   0.11, 0.22, 0.65),
        ("Infrastructure",         0.08, 0.18, 0.60),
        ("Real Assets (Gold/Oil)", 0.06, 0.12, 0.50),
        ("Crypto & Web3",          0.25, 0.60, 0.70),
        ("Frontier Markets",       0.20, 0.55, 0.65),
    ]
    df = pd.DataFrame(
        data,
        columns=["sector", "avg_return", "volatility", "sentiment"]
    )
    return df


# ---------------------------
# Risk / investor archetypes
# ---------------------------
RISK_PROFILES = {
    "The Guardian (Capital First)": {
        "risk_level": 0.25,
        "description": "Capital preservation first. Prefers stable sectors, avoids big drawdowns.",
    },
    "The Balanced Operator": {
        "risk_level": 0.5,
        "description": "Mix of growth and stability. Comfortable with moderate volatility.",
    },
    "The Maverick (High Conviction)": {
        "risk_level": 0.8,
        "description": "Concentrated bets in high-growth themes, accepts large swings.",
    },
    "Bull in a China Shop": {
        "risk_level": 0.95,
        "description": "Very aggressive, chases momentum and narrative – max risk profile.",
    },
}


# ---------------------------
# Scoring logic
# ---------------------------
def score_sectors(df: pd.DataFrame, risk_level: float) -> pd.DataFrame:
    """
    Create a simple 'trend score' from:
    - average return (rewarded)
    - volatility (penalised more for low-risk investors)
    - sentiment (rewarded)
    """

    # Normalise columns roughly to 0–1 scale
    df = df.copy()
    df["ret_score"] = (df["avg_return"] - df["avg_return"].min()) / (
        df["avg_return"].max() - df["avg_return"].min()
    )

    df["vol_score"] = 1.0 - (
        (df["volatility"] - df["volatility"].min())
        / (df["volatility"].max() - df["volatility"].min())
    )

    df["sent_score"] = df["sentiment"]  # already 0–1 style

    # For cautious investors, penalise volatility more
    # For aggressive investors, care more about return & sentiment
    cautious_weight = 1.0 - risk_level
    aggressive_weight = risk_level

    df["trend_score"] = (
        0.45 * df["ret_score"] * aggressive_weight
        + 0.25 * df["sent_score"]
        + 0.30 * df["vol_score"] * cautious_weight
    )

    # Scale to 0–100 for readability
    df["trend_score"] = (df["trend_score"] - df["trend_score"].min()) / (
        df["trend_score"].max() - df["trend_score"].min()
    ) * 100.0

    return df.sort_values("trend_score", ascending=False)


def allocate_portfolio(scored: pd.DataFrame, risk_level: float) -> pd.DataFrame:
    """
    Convert trend scores into approximate portfolio weights.
    Higher risk_level = allow more concentration in top sectors.
    """
    scored = scored.copy()

    # Softmax-style weighting
    # Adjust sharpness with risk_level
    sharpness = 1.0 + risk_level * 2.5
    weights_raw = (scored["trend_score"] / 100.0) ** sharpness
    weights = weights_raw / weights_raw.sum()

    scored["weight"] = (weights * 100).round(1)
    return scored


# ---------------------------
# Streamlit app
# ---------------------------
def main():
    st.set_page_config(
        page_title="Videntis – Investment Trend Dashboard",
        page_icon="📈",
        layout="wide",
    )

    st.title("Videntis – Investment Trend Dashboard")
    st.caption("Prototype tool to explore investor profiles, market sectors and suggested allocations.")

    # Sidebar controls
    st.sidebar.header("Investor Profile")

    profile_name = st.sidebar.selectbox(
        "Choose an investor type:",
        list(RISK_PROFILES.keys()),
    )
    profile = RISK_PROFILES[profile_name]

    st.sidebar.write(f"**Description:** {profile['description']}")

    # Optional fine-tuning slider
    base_risk = profile["risk_level"]
    risk_level = st.sidebar.slider(
        "Fine-tune risk level",
        min_value=0.0,
        max_value=1.0,
        value=float(base_risk),
        step=0.05,
    )

    # Load and score sectors
    df = load_sector_data()
    scored = score_sectors(df, risk_level)
    allocated = allocate_portfolio(scored, risk_level)

    # Layout: left = table, right = charts
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.subheader("Sector Trend Scores")
        st.write(
            "Each sector is scored based on return, volatility and sentiment, "
            "adjusted for the chosen risk profile."
        )
        st.dataframe(
            allocated[["sector", "trend_score", "weight"]],
            use_container_width=True,
        )

    with col2:
        st.subheader("Suggested Allocation (%)")
        st.bar_chart(
            allocated.set_index("sector")["weight"],
            use_container_width=True,
        )

        st.caption(
            "This is not financial advice – it's a prototype to show how Videntis could "
            "translate investor preferences and market data into a structured allocation."
        )

    with st.expander("Model assumptions (for reviewers / recruiters)"):
        st.markdown(
            """
- This is a **prototype**, not a production trading model.
- Sector data is synthetic but structured like a real dataset (returns, volatility, sentiment).
- Risk profiles control how much the model:
  - penalises volatility,
  - rewards high returns,
  - and leans into positive sentiment.
- The goal is to demonstrate:
  - data modelling,
  - simple scoring logic,
  - product thinking,
  - and presenting results in a way a **non-technical stakeholder** can understand.
            """
        )


if __name__ == "__main__":
    main()
