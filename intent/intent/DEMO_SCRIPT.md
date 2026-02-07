Demo script — Intent AI (90s live demo)

1) One-line opener (10s)
- "Intent helps product and people teams spot hidden operational risks and prescribes actions — in seconds, from your CSV."

2) Problem statement (10s)
- "Teams guess at churn drivers and mask problems until it's too late. We turn context into prioritized actions." 

3) Show the UI + quick walkthrough (20s)
- Open app homepage.
- Point to Context Input and CSV upload controls.
- Click `Demo Growth` to load sample data.
- Explain column selectors: X = date, Y = metric.

4) Visualize (15s)
- Show the generated chart and point out trend and predictions panel.
- Say: "Judges — this is live parsing of your file; you can upload your own CSV." 

5) Run Analysis (20s)
- Click `Run Analysis` (or upload and `Upload CSV`).
- If `OPENAI_API_KEY` is set: show live AI response (summary, risk level, predictions, recommendations).
- If not, explain the deterministic mock output but say the production flow is identical.

6) Close with impact + ask (15s)
- "With this, teams can detect risks earlier, measure trends, and get action steps they can execute. We're asking for mentorship and integration partners to pilot with real datasets."

Notes for presenter:
- Keep transitions smooth; speak to value, not internals.
- If asked about architecture: point to `app.py` (Flask), `/upload` CSV handling, optional OpenAI call guarded by `OPENAI_API_KEY`.
- To demo hosted version: mention the Heroku/Docker options in `README.md`.
