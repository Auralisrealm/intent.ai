import streamlit as st
import subprocess
import time
import webbrowser
from flask import Flask, render_template, request, jsonify, send_file
import time
import random
import csv
import io
import os
import json
import logging
import openai
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import base64
import textwrap

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates')

# Global error handler
@app.errorhandler(404)
def not_found(e):
    logger.warning(f"404 Not Found: {request.path}")
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"500 Internal Server Error: {str(e)}", exc_info=True)
    return jsonify({"status": "error", "message": "Internal server error"}), 500

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    user_input = request.json.get('data')
    logger.info(f"Analyze request: input_len={len(user_input) if user_input else 0}")
    
    # ---------------------------------------------------------
    # FOR HACKATHON DEMO: SIMULATED AI LATENCY & LOGIC
    # (This ensures your demo works 100% of the time without API keys)
    # ---------------------------------------------------------
    time.sleep(2) # Simulate "AI Thinking" time
    
    # If an OpenAI API key is present, attempt a live call (returns JSON).
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        openai.api_key = api_key
        try:
            logger.info("Attempting OpenAI API call")
            system_msg = "You are an analyst that outputs a single JSON object describing risk_level, summary, predictions (list of {metric,trend,status}), and recommendations (list of strings). Respond with JSON only."
            user_msg = f"Analyze the following business context and return JSON:\n```{user_input}```"
            resp = openai.ChatCompletion.create(
                model=os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
                messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": user_msg}],
                max_tokens=600,
                temperature=0.2,
            )
            text = resp['choices'][0]['message']['content']
            # Try to parse JSON from model output
            try:
                parsed = json.loads(text)
                parsed['status'] = parsed.get('status', 'success')
                logger.info("OpenAI returned valid JSON")
                return jsonify(parsed)
            except Exception:
                # Fall through to mock if parsing fails
                logger.warning("OpenAI response could not be parsed as JSON")
                pass
        except Exception as e:
            # Log error server-side and fall back to mock response below
            logger.error(f"OpenAI error: {str(e)}", exc_info=True)

    # Fallback mock response (safe demo path without API key)
    risk_level = "Medium"
    if user_input and ("churn" in user_input.lower() or "loss" in user_input.lower()):
        risk_level = "Critical"
    
    response_data = {
        "status": "success",
        "risk_level": risk_level,
        "summary": "Analysis indicates volatility in operational metrics. Primary concern is linked to retention and stability.",
        "predictions": [
            {"metric": "Employee Attrition", "trend": "+12%", "status": "High Risk"},
            {"metric": "Customer Churn", "trend": "+5%", "status": "Warning"},
            {"metric": "Skill Gap", "trend": "Widening", "status": "Critical"}
        ],
        "recommendations": [
            "Initiate immediate retention program for top 10% talent.",
            "Automate support workflows to reduce customer friction.",
            "Diversify supply chain to mitigate geopolitical instability."
        ]
    }

    return jsonify(response_data)


@app.route('/export', methods=['POST'])
def export_pdf():
    # Expects JSON with keys: summary, risk, predictions (list), recommendations (list), labels, values, chart (dataURL optional)
    try:
        payload = request.get_json(force=True)
    except Exception as e:
        return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400

    summary = payload.get('summary', '')
    risk = payload.get('risk', '')
    predictions = payload.get('predictions', [])
    recommendations = payload.get('recommendations', [])
    chart_dataurl = payload.get('chart')

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin_x = 40
    y = height - 40

    c.setFont('Helvetica-Bold', 18)
    c.drawString(margin_x, y, 'Intent AI Report')
    y -= 28

    c.setFont('Helvetica', 12)
    c.drawString(margin_x, y, f'Risk: {risk}')
    y -= 18

    c.setFont('Helvetica-Bold', 12)
    c.drawString(margin_x, y, 'Summary:')
    y -= 14
    c.setFont('Helvetica', 10)
    for line in textwrap.wrap(summary, 90):
        c.drawString(margin_x, y, line)
        y -= 14

    y -= 8
    # Add chart if available
    if chart_dataurl:
        try:
            header, b64 = chart_dataurl.split(',', 1)
            img_bytes = base64.b64decode(b64)
            img = ImageReader(io.BytesIO(img_bytes))
            img_w = width - margin_x * 2
            img_h = 200
            c.drawImage(img, margin_x, y - img_h, width=img_w, height=img_h)
            y -= img_h + 12
        except Exception:
            pass

    # Predictions
    if predictions:
        c.setFont('Helvetica-Bold', 12)
        c.drawString(margin_x, y, 'Predictions:')
        y -= 14
        c.setFont('Helvetica', 10)
        for p in predictions:
            text = f"- {p.get('metric', '')}: {p.get('trend', '')} ({p.get('status', '')})"
            for line in textwrap.wrap(text, 95):
                c.drawString(margin_x, y, line)
                y -= 12
            y -= 4

    # Recommendations
    if recommendations:
        c.setFont('Helvetica-Bold', 12)
        c.drawString(margin_x, y, 'Recommendations:')
        y -= 14
        c.setFont('Helvetica', 10)
        for r in recommendations:
            for line in textwrap.wrap(f"- {r}", 95):
                c.drawString(margin_x, y, line)
                y -= 12
            y -= 4

    c.showPage()
    c.save()
    buffer.seek(0)
    return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name='intent_report.pdf')


