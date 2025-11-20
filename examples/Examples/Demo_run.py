"""
Videntis Demo Script

Runs the TrendPipeline + RiskEngine together using dummy sector data
to show how recommendations would look for different investor archetypes.
"""

from engine.pipeline import TrendPipeline
from profiles.risk_engine import RiskEngine


# Very small example of made-up sector data
SECTOR_DATA = {
    "ai": {
        "returns": [0.12, 0.08, 0.15, -0.02, 0.10],
        "sentiment": 0.9,
    },
    "energy": {
        "returns": [0.03, 0.04, 0.02, 0.01, 0.05],
        "sentiment": 0.6,
    },
    "consumer_staples": {
        "returns": [0.01, 0.015, 0.012, 0.013, 0.011],
        "sentiment": 0.5,
    },
    "crypto": {
        "returns": [0.25, -0.10, 0.30, -0.15, 0.20],
        "sentiment": 0.7,
    },
}


# Simple mapping from archetype → overall risk band
ARCHETYPE_TO_RISK_BAND = {
    "buffett": "low",
    "nedflanders": "low",
    "londonlandlord": "medium",
    "oldmoney": "medium",
    "aiquant": "medium",
    "sovereignfund": "medium",
    "elon": "high",
    "wolf": "high",
    "cryptobro": "high",
    "bullinchinashop": "high",
}


def run_demo(profile_name: str):
    print(f"\n=== Videntis Demo for profile: {profile_name} ===")

    # Load full profile config
    risk_engine = RiskEngine(profile_name)
    profile_config = risk_engine.get_profile()

    print(f"Style: {profile_config['style']}")
    print(f"Description: {profile_config['description']}")
    print(f"Volatility tolerance: {profile_config['volatility_tolerance']}")
    print(f"Max allocation per sector: {profile_config['max_allocation_per_sector']}")
    print(f"Preferred sectors: {profile_config.get('preferred_sectors', [])}\n")

    # Map archetype to a coarse risk band for the pipeline
    risk_band = ARCHETYPE_TO_RISK_BAND.get(profile_name.lower(), "medium")

    pipeline = TrendPipeline(risk_profile=risk_band)
    results = pipeline.run(SECTOR_DATA)

    print("Recommended sectors (highest to lowest adjusted score):\n")
    for item in results:
        print(
            f"- {item['sector']} | base={item['base_score']} | "
            f"adjusted={item['adjusted_score']}"
        )


if __name__ == "__main__":
    # Try changing this value to: "elon", "buffett", "cryptobro", "nedflanders", "bullinchinashop", etc.
    run_demo("elon")
