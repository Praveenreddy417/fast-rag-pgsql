def classify_tier(user_role, module):
    if user_role == "trainee":
        return "TIER_2"
    return "TIER_1"


def classify_severity(message: str):
    message = message.lower()

    if "cannot login" in message or "login page" in message:
        return "MEDIUM"
    if "system down" in message:
        return "HIGH"

    return "LOW"


def escalation_needed(severity):
    return severity == "HIGH"