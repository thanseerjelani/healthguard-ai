"""Drug Interaction Checker Tool - Fixed for Google ADK 1.19.0"""

from typing import Dict, List


def check_drug_interactions(
    current_medications: str, new_medication: str
) -> str:
    """
    Check for drug interactions between current medications and a new medication.
    
    This is a simplified mock implementation. In production, this would connect to
    a real drug interaction database API like FDA or DrugBank.
    
    Args:
        current_medications: Comma-separated string of medication names currently being taken
        new_medication: Name of the medication being considered
        
    Returns:
        JSON string containing interaction warnings and severity levels
    """
    import json
    
    # Parse medications
    med_list = [m.strip() for m in current_medications.split(',') if m.strip()]
    
    # Mock drug interaction database
    # Format: {drug_pair: {severity, description}}
    interaction_db = {
        # NSAIDs + Blood Pressure Medications
        ("ibuprofen", "lisinopril"): {
            "severity": "moderate",
            "description": "NSAIDs may reduce the effectiveness of blood pressure medications",
            "recommendation": "Use acetaminophen instead for pain relief"
        },
        ("ibuprofen", "losartan"): {
            "severity": "moderate",
            "description": "NSAIDs may reduce the effectiveness of blood pressure medications",
            "recommendation": "Use acetaminophen instead for pain relief"
        },
        
        # Aspirin + Blood Thinners
        ("aspirin", "warfarin"): {
            "severity": "severe",
            "description": "Increased risk of bleeding when combined",
            "recommendation": "Avoid combination unless specifically prescribed by doctor"
        },
        
        # Antibiotics + Birth Control
        ("amoxicillin", "birth control"): {
            "severity": "moderate",
            "description": "May reduce effectiveness of birth control pills",
            "recommendation": "Use backup contraception method"
        },
        
        # Diabetes medications
        ("metformin", "alcohol"): {
            "severity": "moderate",
            "description": "Increased risk of lactic acidosis",
            "recommendation": "Limit alcohol consumption"
        },
        
        # Common supplements
        ("st johns wort", "birth control"): {
            "severity": "severe",
            "description": "Significantly reduces birth control effectiveness",
            "recommendation": "Use alternative depression treatment"
        },
        
        # Antidepressants
        ("sertraline", "ibuprofen"): {
            "severity": "moderate",
            "description": "Increased risk of bleeding",
            "recommendation": "Monitor for unusual bleeding or bruising"
        },
    }
    
    interactions_found = []
    new_med_lower = new_medication.lower().strip()
    
    for current_med in med_list:
        current_med_lower = current_med.lower().strip()
        
        # Check both directions of drug pairs
        pair1 = (current_med_lower, new_med_lower)
        pair2 = (new_med_lower, current_med_lower)
        
        if pair1 in interaction_db:
            interaction = interaction_db[pair1].copy()
            interaction["current_medication"] = current_med
            interaction["new_medication"] = new_medication
            interactions_found.append(interaction)
        elif pair2 in interaction_db:
            interaction = interaction_db[pair2].copy()
            interaction["current_medication"] = current_med
            interaction["new_medication"] = new_medication
            interactions_found.append(interaction)
    
    if interactions_found:
        result = {
            "status": "warning",
            "has_interactions": True,
            "interaction_count": len(interactions_found),
            "interactions": interactions_found,
            "message": f"Found {len(interactions_found)} potential drug interaction(s)"
        }
    else:
        result = {
            "status": "success",
            "has_interactions": False,
            "interaction_count": 0,
            "interactions": [],
            "message": f"No known interactions found between {new_medication} and current medications"
        }
    
    return json.dumps(result, indent=2)


def get_medication_info(medication_name: str) -> str:
    """
    Get basic information about a medication.
    
    Args:
        medication_name: Name of the medication
        
    Returns:
        JSON string containing medication information
    """
    import json
    
    # Mock medication database
    medication_db = {
        "ibuprofen": {
            "generic_name": "Ibuprofen",
            "brand_names": ["Advil", "Motrin"],
            "drug_class": "NSAID (Non-steroidal anti-inflammatory drug)",
            "common_uses": ["Pain relief", "Fever reduction", "Inflammation"],
            "common_side_effects": ["Stomach upset", "Heartburn", "Dizziness"],
            "warnings": ["Take with food", "May increase bleeding risk"]
        },
        "acetaminophen": {
            "generic_name": "Acetaminophen",
            "brand_names": ["Tylenol"],
            "drug_class": "Analgesic/Antipyretic",
            "common_uses": ["Pain relief", "Fever reduction"],
            "common_side_effects": ["Rare at normal doses"],
            "warnings": ["Do not exceed 4000mg per day", "Avoid with liver disease"]
        },
        "lisinopril": {
            "generic_name": "Lisinopril",
            "brand_names": ["Prinivil", "Zestril"],
            "drug_class": "ACE Inhibitor",
            "common_uses": ["High blood pressure", "Heart failure"],
            "common_side_effects": ["Dry cough", "Dizziness", "Headache"],
            "warnings": ["May cause dizziness when standing", "Not for use during pregnancy"]
        },
        "metformin": {
            "generic_name": "Metformin",
            "brand_names": ["Glucophage"],
            "drug_class": "Biguanide (Diabetes medication)",
            "common_uses": ["Type 2 diabetes"],
            "common_side_effects": ["Diarrhea", "Nausea", "Stomach upset"],
            "warnings": ["Take with meals", "May need to stop before surgery"]
        },
        "aspirin": {
            "generic_name": "Aspirin",
            "brand_names": ["Bayer", "Bufferin"],
            "drug_class": "NSAID/Antiplatelet",
            "common_uses": ["Pain relief", "Heart attack prevention", "Stroke prevention"],
            "common_side_effects": ["Stomach irritation", "Increased bleeding"],
            "warnings": ["Take with food", "Not for children with viral illness"]
        }
    }
    
    med_lower = medication_name.lower().strip()
    
    if med_lower in medication_db:
        info = medication_db[med_lower].copy()
        info["status"] = "success"
        info["medication"] = medication_name
        return json.dumps(info, indent=2)
    else:
        result = {
            "status": "not_found",
            "medication": medication_name,
            "message": f"Information for '{medication_name}' not found in database"
        }
        return json.dumps(result, indent=2)