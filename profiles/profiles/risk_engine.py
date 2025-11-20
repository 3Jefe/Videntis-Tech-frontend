 """
Videntis Risk Engine
Defines investor archetypes + sector weighting logic.
"""

class RiskEngine:
    def __init__(self):
        self.profiles = {
            "Warren Buffett": {
                "risk": "Low",
                "description": "Long-term value investing, slow but consistent.",
                "weights": {
                    "consumer_staples": 1.5,
                    "energy": 1.3,
                    "ai": 0.6,
                    "crypto": 0.3
                }
            },

            "Elon Musk": {
                "risk": "High",
                "description": "Tech-heavy, innovation-first, accepts volatility.",
                "weights": {
                    "ai": 1.8,
                    "crypto": 1.4,
                    "energy": 0.8,
                    "consumer_staples": 0.4
                }
            },

            "Saudi Royal Strategy": {
                "risk": "Medium",
                "description": "Oil + gold stability, slow-growth high asset security.",
                "weights": {
                    "energy": 2.0,
                    "consumer_staples": 1.0,
                    "ai": 0.6,
                    "crypto": 0.4
                }
            },

            "Ned Flanders": {
                "risk": "Very Low",
                "description": "Hyper-conservative, only safe stable sectors.",
                "weights": {
                    "consumer_staples": 2.0,
                    "energy": 1.0,
                    "ai": 0.2,
                    "crypto": 0.1
                }
            },

            "Bull in a China Shop": {
                "risk": "Reckless",
                "description": "Maximum chaos trader, loves high-volatility bets.",
                "weights": {
                    "ai": 2.0,
                    "crypto": 2.0,
                    "energy": 0.8,
                    "consumer_staples": 0.3
                }
            }
        }

    def get_profile(self, name):
        return self.profiles[name]

    def list_profiles(self):
        return list(self.profiles.keys())
