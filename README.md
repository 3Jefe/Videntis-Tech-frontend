Videntis – AI-Assisted Investment Trend Explorer

Videntis is a concept product for an AI-powered investment trend tool. It tracks where smart money is moving, combines it with historical performance and sentiment, and turns it into clear, risk-aware portfolio suggestions tailored to a user’s profile.

This repository is a small MVP that shows how the core logic could work behind the scenes. It is lightweight but structured like a real product to show product thinking, AI understanding, and clean engineering.

⸻

What Videntis is meant to do

A future Videntis user would:

• Choose an investor profile (examples included in this MVP)
• Set risk tolerance, time horizon and interests
• Allow the engine to scan market trends, historical data and sentiment
• Receive portfolio suggestions with explanations
• Optionally enable automated recurring investing

This repo implements a simplified version of that pipeline.

⸻

Investor Profiles (included in this MVP)

These profiles already exist inside the risk_engine.py file:

• Steady Compounder – Buffett-style, patient, value-driven, low turnover
• Visionary Innovator – Elon-style, high tech, disruption-focused
• Macro Strategist – energy, commodities, macro cycles awareness
• High-Octane Bull – extremely aggressive, accepts large volatility

More profiles can be added later.

⸻

Repo Structure

ai/
model.py – demo “AI” trend model

data/
market_snapshot.csv – small sample of historical returns + sentiment

engine/
pipeline.py – connects model + data + profiles

examples/
demo_run.py – full demonstration script

profiles/
risk_engine.py – investor behaviour logic

frontend/
(placeholder for future UI)

README.md

⸻

ai/model.py – Demo AI Model

This file simulates an AI model that scores sectors based on simple math using:
• historical returns
• volatility
• sentiment (0–1)

It is written like a real TrendModel class so it can be upgraded later.

⸻

profiles/risk_engine.py – Investor Archetypes

Defines how each investor type behaves:
• preferred sectors
• risk limits
• how strongly to react to sentiment
• how concentrated a portfolio is
• target risk band
• sector caps

The provided archetypes produce noticeably different portfolios from the same data.

⸻

engine/pipeline.py – End-to-End Logic

This pipeline:
	1.	loads data from data/market_snapshot.csv
	2.	uses TrendModel to score each sector
	3.	applies a chosen investor profile
	4.	outputs ranked recommendations and weights

This represents the backend logic an app could build on.

⸻

examples/demo_run.py – Demo Script

Running this script shows:
• how a user profile is chosen
• how sector scores are calculated
• how profile logic adjusts the allocation
• final recommended sectors and weights

It demonstrates data → model → risk profile → final output.

⸻

How Videntis Could Grow

Future features could include:
• real market APIs
• live sentiment models
• personalised dashboards
• automated investing
• full UI (web or mobile)
• deeper risk analytics

This MVP shows end-to-end product thinking and structure.

⸻

How to Run (Optional)

Install Python 3 and run:

python examples/demo_run.py
