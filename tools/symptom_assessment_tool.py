"""Symptom Assessment Tool - Fixed for Google ADK 1.19.0"""

from typing import Dict


def assess_symptom_severity(symptoms: str) -> str:
    """
    Assess the severity of symptoms and determine if medical attention is needed.
    
    Args:
        symptoms: Comma-separated list of symptoms (e.g., "headache, fever, cough")
        
    Returns:
        JSON string with severity assessment and recommendations
    """
    import json
    
    # Parse symptoms
    symptom_list = [s.strip() for s in symptoms.split(',') if s.strip()]
    
    # Emergency symptoms that require immediate medical attention
    emergency_symptoms = {
        "chest pain": "Heart attack or cardiac emergency",
        "difficulty breathing": "Respiratory emergency",
        "severe headache": "Possible stroke or hemorrhage",
        "sudden confusion": "Possible stroke",
        "loss of consciousness": "Medical emergency",
        "severe bleeding": "Trauma requiring immediate care",
        "severe abdominal pain": "Possible appendicitis or internal issue",
        "seizure": "Neurological emergency",
        "coughing blood": "Serious respiratory issue",
        "suicidal thoughts": "Mental health emergency"
    }
    
    # High-priority symptoms requiring same-day medical attention
    high_priority_symptoms = {
        "high fever": "Fever above 103°F (39.4°C)",
        "persistent vomiting": "Risk of dehydration",
        "severe pain": "Significant discomfort requiring evaluation",
        "signs of infection": "May need antibiotics",
        "difficulty swallowing": "Possible serious throat infection",
        "severe diarrhea": "Risk of dehydration"
    }
    
    # Moderate symptoms that should be monitored
    moderate_symptoms = {
        "fever": "Monitor temperature, manage with OTC medication",
        "headache": "Usually manageable with OTC pain relievers",
        "cough": "Monitor for worsening, stay hydrated",
        "sore throat": "Usually viral, rest and fluids",
        "mild pain": "Manageable with OTC pain relief",
        "fatigue": "Ensure adequate rest",
        "congestion": "Usually viral, will improve with time"
    }
    
    severity_level = "low"
    emergency_found = []
    high_priority_found = []
    moderate_found = []
    
    # Check for emergency symptoms
    for symptom in symptom_list:
        symptom_lower = symptom.lower().strip()
        
        for emergency_key, description in emergency_symptoms.items():
            if emergency_key in symptom_lower:
                emergency_found.append({
                    "symptom": symptom,
                    "reason": description
                })
                severity_level = "emergency"
        
        for high_key, description in high_priority_symptoms.items():
            if high_key in symptom_lower and severity_level != "emergency":
                high_priority_found.append({
                    "symptom": symptom,
                    "reason": description
                })
                if severity_level != "emergency":
                    severity_level = "high"
        
        for mod_key, description in moderate_symptoms.items():
            if mod_key in symptom_lower and severity_level not in ["emergency", "high"]:
                moderate_found.append({
                    "symptom": symptom,
                    "advice": description
                })
                if severity_level not in ["emergency", "high"]:
                    severity_level = "moderate"
    
    # Build response based on severity
    if severity_level == "emergency":
        result = {
            "severity": "EMERGENCY",
            "severity_level": 5,
            "action_required": "IMMEDIATE MEDICAL ATTENTION",
            "recommendation": "Call 911 or go to the emergency room immediately",
            "emergency_symptoms": emergency_found,
            "warning": "Do not wait. Seek immediate medical care."
        }
    elif severity_level == "high":
        result = {
            "severity": "HIGH PRIORITY",
            "severity_level": 4,
            "action_required": "SAME-DAY MEDICAL CARE",
            "recommendation": "Contact your doctor today or visit urgent care",
            "high_priority_symptoms": high_priority_found,
            "warning": "These symptoms require medical evaluation today"
        }
    elif severity_level == "moderate":
        result = {
            "severity": "MODERATE",
            "severity_level": 3,
            "action_required": "MONITOR AND MANAGE",
            "recommendation": "Manage symptoms at home. See doctor if symptoms worsen or persist beyond 3-5 days",
            "moderate_symptoms": moderate_found,
            "self_care_tips": [
                "Rest and stay hydrated",
                "Use over-the-counter medications as directed",
                "Monitor temperature if fever present",
                "Seek care if symptoms worsen"
            ]
        }
    else:
        result = {
            "severity": "LOW",
            "severity_level": 1,
            "action_required": "ROUTINE CARE",
            "recommendation": "Symptoms appear minor. Continue routine health maintenance.",
            "symptoms": symptom_list,
            "advice": "Schedule regular check-up if you have ongoing concerns"
        }
    
    return json.dumps(result, indent=2)


def check_symptom_duration(symptom: str, duration_days: int) -> str:
    """
    Check if symptom duration requires medical attention.
    
    Args:
        symptom: The symptom being experienced
        duration_days: How many days the symptom has persisted
        
    Returns:
        JSON string with duration assessment
    """
    import json
    
    # Symptoms with their maximum acceptable duration before seeing a doctor
    duration_thresholds = {
        "fever": 3,
        "cough": 10,
        "headache": 7,
        "sore throat": 5,
        "diarrhea": 2,
        "vomiting": 2,
        "pain": 7,
        "fatigue": 14
    }
    
    symptom_lower = symptom.lower().strip()
    
    for key, max_days in duration_thresholds.items():
        if key in symptom_lower:
            if duration_days > max_days:
                result = {
                    "status": "seek_care",
                    "symptom": symptom,
                    "duration_days": duration_days,
                    "threshold_days": max_days,
                    "message": f"{symptom} lasting more than {max_days} days should be evaluated by a doctor",
                    "recommendation": "Schedule an appointment with your healthcare provider"
                }
            else:
                result = {
                    "status": "monitor",
                    "symptom": symptom,
                    "duration_days": duration_days,
                    "threshold_days": max_days,
                    "message": f"{symptom} duration is within normal range",
                    "recommendation": "Continue monitoring. Seek care if symptoms worsen"
                }
            return json.dumps(result, indent=2)
    
    result = {
        "status": "monitor",
        "symptom": symptom,
        "duration_days": duration_days,
        "message": "Continue monitoring symptoms",
        "recommendation": "Consult healthcare provider if concerned"
    }
    return json.dumps(result, indent=2)