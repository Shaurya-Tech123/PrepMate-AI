import numpy as np
from sklearn.ensemble import RandomForestClassifier

def classify_risk(score):
    if score <= 40:
        return "Low Risk"
    elif score <= 70:
        return "Medium Risk"
    else:
        return "High Risk"
def calculate_risk(attendance, marks, attempts, pending_fee):
    if not 0 <= attendance <= 100 or not 0 <= marks <= 100:
        raise ValueError("Attendance and marks must be 0-100.")
    if attempts < 0:
        raise ValueError("Attempts cannot be negative.")
    score = 0
    factors = []
  if attendance < 50:
        score += 40
        factors.append("Very low attendance")
  elif attendance < 70:
        score += 25
        factors.append("Low attendance")
  elif attendance < 80:
        score += 10
        factors.append("Attendance below 80%")
if marks < 35:
        score += 30
        factors.append("Very low test marks")
    elif marks < 50:
        score += 20
        factors.append("Low test marks")
    elif marks < 65:
        score += 10
        score += 10
        factors.append("Pending fees")
        
    score = min(score, 100)
return {
        "risk_score": score,
        "risk_level": classify_risk(score),
        "risk_factors": factors or ["No elevated risk indicators"]
    }
# Test student
student = calculate_risk(
    attendance=55,
    marks=42,
    attempts=3,
    pending_fee=True
)
print(student)



    
         
      
      
…print(student)
