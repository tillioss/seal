"""
Quick Start Evaluation Script for SEAL
Simplified script to get Mayur started with prompt testing
"""

import os
import sys
import json
from pathlib import Path

# Add project root to path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

def create_simple_test_cases():
    """Create simple test cases for quick testing"""
    test_cases = {
        "emt_cases": [
            {
                "name": "EMT1_Low_Visual_Recognition",
                "description": "Class struggling with visual emotion matching",
                "input": {
                    "scores": {
                        "EMT1": [35.0, 40.0, 38.0, 42.0, 39.0],  # Low visual recognition
                        "EMT2": [75.0, 78.0, 80.0, 77.0, 79.0],  # Good situation-expression
                        "EMT3": [70.0, 72.0, 68.0, 71.0, 69.0],  # Decent labeling
                        "EMT4": [65.0, 67.0, 70.0, 68.0, 66.0]   # Fair label-expression
                    },
                    "metadata": {
                        "class_id": "QUICK_TEST_1A",
                        "deficient_area": "EMT1",
                        "num_students": 25
                    }
                },
                "expected_focus": "Visual Emotion Recognition, Emotion Flashcard Pairs"
            },
            {
                "name": "EMT2_Low_Situation_Expression",
                "description": "Class struggling with connecting situations to expressions",
                "input": {
                    "scores": {
                        "EMT1": [80.0, 82.0, 85.0, 83.0, 81.0],  # Good visual recognition
                        "EMT2": [25.0, 30.0, 28.0, 32.0, 29.0],  # Poor situation-expression
                        "EMT3": [75.0, 78.0, 80.0, 77.0, 79.0],  # Good labeling
                        "EMT4": [70.0, 72.0, 68.0, 71.0, 69.0]   # Fair label-expression
                    },
                    "metadata": {
                        "class_id": "QUICK_TEST_2B",
                        "deficient_area": "EMT2",
                        "num_students": 20
                    }
                },
                "expected_focus": "Situation-to-Expression, Story-Based Discussions"
            },
            {
                "name": "EMT3_Low_Vocabulary",
                "description": "Class struggling with emotion vocabulary",
                "input": {
                    "scores": {
                        "EMT1": [75.0, 78.0, 80.0, 77.0, 79.0],  # Good visual recognition
                        "EMT2": [70.0, 72.0, 68.0, 71.0, 69.0],  # Fair situation-expression
                        "EMT3": [20.0, 25.0, 22.0, 28.0, 24.0],  # Poor vocabulary
                        "EMT4": [65.0, 67.0, 70.0, 68.0, 66.0]   # Fair label-expression
                    },
                    "metadata": {
                        "class_id": "QUICK_TEST_3C",
                        "deficient_area": "EMT3",
                        "num_students": 30
                    }
                },
                "expected_focus": "Emotion Vocabulary, Word Wall"
            }
        ],
        "curriculum_cases": [
            {
                "name": "Grade1_Emotional_Awareness_Low",
                "description": "Grade 1 student struggling with emotional awareness",
                "input": {
                    "grade_level": "1",
                    "skill_areas": ["emotional_awareness"],
                    "score": 25.0
                },
                "expected_focus": "Color Me, Emotional Awareness"
            },
            {
                "name": "Grade2_Mixed_Skills_Moderate",
                "description": "Grade 2 student with moderate skills in multiple areas",
                "input": {
                    "grade_level": "2",
                    "skill_areas": ["emotional_awareness", "emotional_regulation"],
                    "score": 65.0
                },
                "expected_focus": "Feelings Chart, Mindfulness, Growth Mindset"
            },
            {
                "name": "Grade5_Anger_Management_High",
                "description": "Grade 5 student with high skills needing advanced anger management",
                "input": {
                    "grade_level": "5",
                    "skill_areas": ["anger_management", "emotional_regulation"],
                    "score": 85.0
                },
                "expected_focus": "Play the Judge, Time Management, Advanced strategies"
            }
        ]
    }
    return test_cases

