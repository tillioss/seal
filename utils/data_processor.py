from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class EMTScores:
    """Standardized structure for EMT scores"""
    EMT1: float  # Visual Emotion Matching
    EMT2: float  # Situation-Expression Matching
    EMT3: float  # Expression Labeling
    EMT4: float  # Label-Expression Matching
    EMT1_BM: float
    EMT2_BM: float
    EMT3_BM: float
    EMT4_BM: float

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)

    @staticmethod
    def validate_scores(scores: Dict[str, float]) -> bool:
        required_scores = {'EMT1', 'EMT2', 'EMT3', 'EMT4'}
        return all(
            key in scores and f"{key}_BM" in scores
            for key in required_scores
        )

@dataclass
class ClassMetadata:
    """Standardized structure for class metadata"""
    grade_level: int
    language: str
    classroom_size: int
    class_id: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def validate_metadata(metadata: Dict[str, Any]) -> bool:
        required_fields = {'grade_level', 'language', 'classroom_size', 'class_id'}
        return all(key in metadata for key in required_fields)

class DataProcessor:
    """Handles data validation and processing"""
    
    @staticmethod
    def validate_batch_data(batch_data: Dict[str, Any]) -> bool:
        """Validate complete batch data structure"""
        try:
            if 'metadata' not in batch_data or 'scores' not in batch_data:
                return False
            
            return (
                ClassMetadata.validate_metadata(batch_data['metadata']) and
                EMTScores.validate_scores(batch_data['scores'])
            )
        except Exception as e:
            logger.error(f"Data validation failed: {e}")
            return False

    @staticmethod
    def format_batch_data(metadata: ClassMetadata, scores: EMTScores) -> Dict[str, Any]:
        """Format batch data into standardized structure"""
        return {
            "metadata": metadata.to_dict(),
            "scores": scores.to_dict()
        }