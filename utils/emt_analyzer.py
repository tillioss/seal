from enum import Enum
from dataclasses import dataclass
from typing import Dict, List

class EMTTask(Enum):
    EMT1 = "Visual Emotion Matching"  # Visual-to-visual matching
    EMT2 = "Situation-to-Expression"  # Verbal context to visual expression
    EMT3 = "Expression Labeling"      # Visual to verbal labeling
    EMT4 = "Label-to-Expression"      # Verbal label to visual expression

@dataclass
class EMTAnalysis:
    class_average: float
    skill_category: str
    intervention_priority: int  # 1-4, 1 being highest priority
    related_skills: List[str]

def analyze_emt_scores(class_scores: Dict[str, float]) -> Dict[str, EMTAnalysis]:
    """
    Analyze EMT scores to identify specific skill gaps and intervention needs.
    """
    analyses = {}
    
    # Define skill mappings and relationships
    emt_skills = {
        'EMT1': {
            'category': 'Visual Emotion Recognition',
            'related_skills': ['pattern recognition', 'visual discrimination']
        },
        'EMT2': {
            'category': 'Context-Emotion Connection',
            'related_skills': ['situational understanding', 'emotional context']
        },
        'EMT3': {
            'category': 'Emotion Vocabulary',
            'related_skills': ['emotional literacy', 'expression recognition']
        },
        'EMT4': {
            'category': 'Emotion Label Understanding',
            'related_skills': ['vocabulary comprehension', 'emotional matching']
        }
    }
    
    # Sort scores by performance (ascending)
    sorted_scores = sorted(class_scores.items(), key=lambda x: x[1])
    
    # Analyze each EMT task
    for priority, (emt, score) in enumerate(sorted_scores, 1):
        analyses[emt] = EMTAnalysis(
            class_average=score,
            skill_category=emt_skills[emt]['category'],
            intervention_priority=priority,
            related_skills=emt_skills[emt]['related_skills']
        )
    
    return analyses

def generate_intervention_strategy(analyses: Dict[str, EMTAnalysis]) -> str:
    """
    Generate targeted intervention strategy based on EMT analyses.
    """
    # Find highest priority area
    priority_area = min(analyses.items(), key=lambda x: x[1].intervention_priority)
    emt_type, analysis = priority_area
    
    # Generate intervention focus
    if emt_type == 'EMT1':
        return """
        Focus: Visual Emotion Recognition
        Primary Strategy: Visual Matching Activities
        - Use emotion flashcard pairs
        - Mirror expression practice
        - Digital emotion matching games
        """
    elif emt_type == 'EMT2':
        return """
        Focus: Situation-Emotion Connection
        Primary Strategy: Contextual Understanding
        - Story-based emotion discussions
        - Scenario cards with emotional contexts
        - Role-playing emotional situations
        """
    elif emt_type == 'EMT3':
        return """
        Focus: Emotion Vocabulary Building
        Primary Strategy: Expression-Label Connection
        - Emotion word wall
        - Expression-label matching games
        - Emotion vocabulary journals
        """
    else:  # EMT4
        return """
        Focus: Emotion Label Comprehension
        Primary Strategy: Label-to-Expression Matching
        - Emotion word-to-face games
        - Verbal emotion cues practice
        - Group emotion word activities
        """