def create_api_test_script():
    """Create a script to test the actual SEAL API"""
    script_content = '''
"""
Test SEAL API endpoints with sample data
Run this script to test the actual API responses
"""

import requests
import json
import time
from typing import Dict, Any

# API Configuration
API_BASE_URL = "http://localhost:8000"  # Change if running on different port

def test_emt_endpoint(test_case: Dict[str, Any]) -> Dict[str, Any]:
    """Test the EMT assessment endpoint"""
    url = f"{API_BASE_URL}/score"
    
    try:
        print(f"Testing EMT case: {test_case['name']}")
        print(f"Description: {test_case['description']}")
        print(f"Expected focus: {test_case['expected_focus']}")
        
        response = requests.post(url, json=test_case['input'], timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("SUCCESS!")
            print(f"Response time: {response.elapsed.total_seconds():.2f}s")
            print(f"Analysis: {result.get('analysis', 'N/A')[:100]}...")
            print(f"Number of strategies: {len(result.get('strategies', []))}")
            return {
                "success": True,
                "response_time": response.elapsed.total_seconds(),
                "response": result,
                "error": None
            }
        else:
            print(f"ERROR: {response.status_code}")
            print(f"Error details: {response.text}")
            return {
                "success": False,
                "response_time": response.elapsed.total_seconds(),
                "response": None,
                "error": f"HTTP {response.status_code}: {response.text}"
            }
    except Exception as e:
        print(f"EXCEPTION: {str(e)}")
        return {
            "success": False,
            "response_time": 0,
            "response": None,
            "error": str(e)
        }

def test_curriculum_endpoint(test_case: Dict[str, Any]) -> Dict[str, Any]:
    """Test the curriculum assessment endpoint"""
    url = f"{API_BASE_URL}/curriculum"
    
    try:
        print(f"Testing Curriculum case: {test_case['name']}")
        print(f"Description: {test_case['description']}")
        print(f"Expected focus: {test_case['expected_focus']}")
        
        response = requests.post(url, json=test_case['input'], timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("SUCCESS!")
            print(f"Response time: {response.elapsed.total_seconds():.2f}s")
            print(f"Number of interventions: {len(result.get('recommended_interventions', []))}")
            return {
                "success": True,
                "response_time": response.elapsed.total_seconds(),
                "response": result,
                "error": None
            }
        else:
            print(f"ERROR: {response.status_code}")
            print(f"Error details: {response.text}")
            return {
                "success": False,
                "response_time": response.elapsed.total_seconds(),
                "response": None,
                "error": f"HTTP {response.status_code}: {response.text}"
            }
    except Exception as e:
        print(f"EXCEPTION: {str(e)}")
        return {
            "success": False,
            "response_time": 0,
            "response": None,
            "error": str(e)
        }

def test_health_endpoint():
    """Test the health check endpoint"""
    url = f"{API_BASE_URL}/health"
    
    try:
        print("Testing health endpoint...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("Health check passed!")
            print(f"Status: {result.get('status', 'unknown')}")
            print(f"Version: {result.get('version', 'unknown')}")
            print(f"LLM Provider: {result.get('llm_provider', 'unknown')}")
            return True
        else:
            print(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Health check exception: {str(e)}")
        return False

def main():
    """Run all API tests"""
    print("Starting SEAL API Tests")
    print("=" * 50)
    
    # Test health first
    if not test_health_endpoint():
        print("API is not healthy. Please check if the server is running.")
        return
    
    print("\\n" + "=" * 50)
    
    # Load test cases
    test_cases = create_simple_test_cases()
    
    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "health_check": True,
        "emt_tests": [],
        "curriculum_tests": []
    }
    
    # Test EMT endpoints
    print("\\nTesting EMT Assessment Endpoints")
    print("-" * 40)
    for case in test_cases["emt_cases"]:
        result = test_emt_endpoint(case)
        result["test_case"] = case["name"]
        results["emt_tests"].append(result)
        print()  # Empty line for readability
    
    # Test Curriculum endpoints
    print("\\nTesting Curriculum Assessment Endpoints")
    print("-" * 40)
    for case in test_cases["curriculum_cases"]:
        result = test_curriculum_endpoint(case)
        result["test_case"] = case["name"]
        results["curriculum_tests"].append(result)
        print()  # Empty line for readability
    
    # Save results
    with open("api_test_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    # Print summary
    print("\\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    emt_success = sum(1 for r in results["emt_tests"] if r["success"])
    curriculum_success = sum(1 for r in results["curriculum_tests"] if r["success"])
    
    print(f"EMT Tests: {emt_success}/{len(results['emt_tests'])} successful")
    print(f"Curriculum Tests: {curriculum_success}/{len(results['curriculum_tests'])} successful")
    
    if results["emt_tests"]:
        avg_emt_time = sum(r["response_time"] for r in results["emt_tests"]) / len(results["emt_tests"])
        print(f"Average EMT response time: {avg_emt_time:.2f}s")
    
    if results["curriculum_tests"]:
        avg_curr_time = sum(r["response_time"] for r in results["curriculum_tests"]) / len(results["curriculum_tests"])
        print(f"Average Curriculum response time: {avg_curr_time:.2f}s")
    
    print(f"\\nResults saved to: api_test_results.json")

if __name__ == "__main__":
    main()
'''
    return script_content

