"""Sample test data fixtures for SEAL API tests."""

from typing import Dict, List, Any
import json


class SampleData:
    """Container for sample test data."""
    
    # Sample EMT Scores
    VALID_EMT_SCORES = {
        "EMT1": 3.2,
        "EMT2": 2.1,
        "EMT3": 4.1,
        "EMT4": 2.8
    }
    
    EDGE_CASE_EMT_SCORES = [
        {"EMT1": 1.0, "EMT2": 1.0, "EMT3": 1.0, "EMT4": 1.0},  # Minimum
        {"EMT1": 5.0, "EMT2": 5.0, "EMT3": 5.0, "EMT4": 5.0},  # Maximum
        {"EMT1": 1.0, "EMT2": 5.0, "EMT3": 1.0, "EMT4": 5.0},  # Mixed
        {"EMT1": 2.123, "EMT2": 3.456, "EMT3": 4.789, "EMT4": 1.234}  # Decimal precision
    ]
    
    INVALID_EMT_SCORES = [
        {"EMT1": 0.5, "EMT2": 2.1, "EMT3": 4.1, "EMT4": 2.8},  # Below minimum
        {"EMT1": 5.5, "EMT2": 2.1, "EMT3": 4.1, "EMT4": 2.8},  # Above maximum
        {"EMT1": -1.0, "EMT2": 2.1, "EMT3": 4.1, "EMT4": 2.8},  # Negative
        {"EMT1": "invalid", "EMT2": 2.1, "EMT3": 4.1, "EMT4": 2.8}  # Non-numeric
    ]
    
    # Sample Class Metadata
    VALID_CLASS_METADATA = {
        "class_name": "3rd Grade Mathematics",
        "grade_level": "3rd Grade",
        "subject": "Mathematics",
        "teacher_name": "Ms. Johnson",
        "school_name": "Sunshine Elementary School"
    }
    
    ALTERNATIVE_CLASS_METADATA = {
        "class_name": "Kindergarten Reading",
        "grade_level": "Kindergarten",
        "subject": "Language Arts",
        "teacher_name": "Mr. Rodriguez",
        "school_name": "Oak Tree Elementary"
    }
    
    # Sample Curriculum Scores
    VALID_CURRICULUM_SCORES = {
        "reading_comprehension": 2.5,
        "mathematical_reasoning": 3.2,
        "scientific_inquiry": 2.8,
        "writing_skills": 3.5,
        "critical_thinking": 2.9
    }
    
    LOW_CURRICULUM_SCORES = {
        "reading_comprehension": 1.2,
        "mathematical_reasoning": 1.5,
        "scientific_inquiry": 1.8,
        "writing_skills": 1.3,
        "critical_thinking": 1.6
    }
    
    HIGH_CURRICULUM_SCORES = {
        "reading_comprehension": 4.8,
        "mathematical_reasoning": 4.9,
        "scientific_inquiry": 4.7,
        "writing_skills": 4.6,
        "critical_thinking": 4.8
    }
    
    # Sample Intervention Requests
    VALID_INTERVENTION_REQUEST = {
        "emt_scores": VALID_EMT_SCORES,
        "class_metadata": VALID_CLASS_METADATA,
        "deficient_area": "EMT2"
    }
    
    # Sample Curriculum Requests
    VALID_CURRICULUM_REQUEST = {
        "skill_areas": ["READING_COMPREHENSION"],
        "grade_levels": ["GRADE_3"],
        "scores": VALID_CURRICULUM_SCORES,
        "class_metadata": VALID_CLASS_METADATA
    }
    
    MULTIPLE_SKILL_AREAS_REQUEST = {
        "skill_areas": ["READING_COMPREHENSION", "MATHEMATICAL_REASONING"],
        "grade_levels": ["GRADE_3", "GRADE_4"],
        "scores": VALID_CURRICULUM_SCORES,
        "class_metadata": VALID_CLASS_METADATA
    }
    
    # Sample LLM Responses
    SAMPLE_INTERVENTION_RESPONSE = {
        "analysis": "Based on the EMT2 scores, students need support with emotional expression and recognition. The class shows difficulty in connecting emotional situations with appropriate expressions.",
        "strategies": [
            {
                "name": "Emotion Recognition Cards",
                "activity": "Use visual cards to help students identify and express emotions",
                "implementation": "Display emotion cards during circle time and ask students to identify feelings",
                "expected_outcomes": "Students will improve their ability to recognize and name emotions",
                "time_allocation": "15 minutes daily",
                "resources": ["Emotion cards", "Circle time space", "Discussion prompts"]
            },
            {
                "name": "Story-Based Emotion Practice",
                "activity": "Read stories and discuss character emotions",
                "implementation": "Read age-appropriate books and pause to discuss how characters feel",
                "expected_outcomes": "Students will connect story situations to emotional expressions",
                "time_allocation": "20 minutes, 3 times per week",
                "resources": ["Picture books", "Story discussion guides"]
            }
        ],
        "timeline": {
            "week_1": "Introduction to emotion vocabulary and basic recognition",
            "week_2": "Practice with emotion cards and simple scenarios",
            "week_3": "Story-based emotion identification and discussion",
            "week_4": "Student-led emotion sharing and assessment"
        },
        "success_metrics": {
            "qualitative": "Students can identify and name at least 5 basic emotions accurately",
            "quantitative": "80% of students show improvement in EMT2 assessment scores",
            "evaluation_methods": "Weekly emotion identification assessments and teacher observation rubrics"
        }
    }
    
    SAMPLE_CURRICULUM_RESPONSE = {
        "recommended_interventions": [
            {
                "title": "Guided Reading Comprehension Program",
                "description": "Structured intervention focusing on reading comprehension skills for elementary students",
                "skill_areas": ["READING_COMPREHENSION"],
                "grade_levels": ["GRADE_3"],
                "implementation": {
                    "duration": "6 weeks",
                    "frequency": "Daily, 30 minutes",
                    "group_size": "Small groups of 4-6 students",
                    "materials": ["Leveled readers", "Comprehension worksheets", "Graphic organizers"],
                    "activities": [
                        "Pre-reading vocabulary introduction",
                        "Guided reading with comprehension questions",
                        "Post-reading discussion and summarization",
                        "Independent practice with similar texts"
                    ]
                },
                "expected_outcomes": "Students will demonstrate improved reading comprehension as measured by 15% increase in assessment scores",
                "assessment_methods": ["Pre/post reading assessments", "Weekly comprehension checks", "Running records"]
            }
        ]
    }
    
    # Sample Error Responses
    INVALID_JSON_RESPONSE = "This is not valid JSON"
    
    MISSING_FIELD_RESPONSE = {
        "analysis": "This response is missing required fields"
        # Missing strategies, timeline, success_metrics
    }
    
    EMPTY_STRATEGIES_RESPONSE = {
        "analysis": "Analysis with empty strategies",
        "strategies": [],
        "timeline": {"week_1": "Empty week"},
        "success_metrics": {"qualitative": "No strategies"}
    }
    
    # Safety Test Data
    SAFE_CONTENT = [
        "Students will learn about emotions through age-appropriate activities.",
        "The intervention focuses on building social-emotional skills.",
        "Teachers will guide students through structured learning experiences."
    ]
    
    UNSAFE_CONTENT = [
        "This content contains harmful keywords that should be blocked.",
        "Students should engage in dangerous activities.",
        "The intervention includes inappropriate content for children."
    ]
    
    # Performance Test Data
    LARGE_CLASS_NAME = "A" * 1000  # Very long class name for payload testing
    
    CONCURRENT_TEST_REQUESTS = [
        {
            "emt_scores": {"EMT1": 2.5, "EMT2": 1.8, "EMT3": 3.2, "EMT4": 2.1},
            "class_metadata": {
                "class_name": f"Concurrent Test Class {i}",
                "grade_level": "3rd Grade",
                "subject": "Math",
                "teacher_name": f"Teacher {i}",
                "school_name": f"School {i}"
            },
            "deficient_area": "EMT2"
        }
        for i in range(10)
    ]
    
    # Validation Test Cases
    VALIDATION_TEST_CASES = {
        "missing_emt_scores": {
            "class_metadata": VALID_CLASS_METADATA,
            "deficient_area": "EMT2"
        },
        "missing_class_metadata": {
            "emt_scores": VALID_EMT_SCORES,
            "deficient_area": "EMT2"
        },
        "missing_deficient_area": {
            "emt_scores": VALID_EMT_SCORES,
            "class_metadata": VALID_CLASS_METADATA
        },
        "invalid_deficient_area": {
            "emt_scores": VALID_EMT_SCORES,
            "class_metadata": VALID_CLASS_METADATA,
            "deficient_area": "INVALID_EMT"
        },
        "empty_class_name": {
            "emt_scores": VALID_EMT_SCORES,
            "class_metadata": {
                **VALID_CLASS_METADATA,
                "class_name": ""
            },
            "deficient_area": "EMT2"
        }
    }
    
    # Mock LLM Response Templates
    @staticmethod
    def get_mock_intervention_response(deficient_area: str = "EMT2") -> Dict[str, Any]:
        """Generate a mock intervention response for a specific EMT area."""
        return {
            "analysis": f"Analysis for {deficient_area} deficiency. Students need targeted support in this area.",
            "strategies": [
                {
                    "name": f"Strategy for {deficient_area}",
                    "activity": f"Activity targeting {deficient_area} skills",
                    "implementation": f"Implementation steps for {deficient_area}",
                    "expected_outcomes": f"Expected outcomes for {deficient_area}",
                    "time_allocation": "30 minutes daily",
                    "resources": [f"Resources for {deficient_area}"]
                }
            ],
            "timeline": {
                "week_1": f"Week 1 activities for {deficient_area}",
                "week_2": f"Week 2 activities for {deficient_area}",
                "week_3": f"Week 3 activities for {deficient_area}",
                "week_4": f"Week 4 assessment for {deficient_area}"
            },
            "success_metrics": {
                "qualitative": f"Qualitative metrics for {deficient_area}",
                "quantitative": f"Quantitative metrics for {deficient_area}",
                "evaluation_methods": f"Evaluation methods for {deficient_area}"
            }
        }
    
    @staticmethod
    def get_mock_curriculum_response(skill_areas: List[str]) -> Dict[str, Any]:
        """Generate a mock curriculum response for specific skill areas."""
        interventions = []
        for skill_area in skill_areas:
            interventions.append({
                "title": f"Intervention for {skill_area}",
                "description": f"Targeted intervention for {skill_area} improvement",
                "skill_areas": [skill_area],
                "grade_levels": ["GRADE_3"],
                "implementation": {
                    "duration": "4 weeks",
                    "frequency": "Daily",
                    "group_size": "Small groups",
                    "materials": [f"Materials for {skill_area}"],
                    "activities": [f"Activities for {skill_area}"]
                },
                "expected_outcomes": f"Improved {skill_area} skills",
                "assessment_methods": [f"Assessment for {skill_area}"]
            })
        
        return {"recommended_interventions": interventions}
    
    # Test Data Generators
    @staticmethod
    def generate_test_emt_scores(base_score: float = 3.0, variation: float = 1.0) -> Dict[str, float]:
        """Generate test EMT scores with controlled variation."""
        import random
        return {
            "EMT1": max(1.0, min(5.0, base_score + random.uniform(-variation, variation))),
            "EMT2": max(1.0, min(5.0, base_score + random.uniform(-variation, variation))),
            "EMT3": max(1.0, min(5.0, base_score + random.uniform(-variation, variation))),
            "EMT4": max(1.0, min(5.0, base_score + random.uniform(-variation, variation)))
        }
    
    @staticmethod
    def generate_test_curriculum_scores(base_score: float = 3.0, variation: float = 1.0) -> Dict[str, float]:
        """Generate test curriculum scores with controlled variation."""
        import random
        return {
            "reading_comprehension": max(1.0, min(5.0, base_score + random.uniform(-variation, variation))),
            "mathematical_reasoning": max(1.0, min(5.0, base_score + random.uniform(-variation, variation))),
            "scientific_inquiry": max(1.0, min(5.0, base_score + random.uniform(-variation, variation))),
            "writing_skills": max(1.0, min(5.0, base_score + random.uniform(-variation, variation))),
            "critical_thinking": max(1.0, min(5.0, base_score + random.uniform(-variation, variation)))
        }
    
    @staticmethod
    def generate_test_class_metadata(class_id: str = "TEST") -> Dict[str, str]:
        """Generate test class metadata with unique identifiers."""
        return {
            "class_name": f"{class_id} Class",
            "grade_level": "3rd Grade",
            "subject": "General",
            "teacher_name": f"Teacher {class_id}",
            "school_name": f"School {class_id}"
        } 