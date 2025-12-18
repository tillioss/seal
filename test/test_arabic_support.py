"""Test script to verify Arabic language support with Gemini in SEAL system."""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Add project root to path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class ArabicSupportTester:
    """Test Arabic language support with Gemini."""
    
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-pro')
        self.results = []
        
    def test_1_arabic_understanding(self):
        """Test 1: Basic Arabic text understanding."""
        logger.info("=" * 60)
        logger.info("TEST 1: Basic Arabic Text Understanding")
        logger.info("=" * 60)
        
        arabic_prompt = """
        أنا معلم في مدرسة ابتدائية. لدي فصل من 25 طالباً يعانون من صعوبات في التعرف على المشاعر والتعبير عنها.
        متوسط درجات EMT:
        - EMT1 (مطابقة المشاعر البصرية): 65%
        - EMT2 (ربط الموقف بالتعبير): 58%
        - EMT3 (تسمية التعبيرات): 62%
        - EMT4 (مطابقة التسمية بالتعبير): 60%
        
        ما هي الاستراتيجيات التي يمكنني استخدامها لمساعدة طلابي؟
        """
        
        english_translation = """
        I am a teacher in an elementary school. I have a class of 25 students who have difficulties 
        recognizing and expressing emotions.
        Average EMT scores:
        - EMT1 (Visual Emotion Matching): 65%
        - EMT2 (Situation-to-Expression): 58%
        - EMT3 (Expression Labeling): 62%
        - EMT4 (Label-to-Expression Matching): 60%
        
        What strategies can I use to help my students?
        """
        
        try:
            response = self.model.generate_content(arabic_prompt)
            
            result = {
                "test_name": "Basic Arabic Understanding",
                "input_language": "Arabic",
                "input_text": arabic_prompt,
                "input_translation": english_translation,
                "response": response.text,
                "success": bool(response.text),
                "response_length": len(response.text) if response.text else 0
            }
            
            logger.info(f"✓ Arabic prompt processed successfully")
            logger.info(f"Response length: {result['response_length']} characters")
            logger.info(f"Response preview: {response.text[:200] if response.text else 'No response'}...")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            logger.error(f"✗ Test failed: {str(e)}")
            result = {
                "test_name": "Basic Arabic Understanding",
                "success": False,
                "error": str(e)
            }
            self.results.append(result)
            return result
    
    def test_2_arabic_response_generation(self):
        """Test 2: Request Arabic response generation."""
        logger.info("=" * 60)
        logger.info("TEST 2: Arabic Response Generation")
        logger.info("=" * 60)
        
        prompt = """
        You are an expert Educational Intervention Specialist.
        
        Create an intervention plan in Arabic for a class with the following information:
        - Class ID: الصف_5أ_2024
        - Number of Students: 25
        - Deficient Area: EMT2 (Situation-to-Expression Connection)
        - Average Scores:
          * EMT1: 65%
          * EMT2: 58%
          * EMT3: 62%
          * EMT4: 60%
        
        Please provide a detailed intervention plan in Arabic. Include:
        1. Analysis of the situation
        2. At least 3 specific strategies
        3. Implementation steps
        4. Expected outcomes
        
        Respond in Arabic only.
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            result = {
                "test_name": "Arabic Response Generation",
                "input_language": "English (requesting Arabic output)",
                "output_language": "Arabic",
                "prompt": prompt,
                "response": response.text,
                "success": bool(response.text),
                "response_length": len(response.text) if response.text else 0,
                "contains_arabic": self._contains_arabic(response.text) if response.text else False
            }
            
            logger.info(f"✓ Arabic response generated successfully")
            logger.info(f"Response length: {result['response_length']} characters")
            logger.info(f"Contains Arabic characters: {result['contains_arabic']}")
            logger.info(f"Response preview: {response.text[:300] if response.text else 'No response'}...")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            logger.error(f"✗ Test failed: {str(e)}")
            result = {
                "test_name": "Arabic Response Generation",
                "success": False,
                "error": str(e)
            }
            self.results.append(result)
            return result
    
    def test_3_arabic_json_response(self):
        """Test 3: Arabic content in structured JSON response."""
        logger.info("=" * 60)
        logger.info("TEST 3: Arabic Content in JSON Response")
        logger.info("=" * 60)
        
        # Define schema for intervention plan with Arabic support
        schema = {
            "type": "object",
            "properties": {
                "classId": {"type": "string"},
                "analysis": {"type": "string"},
                "strategies": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "steps": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                }
            }
        }
        
        prompt = """
        Create an intervention plan in Arabic as a JSON object for:
        - Class ID: الصف_5أ_2024
        - Number of Students: 25
        - Deficient Area: EMT2
        
        The JSON should contain:
        - classId: Arabic class identifier
        - analysis: Analysis in Arabic
        - strategies: Array of 3 strategies, each with title, description, and steps in Arabic
        
        Return ONLY valid JSON, no other text.
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=schema
                )
            )
            
            # Parse JSON to verify it's valid
            json_data = json.loads(response.text) if response.text else {}
            
            result = {
                "test_name": "Arabic Content in JSON Response",
                "prompt": prompt,
                "raw_response": response.text,
                "parsed_json": json_data,
                "success": bool(json_data),
                "has_arabic_in_json": self._contains_arabic(response.text) if response.text else False,
                "json_valid": bool(json_data)
            }
            
            logger.info(f"✓ JSON response with Arabic content generated")
            logger.info(f"JSON valid: {result['json_valid']}")
            logger.info(f"Contains Arabic: {result['has_arabic_in_json']}")
            logger.info(f"JSON structure: {json.dumps(json_data, ensure_ascii=False, indent=2)[:500]}...")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            logger.error(f"✗ Test failed: {str(e)}")
            result = {
                "test_name": "Arabic Content in JSON Response",
                "success": False,
                "error": str(e)
            }
            self.results.append(result)
            return result
    
    def test_4_mixed_language(self):
        """Test 4: Mixed English/Arabic input."""
        logger.info("=" * 60)
        logger.info("TEST 4: Mixed Language Input")
        logger.info("=" * 60)
        
        prompt = """
        Create an intervention plan for:
        - Class ID: الصف_5أ_2024 (Class 5A 2024)
        - Number of Students: 25 طالب (students)
        - Deficient Area: EMT2 (Situation-to-Expression Connection)
        
        Provide the response in English but include Arabic translations for key terms.
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            result = {
                "test_name": "Mixed Language Input",
                "prompt": prompt,
                "response": response.text,
                "success": bool(response.text),
                "contains_arabic": self._contains_arabic(response.text) if response.text else False,
                "response_length": len(response.text) if response.text else 0
            }
            
            logger.info(f"✓ Mixed language input processed")
            logger.info(f"Contains Arabic: {result['contains_arabic']}")
            logger.info(f"Response preview: {response.text[:300] if response.text else 'No response'}...")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            logger.error(f"✗ Test failed: {str(e)}")
            result = {
                "test_name": "Mixed Language Input",
                "success": False,
                "error": str(e)
            }
            self.results.append(result)
            return result
    
    def test_5_emt_workflow_arabic(self):
        """Test 5: Full EMT workflow simulation with Arabic."""
        logger.info("=" * 60)
        logger.info("TEST 5: Full EMT Workflow with Arabic")
        logger.info("=" * 60)
        
        # Simulate the actual SEAL workflow but with Arabic
        prompt = """
        You are an expert Educational Intervention Specialist focusing on emotional intelligence development in children.
        
        Create a detailed intervention plan in Arabic for:
        
        CLASS INFORMATION:
        - Class ID: الصف_5أ_2024
        - Number of Students: 25
        - Primary Area Needing Intervention: EMT2
        
        CURRENT PERFORMANCE:
        EMT Score Averages:
        - EMT1 (Visual Emotion Matching): 65.00%
        - EMT2 (Situation-to-Expression): 58.00%
        - EMT3 (Expression Labeling): 62.00%
        - EMT4 (Label-to-Expression): 60.00%
        
        Provide a complete intervention plan in Arabic including:
        1. Analysis of the performance
        2. 3-5 specific strategies
        3. Implementation timeline (4 weeks)
        4. Success metrics
        
        Format as JSON with Arabic content in the values.
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # Try to parse as JSON
            json_data = None
            try:
                json_data = json.loads(response.text)
            except:
                # Try to extract JSON
                start = response.text.find('{')
                end = response.text.rfind('}') + 1
                if start >= 0 and end > start:
                    json_data = json.loads(response.text[start:end])
            
            result = {
                "test_name": "Full EMT Workflow with Arabic",
                "prompt": prompt,
                "response": response.text,
                "parsed_json": json_data,
                "success": bool(response.text),
                "json_valid": bool(json_data),
                "contains_arabic": self._contains_arabic(response.text) if response.text else False
            }
            
            logger.info(f"✓ Full workflow test completed")
            logger.info(f"JSON valid: {result['json_valid']}")
            logger.info(f"Contains Arabic: {result['contains_arabic']}")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            logger.error(f"✗ Test failed: {str(e)}")
            result = {
                "test_name": "Full EMT Workflow with Arabic",
                "success": False,
                "error": str(e)
            }
            self.results.append(result)
            return result
    
    def _contains_arabic(self, text: str) -> bool:
        """Check if text contains Arabic characters."""
        if not text:
            return False
        arabic_range = range(0x0600, 0x06FF)
        return any(ord(char) in arabic_range for char in text)
    
    def run_all_tests(self):
        """Run all Arabic support tests."""
        logger.info("Starting Arabic Language Support Tests")
        logger.info("=" * 60)
        
        self.test_1_arabic_understanding()
        self.test_2_arabic_response_generation()
        self.test_3_arabic_json_response()
        self.test_4_mixed_language()
        self.test_5_emt_workflow_arabic()
        
        return self.results
    
    def save_results(self, output_dir: str = "test/results"):
        """Save test results to files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save detailed JSON results
        json_file = output_path / f"arabic_support_test_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": timestamp,
                "test_summary": {
                    "total_tests": len(self.results),
                    "successful_tests": sum(1 for r in self.results if r.get("success", False)),
                    "failed_tests": sum(1 for r in self.results if not r.get("success", False))
                },
                "results": self.results
            }, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Results saved to: {json_file}")
        return json_file


def main():
    """Main test execution."""
    try:
        tester = ArabicSupportTester()
        results = tester.run_all_tests()
        
        # Print summary
        logger.info("=" * 60)
        logger.info("TEST SUMMARY")
        logger.info("=" * 60)
        
        successful = sum(1 for r in results if r.get("success", False))
        total = len(results)
        
        logger.info(f"Total tests: {total}")
        logger.info(f"Successful: {successful}")
        logger.info(f"Failed: {total - successful}")
        
        for result in results:
            status = "✓" if result.get("success", False) else "✗"
            logger.info(f"{status} {result.get('test_name', 'Unknown test')}")
        
        # Save results
        json_file = tester.save_results()
        logger.info(f"\nDetailed results saved to: {json_file}")
        
        return results
        
    except Exception as e:
        logger.error(f"Test execution failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()

