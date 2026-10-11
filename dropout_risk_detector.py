
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
import json

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


FEATURES = [
    "attendance_pct",
    "average_test_score",
    "subject_attempts",
    "pending_fee",
]


@dataclass
class StudentRecord:
    student_id: str
    attendance_pct: float
    average_test_score: float
    subject_attempts: int
    pending_fee: bool


def validate_record(student: StudentRecord) -> None:
    """Reject invalid input before scoring."""
    if not 0 <= student.attendance_pct <= 100:
        raise ValueError("attendance_pct must be between 0 and 100.")
    if not 0 <= student.average_test_score <= 100:
        raise ValueError("average_test_score must be between 0 and 100.")
    if student.subject_attempts < 0:
        raise ValueError("subject_attempts cannot be negative.")


def rule_based_risk(student: StudentRecord) -> Dict:
    """
    Transparent fallback score. The weights/thresholds are demo defaults
    and should be reviewed with educators before any real deployment.
    """
    validate_record(student)
    score = 0
    factors: List[str] = []

    if student.attendance_pct < 50:
        score += 40
        factors.append("Very low attendance (<50%)")
    elif student.attendance_pct < 70:
        score += 25
        factors.append("Low attendance (<70%)")
    elif student.attendance_pct < 80:
        score += 10
        factors.append("Attendance below 80%")

    if student.average_test_score < 35:
        score += 30
        factors.append("Very low average test score (<35)")
    elif student.average_test_score < 50:
        score += 20
        factors.append("Low average test score (<50)")
    elif student.average_test_score < 65:
        score += 10
        factors.append("Average test score below 65")

    if student.subject_attempts >= 4:
        score += 20
        factors.append("High number of subject attempts (4+)")
    elif student.subject_attempts >= 2:
        score += 10
        factors.append("Multiple subject attempts (2+)")

    if student.pending_fee:
        score += 10
        factors.append("Pending fee recorded")

    score = min(score, 100)
    return {
        "risk_score": score,
        "risk_level": classify_risk(score),
        "key_factors": factors or ["No elevated risk indicators in the demo rules"],
        "method": "rule_based",
    }


def classify_risk(score: float) -> str:
    """Project flowchart thresholds: Low 0–40, Medium 41–70, High 71–100."""
    if score <= 40:
        return "Low"
    if score <= 70:
        return "Medium"
    return "High"


def make_demo_dataset(n_samples: int = 1200, random_state: int = 42):
    """
    Create synthetic data so the prototype can run without private student data.
    Labels are generated from a simple rule; this is not a real-world model.
    """
    rng = np.random.default_rng(random_state)
    attendance = rng.uniform(20, 100, n_samples)
    test_score = rng.uniform(10, 100, n_samples)
    attempts = rng.integers(0, 6, n_samples)
    pending_fee = rng.integers(0, 2, n_samples)

    labels = []
    for a, t, attempts_count, fee in zip(
        attendance, test_score, attempts, pending_fee
    ):
        demo_score = 0
        demo_score += 40 if a < 50 else 25 if a < 70 else 10 if a < 80 else 0
        demo_score += 30 if t < 35 else 20 if t < 50 else 10 if t < 65 else 0
        demo_score += 20 if attempts_count >= 4 else 10 if attempts_count >= 2 else 0
        demo_score += 10 if fee else 0
        labels.append(classify_risk(min(demo_score, 100)))

    X = np.column_stack([attendance, test_score, attempts, pending_fee])
    return X, np.array(labels)


def train_demo_model(random_state: int = 42) -> Pipeline:
    """Train a demo Random Forest model on synthetic data."""
    X, y = make_demo_dataset(random_state=random_state)
    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", RandomForestClassifier(
            n_estimators=150,
            random_state=random_state,
            class_weight="balanced",
        )),
    ])
    model.fit(X, y)
    return model


def predict_student(
    student: StudentRecord,
    model: Optional[Pipeline] = None,
) -> Dict:
    """
    Return both the transparent rule-based result and (if supplied) ML result.
    Risk is an early-warning signal, not a definitive judgement about a student.
    """
    validate_record(student)
    result = rule_based_risk(student)

    if model is not None:
        X = np.array([[
            student.attendance_pct,
            student.average_test_score,
            student.subject_attempts,
            int(student.pending_fee),
        ]], dtype=float)
        predicted_level = str(model.predict(X)[0])
        probabilities = model.predict_proba(X)[0]
        classes = model.named_steps["classifier"].classes_
        confidence = {
            str(label): round(float(prob), 3)
            for label, prob in zip(classes, probabilities)
        }
        result["ml_prediction"] = predicted_level
        result["ml_class_probabilities"] = confidence
        result["method"] = "rule_based_and_demo_ml"
        result["note"] = (
            "Demo model trained on synthetic data; probabilities are not "
            "validated real-world dropout probabilities."
        )

    result["student_id"] = student.student_id
    return result


def main() -> None:
    model = train_demo_model()

    demo_students = [
        StudentRecord("STU001", 92, 85, 0, False),
        StudentRecord("STU002", 68, 48, 2, False),
        StudentRecord("STU003", 38, 28, 5, True),
    ]

    print("\n=== PrepMate AI: Dropout Risk Detection Demo ===")
    for student in demo_students:
        result = predict_student(student, model)
        print(json.dumps(result, indent=2))
        print("-" * 55)


if __name__ == "__main__":
    main()
