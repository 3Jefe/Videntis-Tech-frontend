 """
Videntis Trend Pipeline
Combines AI model + risk engine to generate final investment suggestions.
"""

from ai.model import TrendModel
from profiles.risk_engine import RiskEngine

class TrendPipeline:
    def __init__(self):
        self.model = TrendModel()
        self.risk = RiskEngine()

    def recommend(self, profile_name: str, sector_data: dict):
        profile = self.risk.get_profile(profile_name)
        ranked = self.model.rank_sectors(sector_data)

        weights = profile["weights"]

        adjusted = []
        for sector, score in ranked:
            weight = weights.get(sector, 1.0)
            adjusted_score = score * weight
            adjusted.append((sector, adjusted_score))

        adjusted.sort(key=lambda x: x[1], reverse=True)
        return adjusted
