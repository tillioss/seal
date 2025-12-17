"""
Human Evaluation Framework for SEAL
Provides tools for human evaluators to assess prompt outputs
"""

import json
import pandas as pd
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
import random

@dataclass
class HumanEvaluationCriteria:
    """Criteria for human evaluation"""
    educational_appropriateness: int  # 1-5 scale
    age_appropriateness: int  # 1-5 scale
    clarity_and_understandability: int  # 1-5 scale
    practical_implementability: int  # 1-5 scale
    safety_and_positivity: int  # 1-5 scale
    relevance_to_deficiency: int  # 1-5 scale
    overall_quality: int  # 1-5 scale
    comments: str = ""
    would_use_in_classroom: bool = False

@dataclass
class HumanEvaluationResult:
    """Result of human evaluation"""
    evaluator_id: str
    test_case_name: str
    model_response: Dict[str, Any]
    criteria: HumanEvaluationCriteria
    evaluation_timestamp: str
    evaluation_duration_minutes: float

class HumanEvaluationFramework:
    """Framework for conducting human evaluations of SEAL outputs"""
    
    def __init__(self, output_dir: str = "test/human_evaluations"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.evaluations = []
        
    def create_evaluation_interface(self, test_cases: List[Dict[str, Any]], 
                                 model_responses: List[Dict[str, Any]]) -> str:
        """Create an HTML interface for human evaluation"""
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEAL Human Evaluation Interface</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .evaluation-container {{
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .test-case-header {{
            background: #2c3e50;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .response-section {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }}
        .criteria-section {{
            background: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }}
        .rating-scale {{
            display: flex;
            gap: 10px;
            margin: 10px 0;
        }}
        .rating-option {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .rating-option input[type="radio"] {{
            margin: 5px;
        }}
        .rating-option label {{
            font-size: 12px;
            text-align: center;
        }}
        .comments-section {{
            margin: 15px 0;
        }}
        .comments-section textarea {{
            width: 100%;
            height: 100px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        .submit-button {{
            background: #27ae60;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin: 20px 0;
        }}
        .submit-button:hover {{
            background: #229954;
        }}
        .evaluation-summary {{
            background: #d5dbdb;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .hidden {{
            display: none;
        }}
    </style>
</head>
<body>
    <h1>SEAL Human Evaluation Interface</h1>
    <p>Please evaluate the following AI-generated intervention plans for educational appropriateness, safety, and practical utility.</p>
    
    <div id="evaluation-container">
        <!-- Evaluations will be dynamically inserted here -->
    </div>
    
    <div class="evaluation-summary">
        <h3>Evaluation Summary</h3>
        <p>Evaluator ID: <input type="text" id="evaluator-id" placeholder="Enter your evaluator ID" required></p>
        <button class="submit-button" onclick="submitAllEvaluations()">Submit All Evaluations</button>
    </div>

    <script>
        const testCases = {json.dumps(test_cases)};
        const modelResponses = {json.dumps(model_responses)};
        let currentEvaluationIndex = 0;
        let evaluations = [];
        
        function createEvaluationHTML(testCase, modelResponse, index) {{
            return `
            <div class="evaluation-container" id="evaluation-{index}">
                <div class="test-case-header">
                    <h2>Test Case {index + 1}: ${{testCase.name}}</h2>
                    <p><strong>Type:</strong> ${{testCase.test_type.toUpperCase()}}</p>
                    <p><strong>Description:</strong> ${{testCase.description}}</p>
                    <p><strong>Grade Level:</strong> ${{testCase.grade_level || 'N/A'}}</p>
                </div>
                
                <div class="response-section">
                    <h3>AI-Generated Response:</h3>
                    <pre>${{JSON.stringify(modelResponse, null, 2)}}</pre>
                </div>
                
                <div class="criteria-section">
                    <h3>Evaluation Criteria (1 = Poor, 5 = Excellent)</h3>
                    
                    <div class="criteria-item">
                        <label><strong>Educational Appropriateness:</strong> How well does this align with educational best practices?</label>
                        <div class="rating-scale">
                            <div class="rating-option"><input type="radio" name="educational_appropriateness_{index}" value="1" required><label>1<br>Poor</label></div>
                            <div class="rating-option"><input type="radio" name="educational_appropriateness_{index}" value="2"><label>2<br>Fair</label></div>
                            <div class="rating-option"><input type="radio" name="educational_appropriateness_{index}" value="3"><label>3<br>Good</label></div>
                            <div class="rating-option"><input type="radio" name="educational_appropriateness_{index}" value="4"><label>4<br>Very Good</label></div>
                            <div class="rating-option"><input type="radio" name="educational_appropriateness_{index}" value="5"><label>5<br>Excellent</label></div>
                        </div>
                    </div>
                    
                    <div class="criteria-item">
                        <label><strong>Age Appropriateness:</strong> Is this suitable for the target age group?</label>
                        <div class="rating-scale">
                            <div class="rating-option"><input type="radio" name="age_appropriateness_{index}" value="1" required><label>1<br>Poor</label></div>
                            <div class="rating-option"><input type="radio" name="age_appropriateness_{index}" value="2"><label>2<br>Fair</label></div>
                            <div class="rating-option"><input type="radio" name="age_appropriateness_{index}" value="3"><label>3<br>Good</label></div>
                            <div class="rating-option"><input type="radio" name="age_appropriateness_{index}" value="4"><label>4<br>Very Good</label></div>
                            <div class="rating-option"><input type="radio" name="age_appropriateness_{index}" value="5"><label>5<br>Excellent</label></div>
                        </div>
                    </div>
                    
                    <div class="criteria-item">
                        <label><strong>Clarity and Understandability:</strong> How clear and easy to understand is this for teachers?</label>
                        <div class="rating-scale">
                            <div class="rating-option"><input type="radio" name="clarity_and_understandability_{index}" value="1" required><label>1<br>Poor</label></div>
                            <div class="rating-option"><input type="radio" name="clarity_and_understandability_{index}" value="2"><label>2<br>Fair</label></div>
                            <div class="rating-option"><input type="radio" name="clarity_and_understandability_{index}" value="3"><label>3<br>Good</label></div>
                            <div class="rating-option"><input type="radio" name="clarity_and_understandability_{index}" value="4"><label>4<br>Very Good</label></div>
                            <div class="rating-option"><input type="radio" name="clarity_and_understandability_{index}" value="5"><label>5<br>Excellent</label></div>
                        </div>
                    </div>
                    
                    <div class="criteria-item">
                        <label><strong>Practical Implementability:</strong> How practical and implementable is this in a real classroom?</label>
                        <div class="rating-scale">
                            <div class="rating-option"><input type="radio" name="practical_implementability_{index}" value="1" required><label>1<br>Poor</label></div>
                            <div class="rating-option"><input type="radio" name="practical_implementability_{index}" value="2"><label>2<br>Fair</label></div>
                            <div class="rating-option"><input type="radio" name="practical_implementability_{index}" value="3"><label>3<br>Good</label></div>
                            <div class="rating-option"><input type="radio" name="practical_implementability_{index}" value="4"><label>4<br>Very Good</label></div>
                            <div class="rating-option"><input type="radio" name="practical_implementability_{index}" value="5"><label>5<br>Excellent</label></div>
                        </div>
                    </div>
                    
                    <div class="criteria-item">
                        <label><strong>Safety and Positivity:</strong> Is this safe, positive, and appropriate for children?</label>
                        <div class="rating-scale">
                            <div class="rating-option"><input type="radio" name="safety_and_positivity_{index}" value="1" required><label>1<br>Poor</label></div>
                            <div class="rating-option"><input type="radio" name="safety_and_positivity_{index}" value="2"><label>2<br>Fair</label></div>
                            <div class="rating-option"><input type="radio" name="safety_and_positivity_{index}" value="3"><label>3<br>Good</label></div>
                            <div class="rating-option"><input type="radio" name="safety_and_positivity_{index}" value="4"><label>4<br>Very Good</label></div>
                            <div class="rating-option"><input type="radio" name="safety_and_positivity_{index}" value="5"><label>5<br>Excellent</label></div>
                        </div>
                    </div>
                    
                    <div class="criteria-item">
                        <label><strong>Relevance to Deficiency:</strong> How well does this address the identified learning deficiency?</label>
                        <div class="rating-scale">
                            <div class="rating-option"><input type="radio" name="relevance_to_deficiency_{index}" value="1" required><label>1<br>Poor</label></div>
                            <div class="rating-option"><input type="radio" name="relevance_to_deficiency_{index}" value="2"><label>2<br>Fair</label></div>
                            <div class="rating-option"><input type="radio" name="relevance_to_deficiency_{index}" value="3"><label>3<br>Good</label></div>
                            <div class="rating-option"><input type="radio" name="relevance_to_deficiency_{index}" value="4"><label>4<br>Very Good</label></div>
                            <div class="rating-option"><input type="radio" name="relevance_to_deficiency_{index}" value="5"><label>5<br>Excellent</label></div>
                        </div>
                    </div>
                    
                    <div class="criteria-item">
                        <label><strong>Overall Quality:</strong> Overall assessment of this intervention plan</label>
                        <div class="rating-scale">
                            <div class="rating-option"><input type="radio" name="overall_quality_{index}" value="1" required><label>1<br>Poor</label></div>
                            <div class="rating-option"><input type="radio" name="overall_quality_{index}" value="2"><label>2<br>Fair</label></div>
                            <div class="rating-option"><input type="radio" name="overall_quality_{index}" value="3"><label>3<br>Good</label></div>
                            <div class="rating-option"><input type="radio" name="overall_quality_{index}" value="4"><label>4<br>Very Good</label></div>
                            <div class="rating-option"><input type="radio" name="overall_quality_{index}" value="5"><label>5<br>Excellent</label></div>
                        </div>
                    </div>
                    
                    <div class="criteria-item">
                        <label><strong>Would you use this in your classroom?</strong></label>
                        <div>
                            <input type="radio" name="would_use_{index}" value="true" id="would_use_yes_{index}">
                            <label for="would_use_yes_{index}">Yes</label>
                            <input type="radio" name="would_use_{index}" value="false" id="would_use_no_{index}">
                            <label for="would_use_no_{index}">No</label>
                        </div>
                    </div>
                    
                    <div class="comments-section">
                        <label><strong>Additional Comments:</strong></label>
                        <textarea name="comments_{index}" placeholder="Please provide any additional feedback, suggestions, or concerns about this intervention plan..."></textarea>
                    </div>
                </div>
            </div>
            `;
        }}
        
        function loadEvaluations() {{
            const container = document.getElementById('evaluation-container');
            let html = '';
            
            for (let i = 0; i < testCases.length; i++) {{
                html += createEvaluationHTML(testCases[i], modelResponses[i], i);
            }}
            
            container.innerHTML = html;
        }}
        
        function submitAllEvaluations() {{
            const evaluatorId = document.getElementById('evaluator-id').value;
            if (!evaluatorId) {{
                alert('Please enter your evaluator ID');
                return;
            }}
            
            const evaluations = [];
            const timestamp = new Date().toISOString();
            
            for (let i = 0; i < testCases.length; i++) {{
                const evaluation = {{
                    evaluator_id: evaluatorId,
                    test_case_name: testCases[i].name,
                    model_response: modelResponses[i],
                    criteria: {{
                        educational_appropriateness: parseInt(document.querySelector(`input[name="educational_appropriateness_${{i}}"]:checked`)?.value || '0'),
                        age_appropriateness: parseInt(document.querySelector(`input[name="age_appropriateness_${{i}}"]:checked`)?.value || '0'),
                        clarity_and_understandability: parseInt(document.querySelector(`input[name="clarity_and_understandability_${{i}}"]:checked`)?.value || '0'),
                        practical_implementability: parseInt(document.querySelector(`input[name="practical_implementability_${{i}}"]:checked`)?.value || '0'),
                        safety_and_positivity: parseInt(document.querySelector(`input[name="safety_and_positivity_${{i}}"]:checked`)?.value || '0'),
                        relevance_to_deficiency: parseInt(document.querySelector(`input[name="relevance_to_deficiency_${{i}}"]:checked`)?.value || '0'),
                        overall_quality: parseInt(document.querySelector(`input[name="overall_quality_${{i}}"]:checked`)?.value || '0'),
                        would_use_in_classroom: document.querySelector(`input[name="would_use_${{i}}"]:checked`)?.value === 'true',
                        comments: document.querySelector(`textarea[name="comments_${{i}}"]`)?.value || ''
                    }},
                    evaluation_timestamp: timestamp,
                    evaluation_duration_minutes: 0 // Could be calculated if needed
                }};
                
                evaluations.push(evaluation);
            }}
            
            // Save evaluations
            const dataStr = JSON.stringify(evaluations, null, 2);
            const dataBlob = new Blob([dataStr], {{type: 'application/json'}});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `seal_human_evaluation_${{evaluatorId}}_${{timestamp.split('T')[0]}}.json`;
            link.click();
            
            alert('Evaluations saved successfully!');
        }}
        
        // Load evaluations when page loads
        loadEvaluations();
    </script>
</body>
</html>
        """
        
        # Save HTML file
        html_path = self.output_dir / "human_evaluation_interface.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_path)
    
    def load_human_evaluations(self, evaluation_file: str) -> List[HumanEvaluationResult]:
        """Load human evaluation results from file"""
        with open(evaluation_file, 'r') as f:
            data = json.load(f)
        
        evaluations = []
        for item in data:
            evaluation = HumanEvaluationResult(
                evaluator_id=item['evaluator_id'],
                test_case_name=item['test_case_name'],
                model_response=item['model_response'],
                criteria=HumanEvaluationCriteria(**item['criteria']),
                evaluation_timestamp=item['evaluation_timestamp'],
                evaluation_duration_minutes=item.get('evaluation_duration_minutes', 0)
            )
            evaluations.append(evaluation)
        
        return evaluations
    
    def analyze_human_evaluations(self, evaluations: List[HumanEvaluationResult]) -> Dict[str, Any]:
        """Analyze human evaluation results"""
        if not evaluations:
            return {}
        
        # Convert to DataFrame for analysis
        data = []
        for eval_result in evaluations:
            row = {
                'evaluator_id': eval_result.evaluator_id,
                'test_case_name': eval_result.test_case_name,
                'evaluation_timestamp': eval_result.evaluation_timestamp,
                **asdict(eval_result.criteria)
            }
            data.append(row)
        
        df = pd.DataFrame(data)
        
        # Calculate statistics
        analysis = {
            'total_evaluations': len(evaluations),
            'unique_evaluators': df['evaluator_id'].nunique(),
            'average_scores': {
                'educational_appropriateness': df['educational_appropriateness'].mean(),
                'age_appropriateness': df['age_appropriateness'].mean(),
                'clarity_and_understandability': df['clarity_and_understandability'].mean(),
                'practical_implementability': df['practical_implementability'].mean(),
                'safety_and_positivity': df['safety_and_positivity'].mean(),
                'relevance_to_deficiency': df['relevance_to_deficiency'].mean(),
                'overall_quality': df['overall_quality'].mean()
            },
            'would_use_percentage': (df['would_use_in_classroom'].sum() / len(df)) * 100,
            'score_distributions': {},
            'evaluator_agreement': self._calculate_evaluator_agreement(df)
        }
        
        # Calculate score distributions
        for criterion in ['educational_appropriateness', 'age_appropriateness', 'clarity_and_understandability',
                         'practical_implementability', 'safety_and_positivity', 'relevance_to_deficiency', 'overall_quality']:
            analysis['score_distributions'][criterion] = df[criterion].value_counts().sort_index().to_dict()
        
        return analysis
    
    def _calculate_evaluator_agreement(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate inter-evaluator agreement"""
        if df['evaluator_id'].nunique() < 2:
            return {'agreement_score': 0.0, 'message': 'Need at least 2 evaluators for agreement analysis'}
        
        # Group by test case and calculate agreement
        agreement_scores = []
        for test_case in df['test_case_name'].unique():
            test_case_data = df[df['test_case_name'] == test_case]
            if len(test_case_data) > 1:
                # Calculate correlation between evaluators for this test case
                numeric_cols = ['educational_appropriateness', 'age_appropriateness', 'clarity_and_understandability',
                               'practical_implementability', 'safety_and_positivity', 'relevance_to_deficiency', 'overall_quality']
                corr_matrix = test_case_data[numeric_cols].corr()
                # Average correlation (excluding diagonal)
                avg_corr = corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].mean()
                agreement_scores.append(avg_corr)
        
        return {
            'agreement_score': np.mean(agreement_scores) if agreement_scores else 0.0,
            'message': f'Average correlation across {len(agreement_scores)} test cases'
        }
    
    def generate_human_evaluation_report(self, evaluations: List[HumanEvaluationResult], 
                                       output_file: str = None) -> str:
        """Generate comprehensive human evaluation report"""
        analysis = self.analyze_human_evaluations(evaluations)
        
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"human_evaluation_report_{timestamp}.json"
        
        # Save analysis
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
        
        # Print summary
        print("HUMAN EVALUATION ANALYSIS")
        print("=" * 50)
        print(f"Total Evaluations: {analysis['total_evaluations']}")
        print(f"Unique Evaluators: {analysis['unique_evaluators']}")
        print(f"Would Use in Classroom: {analysis['would_use_percentage']:.1f}%")
        print("\nAverage Scores:")
        for criterion, score in analysis['average_scores'].items():
            print(f"  {criterion.replace('_', ' ').title()}: {score:.2f}/5")
        
        print(f"\nReport saved to: {output_file}")
        return str(output_file)

def main():
    """Example usage of human evaluation framework"""
    framework = HumanEvaluationFramework()
    
    # Example test cases and responses
    test_cases = [
        {
            "name": "EMT1_Test_Case",
            "test_type": "emt",
            "description": "Test case for visual emotion recognition",
            "grade_level": "2"
        }
    ]
    
    model_responses = [
        {
            "analysis": "Sample analysis",
            "strategies": [{"activity": "Sample activity"}],
            "timeline": {"week1": ["Activity 1"]},
            "success_metrics": {"quantitative": ["50% improvement"]}
        }
    ]
    
    # Create evaluation interface
    interface_path = framework.create_evaluation_interface(test_cases, model_responses)
    print(f"Human evaluation interface created: {interface_path}")

if __name__ == "__main__":
    main()
