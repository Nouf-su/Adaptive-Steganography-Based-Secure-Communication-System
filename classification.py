from text_analysis import analyze_text

WEIGHTS = {
    "credit_card": 5,
    "keywords": 5,
    "passport": 4,
    "id_number": 4,
    "email": 2,
    "phone": 2,
    "ip_address": 2,
    "url": 1
}

HIGH_RISK_COMBOS = [
    {"credit_card", "email"},
    {"passport", "id_number"},
    {"credit_card", "id_number"},
    {"passport", "email"},
    {"id_number", "email"},
]

CLASSIFICATION_ACTIONS = {
    "Public":       {"hide": True, "encrypt": False, "password": False},
    "Restricted":   {"hide": True, "encrypt": True,  "password": True},
    "Confidential": {"hide": True, "encrypt": True,  "password": True},
}

def get_classification_level(score):
    if score >= 5:
        return "Confidential"
    elif score >= 1:
        return "Restricted"
    else:
        return "Public"

def calculate_score(analysis):
    score = 0
    triggered = []
# loop through each detector result
    for key, detected in analysis.items():
        if detected:
            score += WEIGHTS.get(key, 0)
            triggered.append(key) # add to the found list
# check for dangerous combinations
    triggered_set = set(triggered)
    for combo in HIGH_RISK_COMBOS:
        if combo.issubset(triggered_set):
            score += 3 # add bonus points if a dangerous combo is found

    return round(score, 2), triggered

def classify_message(message):
    if not message or not isinstance(message, str):
        return {
            "level": "Unknown",
            "score": 0,
            "triggered_detectors": [],
            "actions": {},
            "analysis": {},
            "error": "Invalid input"
        }

    message = message.strip()

    if len(message) == 0:
        return {
            "level": "Public",
            "score": 0,
            "triggered_detectors": [],
            "actions": CLASSIFICATION_ACTIONS["Public"],
            "analysis": {}
        }

    analysis = analyze_text(message)
    score, triggered = calculate_score(analysis)
    level = get_classification_level(score)
    actions = CLASSIFICATION_ACTIONS[level]

    return {
        "level": level,
        "score": score,
        "triggered_detectors": triggered,
        "actions": actions,
        "analysis": analysis
    }

