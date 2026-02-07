# Intent AI — Decision Intelligence Platform

## Overview

**Intent AI** is a Flask-based web application that helps organizations predict risks and identify strategic opportunities by analyzing business context and data trends. The app integrates with OpenAI's API (optional) for live AI-powered analysis and provides CSV data visualization, trend analysis, and automated report generation.

---

## Features

- ✨ **AI-Powered Analysis**: Text-based business context analysis (with optional OpenAI integration)
- 📊 **CSV Data Upload**: Parse and visualize time-series metrics with interactive Chart.js graphs
- 📈 **Trend Detection**: Automatic risk categorization (High Risk, Warning, Medium)
- 📄 **PDF Export**: Generate professional reports with analysis, predictions, and recommendations
- 🎨 **Modern UI**: Dark-themed glassmorphic design with Tailwind CSS
- 🔒 **Input Validation**: File size limits (5MB), row limits (10K), and content validation
- ✅ **Comprehensive Tests**: Pytest-based endpoint tests with 100% coverage of core routes

---

## Quick Start

### Local Development

```bash
# Activate virtual environment
& .venv/Scripts/Activate.ps1  # Windows PowerShell
# or
source .venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Visit **http://127.0.0.1:5000** in your browser.

### Production (Gunicorn)

```bash
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Docker

```bash
docker build -t intent-ai .
docker run -p 8000:8000 intent-ai
```

---

## Environment Variables

Create a `.env` file in the project root (optional):

```env
OPENAI_API_KEY=sk-xxx...
OPENAI_MODEL=gpt-3.5-turbo
FLASK_ENV=development
FLASK_DEBUG=True
```

**Note**: Without `OPENAI_API_KEY`, the app uses a deterministic mock response (safe demo mode).

---

## API Endpoints

### GET `/`
Returns the main UI homepage.

### POST `/analyze`
Analyzes business context and returns risk assessment.

```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"data": "We are facing high employee churn..."}'
```

**Response**:
```json
{
  "status": "success",
  "risk_level": "Critical",
  "summary": "Analysis indicates volatility...",
  "predictions": [{"metric": "...", "trend": "...", "status": "..."}],
  "recommendations": ["..."]
}
```

### POST `/upload`
Uploads a CSV file and returns trend analysis.

```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@data.csv" \
  -F "column=revenue" \
  -F "x_column=date"
```

**Response**:
```json
{
  "status": "success",
  "headers": ["date", "revenue", ...],
  "labels": ["2024-01", "2024-02", ...],
  "values": [100000, 110000, ...],
  "predictions": [...],
  "summary": "..."
}
```

### POST `/export`
Generates a PDF report.

```bash
curl -X POST http://localhost:5000/export \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "...",
    "risk": "Medium",
    "predictions": [...],
    "recommendations": [...]
  }' \
  -o report.pdf
```

---

## Running Tests

```bash
# Run all tests
pytest -v

# Run specific test
pytest tests/test_app.py::test_home -v

# Generate coverage report
pytest --cov=app tests/
```

**Test Results**: All 4 tests pass ✅
- `test_home`: GET / returns 200 and HTML
- `test_analyze_mock`: POST /analyze returns JSON
- `test_upload_csv`: POST /upload parses CSV
- `test_export_pdf`: POST /export generates PDF

---

## GitHub Actions CI/CD

Push to GitHub to auto-run tests on Python 3.9, 3.10, 3.11.

See `.github/workflows/tests.yml` for configuration.

---

## CSV Format

Accepted input:

```csv
date,revenue,churn_rate
2024-01-01,100000,0.05
2024-02-01,110000,0.04
2024-03-01,120000,0.03
```

**Requirements**:
- ✅ At least one numeric column
- ✅ Max 5MB file size
- ✅ Max 10,000 rows
- ✅ UTF-8 encoding

---

## Deployment

### Heroku

```bash
heroku login
heroku create intent-ai
git push heroku main
heroku config:set OPENAI_API_KEY=sk-xxx...
```

Or use the included `app.json`:

```
https://heroku.com/deploy?template=<your-repo-url>
```

### AWS / DigitalOcean / Azure

Update the Dockerfile as needed and deploy via container registry or IaaS dashboard.

---

## Logging

Logs are printed to stdout:

```
[INFO] Analyze request: input_len=45
[INFO] File upload: demo_growth.csv
[ERROR] OpenAI error: Rate limit exceeded
```

To enable file logging, modify `app.py`:

```python
handlers=[
    logging.FileHandler('app.log'),
    logging.StreamHandler()
]
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `TemplateNotFound: index.html` | Ensure `index.html` in project root; check `template_folder='.'` in `app.py` |
| `ModuleNotFoundError: flask` | Activate venv and run `pip install -r requirements.txt` |
| CSV upload fails | Check file size (<5MB), rows (<10K), has numeric columns |
| "Incorrect API key" (OpenAI) | Verify `OPENAI_API_KEY` in `.env`; app falls back to mock mode |

---

## Security

- ✅ File upload validation (size, type, content)
- ✅ DOS protection (row limit 10K, file size 5MB)
- ✅ Input sanitization
- ✅ No stack trace leaks in errors
- ⚠️ Keep `OPENAI_API_KEY` out of git (use `.env`)

---

## Project Structure

```
intent/
├── app.py                   # Flask app
├── index.html              # UI template
├── requirements.txt        # Dependencies (pinned versions)
├── tests/test_app.py      # Test suite
├── demo_data/             # Sample CSVs
├── .github/workflows/     # GitHub Actions CI
├── Procfile               # Heroku config
├── Dockerfile             # Docker build
└── README.md              # This file
```

---

**Version**: 1.0 MVP  
**Last Updated**: February 2026  
**Built with**: Flask, Chart.js, Tailwind CSS, ReportLab, OpenAI
