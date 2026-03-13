import random

def predict_treatment(disease, symptoms):
    disease = disease.lower()
    symptoms = symptoms.lower()

    # ---- Severity Detection ----
    if any(x in symptoms for x in ["unconscious", "severe pain", "bleeding"]):
        severity = "Severe"
    elif any(x in symptoms for x in ["fever", "infection", "pain"]):
        severity = "Moderate"
    else:
        severity = "Mild"

    # ---- Disease-Based Treatment Mapping ----
    if "diabetes" in disease:
        if severity == "Mild":
            treatment = "Lifestyle Modification"
        elif severity == "Moderate":
            treatment = "Medication (Insulin / Oral Drugs)"
        else:
            treatment = "Specialist Care + Medication"

    elif "heart" in disease:
        if severity == "Mild":
            treatment = "Lifestyle + Monitoring"
        elif severity == "Moderate":
            treatment = "Medication"
        else:
            treatment = "Surgery / Intervention"

    elif "asthma" in disease:
        if severity == "Mild":
            treatment = "Inhaler + Lifestyle"
        elif severity == "Moderate":
            treatment = "Medication"
        else:
            treatment = "Emergency Care"

    else:
        # General diseases (RL-inspired choice)
        if severity == "Mild":
            treatment = random.choice(["Lifestyle", "Therapy"])
        elif severity == "Moderate":
            treatment = random.choice(["Medication", "Therapy"])
        else:
            treatment = random.choice(["Surgery", "Intensive Therapy"])

    return treatment, severity

