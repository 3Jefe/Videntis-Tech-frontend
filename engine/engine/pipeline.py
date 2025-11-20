"""
Videntis Core Trend Pipeline

This file connects:
- the AI model
- sector data
- user risk profiles
- scoring logic

This simulates the backend engine of an early-stage investment product.
"""

from ai.model import TrendModel

class TrendPipeline:
    def __init__(self, risk_profile: str):
        self.model = TrendModel()
        self.risk_profile = risk_profile.lower()

        # Simple, realistic multipliers for risk adjustment
        self.risk_modifiers = {
            "low": 0.7,
            "medium": 1.0,
            "high": 1.3,
        }

    def adjust_for_risk(self, score: float) -> float:
        modifier = self.risk_modifiers.get(self.risk_profile, 1.0)
        adjusted = score * modifier
        return round(min(100, adjusted), 2)

    def run(self, sector_data):
        """
        Steps:
        1. Get model scores for each sector
        2. Adjust scores using user’s risk profile
        3. Rank and return results
        """

        raw_scores = self.model.predict(sector_data)

        adjusted_scores = []
        for sector, score in raw_scores:
            adjusted_scores.append({
                "sector": sector,
                "base_score": score,
                "adjusted_score": self.adjust_for_risk(score)
            })

        # Sort by post-risk score
        adjusted_scores.sort(key=lambda x: x["adjusted_score"], reverse=True)

        return adjusted_scores
