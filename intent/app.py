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


# =========================
# LOGGING
# =========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

logger = logging.getLogger(__name__)


# =========================
# FLASK APP
# =========================
app = Flask(__name__, template_folder='templates')


# =========================
# ERROR HANDLERS
# =========================
@app.errorhandler(404)
def not_found(e):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"status": "error", "message": "Internal server error"}), 500


# =========================
# HOME PAGE
# =========================
@app.route('/')
def home():
    return render_template('index.html')


# =========================
# ANALYZE
# =========================
@app.route('/analyze', methods=['POST'])
def analyze():

    user_input = request.json.get('data')

    time.sleep(2)

    risk_level = "Medium"

    if user_input and ("churn" in user_input.lower() or "loss" in user_input.lower()):
        risk_level = "Critical"

    response_data = {
        "status": "success",
        "risk_level": risk_level,
        "summary": "Analysis indicates volatility in operational metrics.",
        "predictions": [
            {"metric": "Employee Attrition", "trend": "+12%", "status": "High Risk"},
            {"metric": "Customer Churn", "trend": "+5%", "status": "Warning"}
        ],
        "recommendations": [
            "Initiate retention program",
            "Automate workflows"
        ]
    }

    return jsonify(response_data)


# =========================
# EXPORT PDF
# =========================
@app.route('/export', methods=['POST'])
def export_pdf():

    payload = request.get_json(force=True)

    summary = payload.get('summary', '')
    risk = payload.get('risk', '')

    buffer = io.BytesIO()

    c = canvas.Canvas(buffer, pagesize=letter)

    c.drawString(40, 750, f"Risk: {risk}")
    c.drawString(40, 730, summary)

    c.save()

    buffer.seek(0)

    return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name='report.pdf')


# =========================
# CSV UPLOAD
# =========================
@app.route('/upload', methods=['POST'])
def upload():

    file = request.files.get('file')

    if not file:
        return jsonify({"status": "error"}), 400

    text = file.stream.read().decode('utf-8')

    reader = csv.reader(io.StringIO(text))

    values = []

    for row in reader:
        for cell in row:
            try:
                values.append(float(cell))
                break
            except:
                pass

    return jsonify({
        "status": "success",
        "values": values
    })


# =========================
# 🔥 ONLY IMPORTANT FIX
# RUN FLASK PROPERLY
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
