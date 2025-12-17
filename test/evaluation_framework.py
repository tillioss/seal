"""
SEAL Evaluation Framework
Comprehensive testing system for EMT and Curriculum prompt evaluation
"""

import json
import time
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from pathlib import Path
import os
import sys

# Add project root to path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from app.schemas.base import InterventionRequest, EMTScores, ClassMetadata
from app.schemas.curriculum import CurriculumRequest, SkillArea, GradeLevel

@dataclass
class TestCase:
    """Represents a single test case for evaluation"""
    name: str
    input_data: Dict[str, Any]
    expected_focus_areas: List[str]
    grade_level: str = None
    test_type: str = "emt"  # "emt" or "curriculum"
    description: str = ""

@dataclass
class EvaluationResult:
    """Results from evaluating a single test case"""
    test_case: TestCase
    model_response: Dict[str, Any]
    response_time: float
    success: bool
    errors: List[str]
    quality_score: float
    safety_score: float
    relevance_score: float
    completeness_score: float

class SEALEvaluator:
    """Main evaluation class for SEAL prompt testing"""
    
    def __init__(self, output_dir: str = "test/results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = []
        
    def create_test_cases(self) -> List[TestCase]:
        """Create comprehensive test cases for both prompt types"""
        test_cases = []
        
        # EMT Assessment Test Cases
        emt_cases = [
            TestCase(
                name="EMT1_Deficient_Visual_Recognition",
                input_data={
                    "scores": {
                        "EMT1": [45.0, 50.0, 48.0, 52.0, 47.0],  # Low visual recognition
                        "EMT2": [75.0, 78.0, 80.0, 77.0, 79.0],  # Good situation-expression
                        "EMT3": [70.0, 72.0, 68.0, 71.0, 69.0],  # Decent labeling
                        "EMT4": [65.0, 67.0, 70.0, 68.0, 66.0]   # Fair label-expression
                    },
                    "metadata": {
                        "class_id": "TEST_CLASS_1A",
                        "deficient_area": "EMT1",
                        "num_students": 25
                    }
                },
                expected_focus_areas=["Visual Emotion Recognition", "Emotion Flashcard Pairs"],
                test_type="emt",
                description="Class struggling with visual emotion matching"
            ),
            
            TestCase(
                name="EMT2_Deficient_Situation_Expression",
                input_data={
                    "scores": {
                        "EMT1": [80.0, 82.0, 85.0, 83.0, 81.0],  # Good visual recognition
                        "EMT2": [35.0, 40.0, 38.0, 42.0, 39.0],  # Poor situation-expression
                        "EMT3": [75.0, 78.0, 80.0, 77.0, 79.0],  # Good labeling
                        "EMT4": [70.0, 72.0, 68.0, 71.0, 69.0]   # Fair label-expression
                    },
                    "metadata": {
                        "class_id": "TEST_CLASS_2B",
                        "deficient_area": "EMT2",
                        "num_students": 20
                    }
                },
                expected_focus_areas=["Situation-to-Expression", "Story-Based Discussions"],
                test_type="emt",
                description="Class struggling with connecting situations to expressions"
            ),
            
            TestCase(
                name="EMT3_Deficient_Vocabulary",
                input_data={
                    "scores": {
                        "EMT1": [75.0, 78.0, 80.0, 77.0, 79.0],  # Good visual recognition
                        "EMT2": [70.0, 72.0, 68.0, 71.0, 69.0],  # Fair situation-expression
                        "EMT3": [30.0, 35.0, 32.0, 38.0, 34.0],  # Poor vocabulary
                        "EMT4": [65.0, 67.0, 70.0, 68.0, 66.0]   # Fair label-expression
                    },
                    "metadata": {
                        "class_id": "TEST_CLASS_3C",
                        "deficient_area": "EMT3",
                        "num_students": 30
                    }
                },
                expected_focus_areas=["Emotion Vocabulary", "Word Wall"],
                test_type="emt",
                description="Class struggling with emotion vocabulary building"
            ),
            
            TestCase(
                name="EMT4_Deficient_Label_Comprehension",
                input_data={
                    "scores": {
                        "EMT1": [80.0, 82.0, 85.0, 83.0, 81.0],  # Good visual recognition
                        "EMT2": [75.0, 78.0, 80.0, 77.0, 79.0],  # Good situation-expression
                        "EMT3": [70.0, 72.0, 68.0, 71.0, 69.0],  # Fair labeling
                        "EMT4": [25.0, 30.0, 28.0, 32.0, 29.0]   # Poor label comprehension
                    },
                    "metadata": {
                        "class_id": "TEST_CLASS_4D",
                        "deficient_area": "EMT4",
                        "num_students": 22
                    }
                },
                expected_focus_areas=["Label Comprehension", "Word-to-Face Games"],
                test_type="emt",
                description="Class struggling with verbal label to expression matching"
            ),
            
            TestCase(
                name="EMT_Mixed_Deficiencies",
                input_data={
                    "scores": {
                        "EMT1": [55.0, 58.0, 60.0, 57.0, 59.0],  # Moderate visual recognition
                        "EMT2": [45.0, 48.0, 50.0, 47.0, 49.0],  # Poor situation-expression
                        "EMT3": [50.0, 52.0, 48.0, 51.0, 49.0],  # Poor vocabulary
                        "EMT4": [40.0, 42.0, 45.0, 43.0, 41.0]   # Poor label comprehension
                    },
                    "metadata": {
                        "class_id": "TEST_CLASS_5E",
                        "deficient_area": "EMT2",  # Most deficient
                        "num_students": 28
                    }
                },
                expected_focus_areas=["Situation-to-Expression", "Multiple EMT areas"],
                test_type="emt",
                description="Class with multiple emotional learning challenges"
            )
        ]
        
        # Curriculum Assessment Test Cases
        curriculum_cases = [
            TestCase(
                name="Grade1_Emotional_Awareness_Low",
                input_data={
                    "grade_level": "1",
                    "skill_areas": ["emotional_awareness"],
                    "score": 35.0
                },
                expected_focus_areas=["Color Me", "Emotional Awareness"],
                grade_level="1",
                test_type="curriculum",
                description="Grade 1 student struggling with emotional awareness"
            ),
            
            TestCase(
                name="Grade2_Mixed_Skills_Moderate",
                input_data={
                    "grade_level": "2",
                    "skill_areas": ["emotional_awareness", "emotional_regulation"],
                    "score": 65.0
                },
                expected_focus_areas=["Feelings Chart", "Mindfulness", "Growth Mindset"],
                grade_level="2",
                test_type="curriculum",
                description="Grade 2 student with moderate skills in multiple areas"
            ),
            
            TestCase(
                name="Grade5_Anger_Management_High",
                input_data={
                    "grade_level": "5",
                    "skill_areas": ["anger_management", "emotional_regulation"],
                    "score": 85.0
                },
                expected_focus_areas=["Play the Judge", "Time Management", "Advanced strategies"],
                grade_level="5",
                test_type="curriculum",
                description="Grade 5 student with high skills needing advanced anger management"
            ),
            
            TestCase(
                name="Grade2_All_Skills_Low",
                input_data={
                    "grade_level": "2",
                    "skill_areas": ["emotional_awareness", "emotional_regulation", "anger_management"],
                    "score": 25.0
                },
                expected_focus_areas=["Multiple interventions", "Basic skills"],
                grade_level="2",
                test_type="curriculum",
                description="Grade 2 student with low skills across all areas"
            )
        ]
        
        return emt_cases + curriculum_cases
    
    def evaluate_response_quality(self, test_case: TestCase, response: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate the quality of a model response"""
        scores = {
            "safety_score": 1.0,
            "relevance_score": 0.0,
            "completeness_score": 0.0,
            "age_appropriateness": 1.0
        }
        
        # Safety evaluation (basic keyword checking)
        response_text = json.dumps(response, default=str).lower()
        unsafe_keywords = ["negative", "bad", "wrong", "failure", "can't", "won't", "impossible"]
        safety_issues = sum(1 for keyword in unsafe_keywords if keyword in response_text)
        scores["safety_score"] = max(0.0, 1.0 - (safety_issues * 0.2))
        
        # Relevance evaluation
        if test_case.test_type == "emt":
            if "strategies" in response and len(response["strategies"]) >= 3:
                scores["relevance_score"] += 0.3
            if "timeline" in response and len(response["timeline"]) >= 4:
                scores["relevance_score"] += 0.3
            if "success_metrics" in response:
                scores["relevance_score"] += 0.4
                
        elif test_case.test_type == "curriculum":
            if "recommended_interventions" in response and len(response["recommended_interventions"]) >= 2:
                scores["relevance_score"] += 0.5
            if "implementation_order" in response:
                scores["relevance_score"] += 0.3
            if "skill_focus" in response:
                scores["relevance_score"] += 0.2
        
        # Completeness evaluation
        required_fields = {
            "emt": ["analysis", "strategies", "timeline", "success_metrics"],
            "curriculum": ["recommended_interventions", "skill_focus", "implementation_order"]
        }
        
        required = required_fields.get(test_case.test_type, [])
        present_fields = sum(1 for field in required if field in response)
        scores["completeness_score"] = present_fields / len(required) if required else 0.0
        
        return scores
    
    def run_evaluation(self, test_cases: List[TestCase], model_configs: List[Dict[str, Any]] = None):
        """Run comprehensive evaluation across test cases and model configurations"""
        if model_configs is None:
            model_configs = [
                {"provider": "gemini", "temperature": 0.3, "max_tokens": 2048},
                {"provider": "gemini", "temperature": 0.7, "max_tokens": 2048},
                {"provider": "gemini", "temperature": 0.1, "max_tokens": 1024}
            ]
        
        print(f"Starting evaluation with {len(test_cases)} test cases and {len(model_configs)} model configurations")
        
        for i, test_case in enumerate(test_cases):
            print(f"\n{'='*60}")
            print(f"Test Case {i+1}/{len(test_cases)}: {test_case.name}")
            print(f"Type: {test_case.test_type.upper()}")
            print(f"Description: {test_case.description}")
            print(f"{'='*60}")
            
            for j, config in enumerate(model_configs):
                print(f"\nModel Config {j+1}/{len(model_configs)}: {config}")
                
                try:
                    # Simulate API call (replace with actual implementation)
                    start_time = time.time()
                    response = self._simulate_api_call(test_case, config)
                    response_time = time.time() - start_time
                    
                    # Evaluate response
                    quality_scores = self.evaluate_response_quality(test_case, response)
                    
                    # Create result
                    result = EvaluationResult(
                        test_case=test_case,
                        model_response=response,
                        response_time=response_time,
                        success=True,
                        errors=[],
                        quality_score=sum(quality_scores.values()) / len(quality_scores),
                        safety_score=quality_scores["safety_score"],
                        relevance_score=quality_scores["relevance_score"],
                        completeness_score=quality_scores["completeness_score"]
                    )
                    
                    self.results.append(result)
                    
                    print(f"✅ Success - Quality Score: {result.quality_score:.2f}")
                    print(f"   Safety: {result.safety_score:.2f}, Relevance: {result.relevance_score:.2f}, Completeness: {result.completeness_score:.2f}")
                    
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    result = EvaluationResult(
                        test_case=test_case,
                        model_response={},
                        response_time=0.0,
                        success=False,
                        errors=[str(e)],
                        quality_score=0.0,
                        safety_score=0.0,
                        relevance_score=0.0,
                        completeness_score=0.0
                    )
                    self.results.append(result)
    
    def _simulate_api_call(self, test_case: TestCase, config: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate API call (replace with actual implementation)"""
        # This is a placeholder - replace with actual API calls
        if test_case.test_type == "emt":
            return {
                "analysis": f"Analysis for {test_case.name}",
                "strategies": [
                    {
                        "activity": "Test Activity",
                        "implementation": ["Step 1", "Step 2", "Step 3", "Step 4"],
                        "expected_outcomes": ["Outcome 1", "Outcome 2"],
                        "time_allocation": "30 minutes",
                        "resources": ["Resource 1", "Resource 2"]
                    }
                ],
                "timeline": {
                    "week1": ["Activity 1"],
                    "week2": ["Activity 2"],
                    "week3": ["Activity 3"],
                    "week4": ["Activity 4"]
                },
                "success_metrics": {
                    "quantitative": ["50% improvement"],
                    "qualitative": ["Better understanding"],
                    "assessment_methods": ["Weekly tests"]
                }
            }
        else:  # curriculum
            return {
                "recommended_interventions": [
                    {
                        "name": "Test Intervention",
                        "grade_levels": [test_case.grade_level],
                        "skill_area": "emotional_awareness",
                        "summary": "Test summary",
                        "implementation": {
                            "steps": ["Step 1", "Step 2", "Step 3", "Step 4"],
                            "materials": ["Material 1"],
                            "time_allocation": "20 minutes"
                        },
                        "intended_purpose": "Test purpose"
                    }
                ],
                "skill_focus": ["emotional_awareness"],
                "implementation_order": ["Intervention 1", "Intervention 2"]
            }
    
    def generate_report(self):
        """Generate comprehensive evaluation report"""
        if not self.results:
            print("No results to report")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create summary DataFrame
        summary_data = []
        for result in self.results:
            summary_data.append({
                "test_case": result.test_case.name,
                "test_type": result.test_case.test_type,
                "success": result.success,
                "response_time": result.response_time,
                "quality_score": result.quality_score,
                "safety_score": result.safety_score,
                "relevance_score": result.relevance_score,
                "completeness_score": result.completeness_score,
                "errors": "; ".join(result.errors) if result.errors else ""
            })
        
        df = pd.DataFrame(summary_data)
        
        # Save detailed results
        detailed_results = {
            "timestamp": timestamp,
            "summary_stats": {
                "total_tests": len(self.results),
                "successful_tests": sum(1 for r in self.results if r.success),
                "average_quality_score": df["quality_score"].mean(),
                "average_response_time": df["response_time"].mean()
            },
            "results": [
                {
                    "test_case": result.test_case.name,
                    "test_type": result.test_case.test_type,
                    "input_data": result.test_case.input_data,
                    "response": result.model_response,
                    "scores": {
                        "quality": result.quality_score,
                        "safety": result.safety_score,
                        "relevance": result.relevance_score,
                        "completeness": result.completeness_score
                    },
                    "response_time": result.response_time,
                    "success": result.success,
                    "errors": result.errors
                }
                for result in self.results
            ]
        }
        
        # Save files
        json_path = self.output_dir / f"evaluation_results_{timestamp}.json"
        csv_path = self.output_dir / f"evaluation_summary_{timestamp}.csv"
        
        with open(json_path, 'w') as f:
            json.dump(detailed_results, f, indent=2, default=str)
        
        df.to_csv(csv_path, index=False)
        
        print(f"\n{'='*60}")
        print("EVALUATION REPORT")
        print(f"{'='*60}")
        print(f"Total Tests: {len(self.results)}")
        print(f"Successful: {sum(1 for r in self.results if r.success)}")
        print(f"Success Rate: {sum(1 for r in self.results if r.success) / len(self.results) * 100:.1f}%")
        print(f"Average Quality Score: {df['quality_score'].mean():.2f}")
        print(f"Average Response Time: {df['response_time'].mean():.2f}s")
        print(f"\nResults saved to:")
        print(f"  Detailed: {json_path}")
        print(f"  Summary: {csv_path}")

def main():
    """Main execution function"""
    evaluator = SEALEvaluator()
    
    # Create test cases
    test_cases = evaluator.create_test_cases()
    print(f"Created {len(test_cases)} test cases")
    
    # Run evaluation
    evaluator.run_evaluation(test_cases)
    
    # Generate report
    evaluator.generate_report()

if __name__ == "__main__":
    main()
