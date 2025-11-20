"""
Videntis AI Model (Demo Version)

This module contains simple, believable investment-trend prediction logic.
It does NOT try to be real machine learning — instead, it simulates an
early-stage model in a way that looks realistic to employers.
"""

import random
import statistics
from typing import List, Dict

class TrendModel:
    def __init__(self):
        # pretend the model was "trained" on historical investor behaviour
        self.base_trend_strength = 0.5

    def score_sector(self, historical_returns: List[float], sentiment: float) -> float:
        """
        Generates a trend score (0–100).
        Uses:
            - mean return
            - volatility
            - sentiment input (0–1)
        """

        if len(historical_returns) == 0:
            return 0.0

        mean_return = statistics.mean(historical_returns)
        volatility = statistics.pvariance(historical_returns)

        # Simple believable formula
        score = (
            (mean_return * 20)
            - (volatility * 5)
            + (sentiment * 40)
            + random.uniform(-5, 5)      # randomness makes it seem "human"
        )

        return max(0, min(100, round(score, 2)))

    def predict(self, sector_data: Dict[str, Dict]):
        """
        Returns a ranked list of sectors with their trend score.
        """
        results = []

        for sector, info in sector_data.items():
            score = self.score_sector(
                historical_returns=info["returns"],
                sentiment=info["sentiment"],
            )
            results.append((sector, score))

        # sort from strongest to weakest
        results.sort(key=lambda x: x[1], reverse=True)
        return results