def create_prompt_experimentation_guide():
    """Create a guide for prompt experimentation"""
    guide_content = '''
# SEAL Prompt Experimentation Guide

## Overview
This guide helps you experiment with different prompt configurations and analyze their outputs for the SEAL project.

## Quick Start

### 1. Test the API
```bash
# Start the SEAL API server
cd /path/to/seal
python -m uvicorn app.main:app --reload

# In another terminal, run the API tests
python test/api_test_script.py
```

### 2. Generate Realistic Test Data
```bash
python test/realistic_data_generator.py
```

### 3. Run Comprehensive Evaluation
```bash
python test/run_comprehensive_evaluation.py --num-classes 5 --human-sample-size 10
```

## Experimentation Areas

### A. Prompt Temperature Variations
Test different temperature settings to see how they affect creativity vs consistency:

- **Conservative (0.1)**: More consistent, predictable responses
- **Balanced (0.3)**: Good balance of creativity and consistency  
- **Creative (0.7)**: More varied, creative responses
- **Highly Creative (0.9)**: Maximum creativity, may be less consistent

### B. Token Limit Variations
Test different max_tokens settings:

- **1024 tokens**: Shorter, more concise responses
- **2048 tokens**: Standard length responses
- **4096 tokens**: Longer, more detailed responses

### C. Prompt Template Modifications
Experiment with different prompt templates:

1. **Safety Guidelines**: Modify the safety guidelines in prompts
2. **Instruction Clarity**: Adjust how instructions are presented
3. **Example Quality**: Improve or modify example responses
4. **Context Length**: Add or remove contextual information

### D. Input Data Variations
Test with different types of input data:

1. **Score Ranges**: Test with very low, moderate, and high scores
2. **Class Sizes**: Test with different class sizes (5, 15, 25, 35 students)
3. **Grade Levels**: Test across all supported grade levels
4. **Deficient Areas**: Test each EMT area as the primary deficiency

## Evaluation Criteria

### Automated Metrics
- **Response Time**: How quickly the API responds
- **Success Rate**: Percentage of successful API calls
- **JSON Validity**: Whether responses are valid JSON
- **Schema Compliance**: Whether responses match expected schemas

### Human Evaluation Criteria
- **Educational Appropriateness**: How well aligned with educational best practices
- **Age Appropriateness**: Suitability for target age group
- **Clarity**: How clear and understandable for teachers
- **Practicality**: How implementable in real classrooms
- **Safety**: How safe and positive for children
- **Relevance**: How well it addresses the identified deficiency

## Analysis Framework

### 1. Quantitative Analysis
- Compare response times across different configurations
- Measure success rates and error patterns
- Analyze quality scores from automated evaluation

### 2. Qualitative Analysis
- Review human evaluation feedback
- Identify common themes in comments
- Look for patterns in high vs low scoring responses

### 3. Comparative Analysis
- Compare EMT vs Curriculum tool performance
- Compare different grade levels
- Compare different deficient areas

## Iteration Process

1. **Baseline**: Run current prompts with test data
2. **Identify Issues**: Look for patterns in low-scoring responses
3. **Modify Prompts**: Make targeted improvements
4. **Re-test**: Run evaluation again with modified prompts
5. **Compare**: Compare results with baseline
6. **Iterate**: Repeat until satisfied with results

## Key Files to Modify

- `app/prompts/intervention.py`: EMT assessment prompts
- `app/prompts/curriculum.py`: Curriculum assessment prompts
- `app/llm/gateway.py`: LLM integration logic
- `app/safety/guardrails.py`: Safety validation logic

## Best Practices

1. **Version Control**: Keep track of prompt changes
2. **A/B Testing**: Test one change at a time
3. **Documentation**: Document what you changed and why
4. **Backup**: Keep copies of working prompts
5. **Gradual Changes**: Make small, incremental changes

## Common Issues and Solutions

### Issue: Responses not following schema
**Solution**: Check prompt instructions, improve examples, adjust temperature

### Issue: Responses too generic
**Solution**: Add more specific instructions, improve context, increase temperature

### Issue: Responses too long/short
**Solution**: Adjust max_tokens, modify prompt instructions

### Issue: Safety violations
**Solution**: Strengthen safety guidelines, improve safety validation

### Issue: Poor educational quality
**Solution**: Add educational expertise to prompts, improve examples

## Next Steps

1. Start with the quick start tests
2. Identify the most promising areas for improvement
3. Make targeted changes to prompts
4. Re-run evaluations
5. Compare results and iterate
'''
    return guide_content

def main():
    """Create quick start files for Mayur"""
    print("Creating Quick Start Files for SEAL Evaluation")
    
    # Create test cases
    test_cases = create_simple_test_cases()
    
    # Save test cases
    with open("test/quick_test_cases.json", "w") as f:
        json.dump(test_cases, f, indent=2)
    
    # Create API test script
    api_script = create_api_test_script()
    with open("test/api_test_script.py", "w") as f:
        f.write(api_script)
    
    # Create experimentation guide
    guide = create_prompt_experimentation_guide()
    with open("test/EXPERIMENTATION_GUIDE.md", "w") as f:
        f.write(guide)
    
    print("Quick start files created:")
    print("  - test/quick_test_cases.json: Simple test cases")
    print("  - test/api_test_script.py: API testing script")
    print("  - test/EXPERIMENTATION_GUIDE.md: Detailed experimentation guide")
    
    print("\nNext Steps for Mayur:")
    print("1. Start the SEAL API: python -m uvicorn app.main:app --reload")
    print("2. Run API tests: python test/api_test_script.py")
    print("3. Read the guide: test/EXPERIMENTATION_GUIDE.md")
    print("4. Start experimenting with different prompt configurations!")

if __name__ == "__main__":
    main()
