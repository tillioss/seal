
"""
Test SEAL API endpoints with sample data
Run this script to test the actual API responses
"""

import requests
import json
import time
from typing import Dict, Any

# API Configuration
API_BASE_URL = "http://localhost:8001"  # Change if running on different port

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
    
    print("\n" + "=" * 50)
    
    # Load test cases
    test_cases = create_simple_test_cases()
    
    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "health_check": True,
        "emt_tests": [],
        "curriculum_tests": []
    }
    
    # Test EMT endpoints
    print("\nTesting EMT Assessment Endpoints")
    print("-" * 40)
    for case in test_cases["emt_cases"]:
        result = test_emt_endpoint(case)
        result["test_case"] = case["name"]
        results["emt_tests"].append(result)
        print()  # Empty line for readability
    
    # Test Curriculum endpoints
    print("\nTesting Curriculum Assessment Endpoints")
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
    print("\n" + "=" * 50)
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
    
    print(f"\nResults saved to: api_test_results.json")

if __name__ == "__main__":
    main()