@app.route('/upload', methods=['POST'])
def upload():
    # Accept a CSV file upload, allow selecting a column by name or index,
    # parse numeric column, and return time-series for charting + headers
    file = request.files.get('file')
    if not file:
        logger.warning("Upload attempted without file")
        return jsonify({"status": "error", "message": "No file uploaded"}), 400
    
    logger.info(f"File upload: {file.filename}")
    
    # Validate file
    if not file.filename.lower().endswith('.csv'):
        logger.warning(f"Non-CSV file upload attempted: {file.filename}")
        return jsonify({"status": "error", "message": "Only CSV files are allowed"}), 400
    
    # Check file size (max 5MB)
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    if file_size > 5 * 1024 * 1024:  # 5MB
        logger.warning(f"File too large: {file_size} bytes")
        return jsonify({"status": "error", "message": "File size exceeds 5MB limit"}), 400
    file.seek(0)  # Reset to start

    selected_col = request.form.get('column')
    selected_x = request.form.get('x_column')

    try:
        text = file.stream.read().decode('utf-8', errors='ignore')
        
        # Validate CSV is not empty
        if not text.strip():
            logger.warning("Empty CSV file uploaded")
            return jsonify({"status": "error", "message": "CSV file is empty"}), 400
# Limit rows to prevent DOS (max 10,000 rows)
        stream = io.StringIO(text)
        lines = text.split('\n')
        if len(lines) > 10000:
            return jsonify({"status": "error", "message": "CSV exceeds 10,000 rows limit"}), 400
        
        stream = io.StringIO(text)

        # Peek header row
        sample = stream.getvalue().splitlines()
        headers = None
        if len(sample) > 0:
            first_row = sample[0]
            # basic split for header detection
            possible = [h.strip() for h in first_row.split(',')]
            # if any non-numeric entries, treat as header
            if any([not h.replace('.', '', 1).isdigit() for h in possible]):
                headers = possible

        labels = []
        values = []

        # If headers detected, use DictReader for convenience
        stream.seek(0)
        if headers:
            reader = csv.DictReader(stream)
            # decide which column to use
            col_name = None
            if selected_col:
                # if selected_col is an index (string of int), convert
                try:
                    idx = int(selected_col)
                    if 0 <= idx < len(headers):
                        col_name = headers[idx]
                except:
                    # treat as header name
                    if selected_col in headers:
                        col_name = selected_col
            # fallback to last header
            if not col_name:
                col_name = headers[-1]

            # decide which column to use for x-axis (labels)
            col_name_x = None
            if selected_x:
                try:
                    idx = int(selected_x)
                    if 0 <= idx < len(headers):
                        col_name_x = headers[idx]
                except:
                    if selected_x in headers:
                        col_name_x = selected_x

            row_index = 0
            for row in reader:
                row_index += 1
                cell = row.get(col_name)
                if cell is None:
                    continue
                try:
                    num = float(cell)
                except:
                    continue
                # label from x column if available, else numeric row index
                label_val = None
                if col_name_x:
                    label_val = row.get(col_name_x)
                labels.append(label_val if label_val is not None else str(row_index))
                values.append(num)
        else:
            # No headers: parse rows and select column by index or first numeric
            reader = csv.reader(stream)
            row_index = 0
            for row in reader:
                row_index += 1
                if not row:
                    continue
                num = None
                if selected_col:
                    try:
                        idx = int(selected_col)
                        if 0 <= idx < len(row):
                            num = float(row[idx])
                    except:
                        num = None
                if num is None:
                    for cell in row:
                        try:
                            num = float(cell)
                            break
                        except:
                            continue
                if num is None:
                    continue
                # x label from selected_x if numeric index provided
                label_val = None
                if selected_x:
                    try:
                        idx_x = int(selected_x)
                        if 0 <= idx_x < len(row):
                            label_val = row[idx_x]
                    except:
                        label_val = None
                labels.append(label_val if label_val is not None else str(row_index))
                values.append(num)

        if not values:
            return jsonify({"status": "error", "message": "No numeric data found in CSV. Ensure at least one column contains numbers."}), 400

        first = values[0]
        last = values[-1]
        trend_pct = ((last - first) / abs(first) * 100) if first != 0 else 0
        risk = "High Risk" if trend_pct > 10 else "Warning"

        response = {
            "status": "success",
            "headers": headers or [],
            "labels": labels,
            "values": values,
            "predictions": [
                {"metric": "Uploaded Metric", "trend": f"{trend_pct:.1f}%", "status": risk}
            ],
            "recommendations": [
                "Investigate root causes for rising metric.",
                "Run targeted interventions and measure impact over next quarter."
            ],
            "summary": f"Uploaded metric changed by {trend_pct:.1f}% over the observed period."
        }

        logger.info(f"Upload successful: {len(values)} data points parsed")
        return jsonify(response)
    except Exception as e:
        logger.error(f"Upload processing error: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500
# start flask server in background
subprocess.Popen(["python", "intent/app.py"])

time.sleep(2)

st.title("Intent AI")

st.components.v1.iframe("http://localhost:5000", height=800)

