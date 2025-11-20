 from engine.pipeline import TrendPipeline

SECTOR_DATA = {
    "ai": {
        "returns": [0.12, 0.08, -0.15, 0.02, 0.10],
        "sentiment": 0.9
    },
    "energy": {
        "returns": [0.03, 0.04, 0.02, 0.01, 0.05],
        "sentiment": 0.6
    },
    "consumer_staples": {
        "returns": [0.01, 0.015, 0.012, 0.013, 0.011],
        "sentiment": 0.5
    },
    "crypto": {
        "returns": [0.25, -0.10, 0.30, -0.15, 0.20],
        "sentiment": 0.7
    }
}

pipeline = TrendPipeline()

investors = [
    "Warren Buffett",
    "Elon Musk",
    "Saudi Royal Strategy",
    "Ned Flanders",
    "Bull in a China Shop"
]

for investor in investors:
    print(f"\n=== {investor} Recommendations ===")
    ranked = pipeline.recommend(investor, SECTOR_DATA)
    for sector, score in ranked:
        print(f"{sector}: {score:.2f}")
