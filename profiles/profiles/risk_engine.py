"""
Videntis Risk & Investor Archetype Engine

This module defines two layers of risk profiling:

1) Standard risk profiles (low / medium / high)
2) Named investor archetypes inspired by well-known investing styles

Each profile contains:
- volatility_tolerance: how much volatility the user is comfortable with (0–1)
- max_allocation_per_sector: cap for concentration in a single sector (0–1)
- preferred_sectors: sectors this style tends to favour
- style: a short label for the approach
- description: human-readable explanation of how this "investor" behaves

The goal is to make risk/intention selection feel intuitive and memorable.
"""


class RiskEngine:
    def __init__(self, profile: str):
        self.profile = profile.lower().strip()

        # --- Standard Profiles (simple and expected in any fintech app) ---
        self.standard_profiles = {
            "low": {
                "volatility_tolerance": 0.20,
                "max_allocation_per_sector": 0.25,
                "preferred_sectors": ["bonds", "utilities", "consumer_staples"],
                "style": "Capital Preservation",
                "description": (
                    "Very cautious, prefers stability and low volatility. "
                    "Focuses on defensive sectors and predictable income."
                ),
            },
            "medium": {
                "volatility_tolerance": 0.50,
                "max_allocation_per_sector": 0.35,
                "preferred_sectors": ["large_cap_equities", "healthcare", "diversified_funds"],
                "style": "Balanced Growth",
                "description": (
                    "Balanced mix of growth and safety. Happy to take some risk for higher returns, "
                    "but still wants diversification and downside protection."
                ),
            },
            "high": {
                "volatility_tolerance": 0.80,
                "max_allocation_per_sector": 0.60,
                "preferred_sectors": ["tech", "emerging_markets", "growth_equities"],
                "style": "Aggressive Growth",
                "description": (
                    "Comfortable with big swings in portfolio value. Focuses on high-growth, "
                    "high-potential sectors and accepts the risk that comes with them."
                ),
            },
        }

        # --- Investor Archetypes (recognisable styles people can relate to) ---
        self.archetypes = {
            # ✔ Warren Buffett – classic value investor
            "buffett": {
                "volatility_tolerance": 0.30,
                "max_allocation_per_sector": 0.35,
                "preferred_sectors": ["value", "financials", "consumer_staples", "industrials"],
                "style": "Value Investing",
                "description": (
                    "Invests like Warren Buffett: patient, fundamentals-first, and focused on "
                    "undervalued, cash-generating businesses held for the long term."
                ),
            },

            # ✔ Elon – innovation-heavy, tech-focused
            "elon": {
                "volatility_tolerance": 0.85,
                "max_allocation_per_sector": 0.70,
                "preferred_sectors": ["tech", "ai", "autonomous", "space", "clean_energy"],
                "style": "Innovation-Heavy Growth",
                "description": (
                    "Allocates heavily to disruptive, high-innovation sectors: AI, EVs, space, "
                    "and frontier technology. Accepts high volatility for potential outsized returns."
                ),
            },

            # ✔ Sovereign Fund – Saudi-style long-term macro/infrastructure strategy
            "sovereignfund": {
                "volatility_tolerance": 0.45,
                "max_allocation_per_sector": 0.40,
                "preferred_sectors": ["energy", "infrastructure", "metals", "global_equities"],
                "style": "Sovereign Wealth Strategy",
                "description": (
                    "Invests like a sovereign wealth fund: long-term, globally diversified, with "
                    "significant exposure to real assets, energy, and infrastructure."
                ),
            },

            # ✔ Wolf of Wall Street – hyper-aggressive speculation
            "wolf": {
                "volatility_tolerance": 1.00,
                "max_allocation_per_sector": 0.95,
                "preferred_sectors": ["speculative_equities", "microcaps", "leveraged_etfs"],
                "style": "High-Leverage Speculation",
                "description": (
                    "Chases momentum and hype cycles, trades aggressively, and uses concentrated positions. "
                    "Very high risk tolerance, aiming for outsized short-term gains."
                ),
            },

            # ✔ Crypto Bro – all-in digital assets
            "cryptobro": {
                "volatility_tolerance": 1.00,
                "max_allocation_per_sector": 0.98,
                "preferred_sectors": ["crypto", "defi", "layer1", "metaverse"],
                "style": "Crypto Maximalist",
                "description": (
                    "Lives almost entirely in the crypto universe. Accepts extreme volatility and drawdowns "
                    "in pursuit of asymmetric upside in blockchain and digital assets."
                ),
            },

            # ✔ Ned Flanders – ultra-conservative ethical investor
            "nedflanders": {
                "volatility_tolerance": 0.10,
                "max_allocation_per_sector": 0.20,
                "preferred_sectors": ["green_energy", "healthcare", "education", "consumer_staples"],
                "style": "Ethical Capital Preservation",
                "description": (
                    "Extremely careful and values-driven. Avoids controversial industries and focuses on "
                    "ethical, stable, socially positive sectors with modest but steady growth."
                ),
            },

            # ✔ London Landlord – yield & property focused
            "londonlandlord": {
                "volatility_tolerance": 0.35,
                "max_allocation_per_sector": 0.50,
                "preferred_sectors": ["real_estate", "infrastructure", "utilities", "reits"],
                "style": "Income & Yield",
                "description": (
                    "Thinks in terms of rent-like income and long-term appreciation. Prefers property-backed "
                    "and infrastructure-style assets with recurring cashflow."
                ),
            },

            # ✔ AI Quant – algorithmic, data-driven investor
            "aiquant": {
                "volatility_tolerance": 0.60,
                "max_allocation_per_sector": 0.40,
                "preferred_sectors": ["tech", "fintech", "ai", "robotics"],
                "style": "Data-Driven Quant",
                "description": (
                    "Makes decisions based on models and statistics rather than emotion. Favors sectors "
                    "where data and signals can be systematically exploited."
                ),
            },

            # ✔ Old Money – wealth preservation over aggressive growth
            "oldmoney": {
                "volatility_tolerance": 0.30,
                "max_allocation_per_sector": 0.25,
                "preferred_sectors": ["bluechips", "luxury", "bonds", "metals", "property"],
                "style": "Wealth Preservation",
                "description": (
                    "Focused on protecting multi-generational wealth. Prefers established brands, hard assets, "
                    "and income-generating holdings over speculative growth."
                ),
            },
        }

    def get_profile(self):
        """
        Returns:
        - a detailed dict for the selected archetype (if it exists)
        - a standard risk profile (if 'low'/'medium'/'high' etc)
        - medium profile as a safe default if nothing matches
        """
        if self.profile in self.archetypes:
            return self.archetypes[self.profile]

        if self.profile in self.standard_profiles:
            return self.standard_profiles[self.profile]

        # Default fallback if unknown
        return self.standard_profiles["medium"]
