"""
Comprehensive SEAL Evaluation Script
Integrates automated testing, realistic data generation, and human evaluation
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Any
import argparse

# Add project root to path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from evaluation_framework import SEALEvaluator, TestCase
from realistic_data_generator import RealisticDataGenerator
from human_evaluation_framework import HumanEvaluationFramework

class ComprehensiveSEALEvaluator:
    """Comprehensive evaluation system for SEAL prompts"""
    
    def __init__(self, output_dir: str = "test/comprehensive_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.automated_evaluator = SEALEvaluator(str(self.output_dir / "automated"))
        self.data_generator = RealisticDataGenerator()
        self.human_evaluator = HumanEvaluationFramework(str(self.output_dir / "human"))
        
        self.results = {
            "automated_results": [],
            "human_evaluation_interface": None,
            "test_data_generated": False,
            "evaluation_summary": {}
        }
    
    def generate_realistic_test_data(self, num_classes_per_grade: int = 10) -> List[TestCase]:
        """Generate realistic test data and convert to test cases"""
        print("🔄 Generating realistic test data...")
        
        # Generate class profiles
        profiles = self.data_generator.generate_test_dataset(num_classes_per_grade)
        
        # Save generated data
        self.data_generator.save_test_data(profiles, str(self.output_dir / "data"))
        
        # Convert to test cases
        emt_cases = self.data_generator.create_emt_test_cases(profiles)
        curriculum_cases = self.data_generator.create_curriculum_test_cases(profiles)
        
        # Convert to TestCase objects
        test_cases = []
        
        for case_data in emt_cases:
            test_case = TestCase(
                name=case_data["name"],
                input_data=case_data["input_data"],
                expected_focus_areas=case_data["expected_focus_areas"],
                test_type=case_data["test_type"],
                description=case_data["description"]
            )
            test_cases.append(test_case)
        
        for case_data in curriculum_cases:
            test_case = TestCase(
                name=case_data["name"],
                input_data=case_data["input_data"],
                expected_focus_areas=case_data["expected_focus_areas"],
                grade_level=case_data["grade_level"],
                test_type=case_data["test_type"],
                description=case_data["description"]
            )
            test_cases.append(test_case)
        
        self.results["test_data_generated"] = True
        print(f"✅ Generated {len(test_cases)} test cases from {len(profiles)} class profiles")
        
        return test_cases
    
    def run_automated_evaluation(self, test_cases: List[TestCase], 
                               model_configs: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Run automated evaluation on test cases"""
        print("🤖 Running automated evaluation...")
        
        if model_configs is None:
            model_configs = [
                {"provider": "gemini", "temperature": 0.1, "max_tokens": 1024, "name": "conservative"},
                {"provider": "gemini", "temperature": 0.3, "max_tokens": 2048, "name": "balanced"},
                {"provider": "gemini", "temperature": 0.7, "max_tokens": 2048, "name": "creative"},
                {"provider": "gemini", "temperature": 0.9, "max_tokens": 4096, "name": "highly_creative"}
            ]
        
        # Run evaluation
        self.automated_evaluator.run_evaluation(test_cases, model_configs)
        
        # Generate report
        self.automated_evaluator.generate_report()
        
        # Store results
        self.results["automated_results"] = self.automated_evaluator.results
        
        print(f"✅ Automated evaluation completed with {len(self.automated_evaluator.results)} results")
        
        return self.automated_evaluator.results
    
    def create_human_evaluation_interface(self, test_cases: List[TestCase], 
                                        sample_size: int = 20) -> str:
        """Create human evaluation interface with sample of test cases"""
        print("👥 Creating human evaluation interface...")
        
        # Sample test cases for human evaluation
        import random
        sampled_cases = random.sample(test_cases, min(sample_size, len(test_cases)))
        
        # Convert to format expected by human evaluator
        test_case_data = []
        model_response_data = []
        
        for case in sampled_cases:
            test_case_data.append({
                "name": case.name,
                "test_type": case.test_type,
                "description": case.description,
                "grade_level": getattr(case, 'grade_level', None),
                "input_data": case.input_data
            })
            
            # Generate sample response (replace with actual API calls)
            if case.test_type == "emt":
                sample_response = {
                    "analysis": f"Analysis for {case.name} - focusing on {case.input_data['metadata']['deficient_area']}",
                    "strategies": [
                        {
                            "activity": f"Sample Activity for {case.input_data['metadata']['deficient_area']}",
                            "implementation": ["Step 1: Prepare materials", "Step 2: Introduce activity", "Step 3: Guide students", "Step 4: Assess progress"],
                            "expected_outcomes": ["Improved understanding", "Better engagement"],
                            "time_allocation": "30 minutes",
                            "resources": ["Activity materials", "Assessment tools"]
                        }
                    ],
                    "timeline": {
                        "week1": ["Introduction and setup"],
                        "week2": ["Core activities"],
                        "week3": ["Practice and reinforcement"],
                        "week4": ["Assessment and review"]
                    },
                    "success_metrics": {
                        "quantitative": ["20% improvement in scores"],
                        "qualitative": ["Increased student engagement"],
                        "assessment_methods": ["Weekly assessments", "Teacher observations"]
                    }
                }
            else:  # curriculum
                sample_response = {
                    "recommended_interventions": [
                        {
                            "name": f"Sample Intervention for Grade {case.input_data['grade_level']}",
                            "grade_levels": [case.input_data['grade_level']],
                            "skill_area": case.input_data['skill_areas'][0],
                            "summary": f"Intervention targeting {case.input_data['skill_areas'][0]}",
                            "implementation": {
                                "steps": ["Step 1: Preparation", "Step 2: Introduction", "Step 3: Practice", "Step 4: Assessment"],
                                "materials": ["Required materials"],
                                "time_allocation": "20 minutes"
                            },
                            "intended_purpose": "Improve emotional learning skills"
                        }
                    ],
                    "skill_focus": case.input_data['skill_areas'],
                    "implementation_order": ["Primary intervention", "Supporting activities"]
                }
            
            model_response_data.append(sample_response)
        
        # Create interface
        interface_path = self.human_evaluator.create_evaluation_interface(
            test_case_data, model_response_data
        )
        
        self.results["human_evaluation_interface"] = interface_path
        print(f"✅ Human evaluation interface created: {interface_path}")
        
        return interface_path
    
    def analyze_results(self) -> Dict[str, Any]:
        """Analyze and summarize all evaluation results"""
        print("📊 Analyzing evaluation results...")
        
        summary = {
            "evaluation_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "test_data_generated": self.results["test_data_generated"],
            "automated_evaluation": {},
            "human_evaluation_available": self.results["human_evaluation_interface"] is not None
        }
        
        # Analyze automated results
        if self.results["automated_results"]:
            automated_results = self.results["automated_results"]
            
            # Calculate statistics
            success_rate = sum(1 for r in automated_results if r.success) / len(automated_results)
            avg_quality = sum(r.quality_score for r in automated_results) / len(automated_results)
            avg_response_time = sum(r.response_time for r in automated_results) / len(automated_results)
            
            # Group by test type
            emt_results = [r for r in automated_results if r.test_case.test_type == "emt"]
            curriculum_results = [r for r in automated_results if r.test_case.test_type == "curriculum"]
            
            summary["automated_evaluation"] = {
                "total_tests": len(automated_results),
                "success_rate": success_rate,
                "average_quality_score": avg_quality,
                "average_response_time": avg_response_time,
                "emt_tests": len(emt_results),
                "curriculum_tests": len(curriculum_results),
                "results_by_type": {
                    "emt": {
                        "count": len(emt_results),
                        "avg_quality": sum(r.quality_score for r in emt_results) / len(emt_results) if emt_results else 0,
                        "success_rate": sum(1 for r in emt_results if r.success) / len(emt_results) if emt_results else 0
                    },
                    "curriculum": {
                        "count": len(curriculum_results),
                        "avg_quality": sum(r.quality_score for r in curriculum_results) / len(curriculum_results) if curriculum_results else 0,
                        "success_rate": sum(1 for r in curriculum_results if r.success) / len(curriculum_results) if curriculum_results else 0
                    }
                }
            }
        
        self.results["evaluation_summary"] = summary
        
        # Save summary
        summary_path = self.output_dir / "evaluation_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print(f"✅ Analysis complete. Summary saved to: {summary_path}")
        
        return summary
    
    def print_summary_report(self):
        """Print a comprehensive summary report"""
        summary = self.results["evaluation_summary"]
        
        print("\n" + "="*80)
        print("SEAL COMPREHENSIVE EVALUATION REPORT")
        print("="*80)
        print(f"Evaluation Date: {summary.get('evaluation_timestamp', 'N/A')}")
        print(f"Test Data Generated: {'✅' if summary.get('test_data_generated') else '❌'}")
        print(f"Human Evaluation Interface: {'✅' if summary.get('human_evaluation_available') else '❌'}")
        
        if summary.get("automated_evaluation"):
            auto = summary["automated_evaluation"]
            print(f"\n🤖 AUTOMATED EVALUATION RESULTS:")
            print(f"  Total Tests: {auto.get('total_tests', 0)}")
            print(f"  Success Rate: {auto.get('success_rate', 0):.1%}")
            print(f"  Average Quality Score: {auto.get('average_quality_score', 0):.2f}/1.0")
            print(f"  Average Response Time: {auto.get('average_response_time', 0):.2f}s")
            
            if auto.get("results_by_type"):
                by_type = auto["results_by_type"]
                print(f"\n  📊 Results by Type:")
                for test_type, stats in by_type.items():
                    print(f"    {test_type.upper()}:")
                    print(f"      Tests: {stats.get('count', 0)}")
                    print(f"      Quality: {stats.get('avg_quality', 0):.2f}")
                    print(f"      Success: {stats.get('success_rate', 0):.1%}")
        
        print(f"\n📁 Results saved to: {self.output_dir}")
        print(f"👥 Human evaluation interface: {self.results.get('human_evaluation_interface', 'Not created')}")
        
        print("\n" + "="*80)
        print("NEXT STEPS:")
        print("1. Review automated evaluation results")
        print("2. Use human evaluation interface for qualitative assessment")
        print("3. Compare human vs automated evaluations")
        print("4. Iterate on prompts based on findings")
        print("="*80)

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Comprehensive SEAL Evaluation")
    parser.add_argument("--num-classes", type=int, default=10, 
                       help="Number of classes per grade to generate")
    parser.add_argument("--human-sample-size", type=int, default=20,
                       help="Number of test cases for human evaluation")
    parser.add_argument("--skip-human", action="store_true",
                       help="Skip human evaluation interface creation")
    parser.add_argument("--output-dir", type=str, default="test/comprehensive_results",
                       help="Output directory for results")
    
    args = parser.parse_args()
    
    print("🚀 Starting Comprehensive SEAL Evaluation")
    print(f"📊 Configuration:")
    print(f"  - Classes per grade: {args.num_classes}")
    print(f"  - Human evaluation sample: {args.human_sample_size}")
    print(f"  - Output directory: {args.output_dir}")
    print(f"  - Skip human evaluation: {args.skip_human}")
    
    # Initialize evaluator
    evaluator = ComprehensiveSEALEvaluator(args.output_dir)
    
    try:
        # Step 1: Generate realistic test data
        test_cases = evaluator.generate_realistic_test_data(args.num_classes)
        
        # Step 2: Run automated evaluation
        automated_results = evaluator.run_automated_evaluation(test_cases)
        
        # Step 3: Create human evaluation interface (if not skipped)
        if not args.skip_human:
            human_interface = evaluator.create_human_evaluation_interface(
                test_cases, args.human_sample_size
            )
        
        # Step 4: Analyze results
        summary = evaluator.analyze_results()
        
        # Step 5: Print comprehensive report
        evaluator.print_summary_report()
        
        print("\n✅ Comprehensive evaluation completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during evaluation: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
