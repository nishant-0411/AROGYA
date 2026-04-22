import os
import json
from typing import Dict, Any, Optional
from datetime import datetime

try:
    from sqlalchemy import create_engine, Column, String, Text, DateTime, JSON
    from sqlalchemy.orm import declarative_base, sessionmaker
    SQLALCHEMY_AVAILABLE = True
    Base = declarative_base()

    class PatientCaseModel(Base): 
        __tablename__ = "patient_cases"
        
        patient_id = Column(String, primary_key=True, index=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        demographics = Column(JSON, default=dict)
        medical_history = Column(JSON, default=list)
        current_medications = Column(JSON, default=list)
        lab_results = Column(JSON, default=list)
        notes = Column(Text, default="")
except ImportError:
    SQLALCHEMY_AVAILABLE = False


class PatientCaseMemory:
    """
    Manages persistent case memory for patients, allowing the system to accumulate
    facts, findings, and context across multiple sessions.
    """
    
    def __init__(self, db_url: Optional[str] = None):
        self.use_sql = SQLALCHEMY_AVAILABLE
        
        if self.use_sql:
            if not db_url:
                db_url = os.getenv("DATABASE_URL")
                
            if not db_url:
                db_path = os.path.join(os.getcwd(), "data", "processed", "patients.db")
                os.makedirs(os.path.dirname(db_path), exist_ok=True)
                db_url = f"sqlite:///{db_path}"
                
            self.engine = create_engine(db_url)
            Base.metadata.create_all(self.engine)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        else:
            self.storage_dir = os.path.join(os.getcwd(), "data", "processed", "patient_cases")
            os.makedirs(self.storage_dir, exist_ok=True)

    def _get_file_path(self, patient_id: str) -> str:
        return os.path.join(self.storage_dir, f"{patient_id}.json")

    def get_case(self, patient_id: str) -> Dict[str, Any]:
        if self.use_sql:
            with self.SessionLocal() as session:
                case = session.query(PatientCaseModel).filter(PatientCaseModel.patient_id == patient_id).first()
                if not case:
                    return {}
                return {
                    "patient_id": case.patient_id,
                    "demographics": case.demographics or {},
                    "medical_history": case.medical_history or [],
                    "current_medications": case.current_medications or [],
                    "lab_results": case.lab_results or [],
                    "notes": case.notes or "",
                    "created_at": case.created_at.isoformat() if case.created_at else None,
                    "updated_at": case.updated_at.isoformat() if case.updated_at else None,
                }
        else:
            path = self._get_file_path(patient_id)
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return json.load(f)
            return {}

    def update_case(self, patient_id: str, updates: Dict[str, Any]) -> None:
        if self.use_sql:
            with self.SessionLocal() as session:
                case = session.query(PatientCaseModel).filter(PatientCaseModel.patient_id == patient_id).first()
                if not case:
                    case = PatientCaseModel(patient_id=patient_id)
                    session.add(case)
                    
                for key, value in updates.items():
                    if hasattr(case, key):
                        setattr(case, key, value)
                
                session.commit()
        else:
            case_data = self.get_case(patient_id)
            if not case_data:
                case_data = {
                    "patient_id": patient_id,
                    "created_at": datetime.utcnow().isoformat()
                }
            case_data.update(updates)
            case_data["updated_at"] = datetime.utcnow().isoformat()
            
            with open(self._get_file_path(patient_id), 'w') as f:
                json.dump(case_data, f, indent=2)

    def clear_case(self, patient_id: str) -> None:
        """Clear a patient case memory for privacy-sensitive demos."""
        if self.use_sql:
            with self.SessionLocal() as session:
                case = session.query(PatientCaseModel).filter(PatientCaseModel.patient_id == patient_id).first()
                if case:
                    session.delete(case)
                    session.commit()
        else:
            path = self._get_file_path(patient_id)
            if os.path.exists(path):
                os.remove(path)

    def get_case_summary(self, patient_id: str) -> str:
        """Get a formatted string summary of the patient case for prompt injection."""
        case = self.get_case(patient_id)
        if not case:
            return f"No persistent case memory found for patient {patient_id}."
            
        summary = f"Patient Profile ({patient_id}):\n"
        if case.get("demographics"):
            summary += f"Demographics: {case['demographics']}\n"
        if case.get("medical_history"):
            summary += "Medical History:\n"
            for item in case["medical_history"]:
                summary += f"  - {item}\n"
        if case.get("current_medications"):
            summary += "Current Medications:\n"
            for med in case["current_medications"]:
                summary += f"  - {med}\n"
        if case.get("lab_results"):
            summary += "Recent Labs/Imaging:\n"
            for lab in case["lab_results"]:
                summary += f"  - {lab}\n"
        if case.get("notes"):
            summary += f"Clinical Notes: {case['notes']}\n"
            
        return summary
