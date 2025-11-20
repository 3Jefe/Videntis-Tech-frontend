 """
Videntis AI Model (Demo Version)
Simulates investment trend detection using simple statistical logic.
"""

import random
import statistics
from typing import List, Dict

class TrendModel:
    def __init__(self):
        self.base_trend_strength = 0.5

    def score_sector(self, historical_returns: List[float], sentiment: float):
        if len(historical_returns) == 0:
            return 0.0
        
        mean_return = statistics.mean(historical_returns)
        volatility = statistics.pvariance(historical_returns)

        score = (
            (mean_return * 20)
            - (volatility * 10)
            + (sentiment * 30)
            + (self.base_trend_strength * 10)
        )

        return max(0, min(100, score))

    def rank_sectors(self, sector_data: Dict):
        rankings = []
        for sector, info in sector_data.items():
            score = self.score_sector(info["returns"], info["sentiment"])
            rankings.append((sector, score))
        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings
