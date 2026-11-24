def user_directory_path(instance, filename):
    return f'xrays/user_{instance.user.id}/{filename}'

# PSI --------------------------

def calculate_psi_score(data):
    score = 0

    if data.gender == 'M':
        score += data.age
    else:
        score += (data.age - 10)

    if data.nursing_home: score += 10

    if data.cancer: score += 30
    if data.liver_disease: score += 20
    if data.heart_disease: score += 10
    if data.cerebrovascular_disease: score += 10
    if data.renal_disease: score += 10

    if data.altered_mental_status: score += 20
    if data.respiratory_rate >= 30: score += 20
    if data.systolic_bp < 90: score += 20
    if data.temperature < 35 or data.temperature >= 40: score += 15
    if data.pulse >= 125: score += 10

    if data.hemoglobin < 100:
        score += 10

    return score

# X-Ray --------------------------

def get_risk_class(score):
    if score <= 50:
        return "I (Low)", "0.1%"
    elif score <= 70:
        return "II (Low)", "0.6%"
    elif score <= 90:
        return "III (Moderate)", "0.9 - 2.8%"
    elif score <= 130:
        return "IV (High)", "8.2 - 9.3%"
    else:
        return "V (Very high)", "27 - 31%"