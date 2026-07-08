import re


def analyze_text(message):
    
    if not message or not isinstance(message, str):
        return {
            "email": False,
            "phone": False,
            "id_number": False,
            "credit_card": False,
            "keywords": False,
            "url": False,
            "ip_address": False,
            "passport": False,
        }

    # Email pattern
    email = bool(re.findall(r'[\w\.\-]+@[a-zA-Z\-]+\.[a-zA-Z]+', message))

    # Phone number pattern - must start with + or 00 or 05
    phone = bool(re.findall(r'(\+\d{10,15}|00\d{9,13}|05\d{8})', message))

    # ID number pattern
    id_number = bool(re.findall(r'\b\d{10}\b', message))

    # Credit card pattern
    credit_card = bool(re.findall(
        r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b', message))

    # Sensitive keywords pattern
    keywords_list = [
        'secret', 'confidential', 'private', 'password', 'classified',
        'restricted', 'top secret', 'sensitive', 'protected'
    ]
    keyword_found = bool(re.findall(
        r'\b(?:' + '|'.join(keywords_list) + r')\b',
        message, re.IGNORECASE))

    # URL pattern
    url = bool(re.findall(r'https?://[^\s]+', message))

    # IP address pattern
    ip_address = bool(re.findall(
        r'\b(?:25[0-5]|2[0-4]\d|1?\d?\d)\.'
        r'(?:25[0-5]|2[0-4]\d|1?\d?\d)\.'
        r'(?:25[0-5]|2[0-4]\d|1?\d?\d)\.'
        r'(?:25[0-5]|2[0-4]\d|1?\d?\d)\b', message))

    # Passport number pattern
    passport = bool(re.findall(r'\b[A-Z]{1,2}\d{6,9}\b', message))

    return {
        "email": email,
        "phone": phone,
        "id_number": id_number,
        "credit_card": credit_card,
        "keywords": keyword_found,
        "url": url,
        "ip_address": ip_address,
        "passport": passport,
    }