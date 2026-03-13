from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import matplotlib.pyplot as plt

app = Flask(__name__)

# -------------------------------
# Folder setup
# -------------------------------
os.makedirs("static/reports", exist_ok=True)
os.makedirs("static/images", exist_ok=True)

# -------------------------------
# Database initialization
# -------------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS patient_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        disease TEXT,
        symptoms TEXT,
        severity TEXT,
        treatment TEXT,
        rating INTEGER,
        comment TEXT,
        report TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

init_db()

# -------------------------------
# Home Page
# -------------------------------
@app.route('/')
def index():
    return render_template('index.html')

# -------------------------------
# Symptom Entry Page
# -------------------------------
@app.route('/symptom_entry')
def symptom_entry():
    return render_template('symptom_entry.html')

# -------------------------------
# Treatment Logic (Hybrid RL style)
# -------------------------------
def recommend_treatment(disease, symptoms):
    symptoms = symptoms.lower()

    # ---------- DIABETES ----------
    if disease.lower() == "diabetes":
        if any(word in symptoms for word in ["very high sugar", "confusion", "vomiting", "unconscious"]):
            return "Severe", "Emergency Insulin + Hospital Care"
        elif any(word in symptoms for word in ["high sugar", "thirst", "frequent urination", "blurred vision"]):
            return "Moderate", "Medication + Diet Control"
        else:
            return "Mild", "Lifestyle Changes"

    # ---------- HEART DISEASE ----------
    elif disease.lower() in ["heart disease", "heart attack"]:
        if any(word in symptoms for word in ["severe chest pain", "fainting", "shortness of breath at rest"]):
            return "Severe", "Hospitalization + Surgery"
        elif any(word in symptoms for word in ["chest pain", "irregular heartbeat", "dizziness"]):
            return "Moderate", "Medication + Monitoring"
        else:
            return "Mild", "General Consultation"

    # ---------- ASTHMA ----------
    elif disease.lower() == "asthma":
        if any(word in symptoms for word in ["breathing difficulty", "severe wheezing", "unable to breathe"]):
            return "Severe", "Emergency Inhalation + ICU Care"
        elif any(word in symptoms for word in ["wheezing", "shortness of breath", "chest tightness"]):
            return "Moderate", "Inhalers + Medication"
        else:
            return "Mild", "Avoid Triggers"

    # ---------- DEFAULT ----------
    else:
        return "Mild", "General Consultation"



# -------------------------------
# Submit Patient Data
# -------------------------------
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    disease = request.form['disease']
    symptoms = request.form['symptoms']

    report_file = request.files['report']
    filename = ""
    if report_file and report_file.filename != "":
        filename = report_file.filename
        report_file.save(os.path.join("static/reports", filename))

    severity, treatment = recommend_treatment(disease, symptoms)

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO patient_data
        (name, age, disease, symptoms, severity, treatment, report)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, age, disease, symptoms, severity, treatment, filename))
    conn.commit()
    conn.close()

    return render_template(
        'result.html',
        name=name,
        age=age,
        disease=disease,
        symptoms=symptoms,
        severity=severity,
        treatment=treatment
    )

# -------------------------------
# Feedback Page
# -------------------------------
@app.route('/feedback', methods=['POST'])
def feedback():
    rating = request.form['rating']
    comment = request.form['comment']

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
        UPDATE patient_data
        SET rating = ?, comment = ?
        WHERE id = (SELECT MAX(id) FROM patient_data)
    """, (rating, comment))
    conn.commit()
    conn.close()

    return redirect(url_for('graph'))

# -------------------------------
# Graph Generation
# -------------------------------
@app.route('/graph')
def graph():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT severity, COUNT(*) FROM patient_data GROUP BY severity")
    data = cur.fetchall()
    conn.close()

    severities = [row[0] for row in data]
    counts = [row[1] for row in data]

    plt.figure()
    plt.bar(severities, counts)
    plt.xlabel("Severity Level")
    plt.ylabel("Number of Patients")
    plt.title("Patient Severity Distribution")
    plt.tight_layout()

    graph_path = "static/images/graph.png"
    plt.savefig(graph_path)
    plt.close()

    return render_template('graph.html')

# -------------------------------
# Review Patient Data
# -------------------------------
@app.route('/review')
def review():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM patient_data ORDER BY created_at DESC")
    data = cur.fetchall()
    conn.close()
    return render_template('review.html', data=data)

# -------------------------------
# Run App
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
