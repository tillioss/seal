"""Prompt templates for intervention generation."""

from typing import Dict, Any
import json
from app.schemas import InterventionPlan

class InterventionPrompt:
    """Manages prompt templates for intervention generation."""
    
    # EMT-specific intervention strategies from original assessment tool
    EMT_STRATEGIES = {
        "EMT1": {
            "focus": "Visual Emotion Recognition",
            "description": "Visual-to-visual emotion matching difficulties",
            "strategies": [
                {
                    "activity": "Emotion Flashcard Pairs",
                    "implementation": [
                        "Use emotion flashcard pairs for matching practice",
                        "Start with basic emotions (happy, sad, angry, surprised)",
                        "Progress to more complex emotions (frustrated, excited, worried)",
                        "Practice in pairs and small groups"
                    ],
                    "resources": ["Emotion flashcard sets", "Timer for activities", "Progress tracking sheets"]
                },
                {
                    "activity": "Mirror Expression Practice",
                    "implementation": [
                        "Students practice making facial expressions in mirrors",
                        "Match their expression to emotion cards",
                        "Take turns showing expressions to classmates",
                        "Guess and discuss the emotions shown"
                    ],
                    "resources": ["Hand mirrors", "Emotion reference cards", "Expression practice guide"]
                },
                {
                    "activity": "Digital Emotion Matching Games",
                    "implementation": [
                        "Use tablet/computer games for emotion matching",
                        "Interactive drag-and-drop emotion activities",
                        "Progressive difficulty levels",
                        "Track accuracy and improvement over time"
                    ],
                    "resources": ["Tablets/computers", "Educational emotion apps", "Progress tracking software"]
                }
            ]
        },
        "EMT2": {
            "focus": "Situation-to-Expression Connection",
            "description": "Connecting verbal contexts to visual expressions",
            "strategies": [
                {
                    "activity": "Story-Based Emotion Discussions",
                    "implementation": [
                        "Read short stories with emotional situations",
                        "Discuss how characters might feel",
                        "Match story situations to facial expressions",
                        "Create alternative story endings with different emotions"
                    ],
                    "resources": ["Age-appropriate story books", "Emotion expression cards", "Discussion prompts"]
                },
                {
                    "activity": "Scenario Cards with Emotional Contexts",
                    "implementation": [
                        "Present scenario cards describing emotional situations",
                        "Students select matching facial expressions",
                        "Discuss why certain emotions fit specific situations",
                        "Role-play scenarios with appropriate expressions"
                    ],
                    "resources": ["Scenario cards", "Emotion expression photos", "Role-play props"]
                },
                {
                    "activity": "Role-Playing Emotional Situations",
                    "implementation": [
                        "Act out common emotional scenarios",
                        "Practice showing appropriate facial expressions",
                        "Discuss body language and tone of voice",
                        "Reflect on how situations make us feel"
                    ],
                    "resources": ["Situation prompt cards", "Simple costumes/props", "Reflection journals"]
                }
            ]
        },
        "EMT3": {
            "focus": "Emotion Vocabulary Building",
            "description": "Visual to verbal emotion labeling difficulties",
            "strategies": [
                {
                    "activity": "Emotion Word Wall",
                    "implementation": [
                        "Create classroom emotion vocabulary display",
                        "Add new emotion words weekly",
                        "Practice using emotion words in sentences",
                        "Connect words to facial expressions and situations"
                    ],
                    "resources": ["Word wall materials", "Emotion vocabulary cards", "Sentence strips"]
                },
                {
                    "activity": "Expression-Label Matching Games",
                    "implementation": [
                        "Match emotion words to facial expressions",
                        "Use memory games with emotion vocabulary",
                        "Practice spelling and defining emotion words",
                        "Create emotion word puzzles and activities"
                    ],
                    "resources": ["Emotion word cards", "Expression photos", "Memory game materials", "Puzzles"]
                },
                {
                    "activity": "Emotion Vocabulary Journals",
                    "implementation": [
                        "Students keep daily emotion journals",
                        "Write about feelings using new vocabulary",
                        "Draw pictures to match emotion words",
                        "Share journal entries in small groups"
                    ],
                    "resources": ["Individual journals", "Emotion word reference sheets", "Drawing materials"]
                }
            ]
        },
        "EMT4": {
            "focus": "Emotion Label Comprehension",
            "description": "Verbal label to visual expression matching difficulties",
            "strategies": [
                {
                    "activity": "Emotion Word-to-Face Games",
                    "implementation": [
                        "Call out emotion words, students show expressions",
                        "Use emotion word bingo with facial expressions",
                        "Practice quick word-to-expression responses",
                        "Play emotion charades with word prompts"
                    ],
                    "resources": ["Emotion word cards", "Bingo cards with expressions", "Timer", "Charades prompts"]
                },
                {
                    "activity": "Verbal Emotion Cues Practice",
                    "implementation": [
                        "Listen to emotion words and respond with expressions",
                        "Practice with audio recordings of emotion words",
                        "Use verbal descriptions to guide expression making",
                        "Develop quick recognition of emotion vocabulary"
                    ],
                    "resources": ["Audio recordings", "Headphones", "Emotion word lists", "Response cards"]
                },
                {
                    "activity": "Group Emotion Word Activities",
                    "implementation": [
                        "Team-based emotion word competitions",
                        "Collaborative emotion word sorting activities",
                        "Group discussions about emotion word meanings",
                        "Peer teaching of emotion vocabulary"
                    ],
                    "resources": ["Team activity materials", "Sorting cards", "Competition scorecards", "Group work guidelines"]
                }
            ]
        }
    }
    
    EXAMPLE_RESPONSE = {
        "analysis": "The class shows significant deficiency in EMT3 (Expression Labeling) with an average score of 65%, indicating difficulties in labeling emotional expressions accurately.",
        "strategies": [
            {
                "activity": "Emotion Word Wall",
                "implementation": [
                    "Create classroom emotion vocabulary display",
                    "Add new emotion words weekly",
                    "Practice using emotion words in sentences",
                    "Connect words to facial expressions and situations"
                ],
                "expected_outcomes": [
                    "Expanded emotion vocabulary",
                    "Improved expression labeling accuracy",
                    "Better emotional communication skills"
                ],
                "time_allocation": "20 minutes daily",
                "resources": [
                    "Word wall materials",
                    "Emotion vocabulary cards",
                    "Sentence strips"
                ]
            }
        ],
        "timeline": {
            "week1": ["Set up emotion word wall", "Introduce basic emotion vocabulary"],
            "week2": ["Add complex emotions", "Practice word-expression connections"],
            "week3": ["Group vocabulary activities", "Peer teaching sessions"],
            "week4": ["Assessment activities", "Vocabulary reinforcement games"]
        },
        "success_metrics": {
            "quantitative": ["15% improvement in EMT3 scores", "90% vocabulary retention rate"],
            "qualitative": ["Increased confidence in emotion labeling", "Better use of emotion vocabulary"],
            "assessment_methods": ["Weekly vocabulary assessments", "Expression labeling tests", "Peer feedback"]
        }
    }
    
    BASE_TEMPLATE = """You are an expert Educational Intervention Specialist focusing on emotional intelligence development in children.

TASK: Create a detailed intervention plan for a class showing difficulties in emotional recognition and expression.

SAFETY GUIDELINES - CRITICAL:
- Use ONLY positive, encouraging, and age-appropriate language
- Focus on growth, learning, and development opportunities
- Avoid any negative, harmful, or inappropriate content
- Use simple language that children can understand
- Ensure all activities are safe and suitable for the classroom
- Promote inclusivity and respect for all students

CLASS INFORMATION:
- Class ID: {class_id}
- Number of Students: {num_students}
- Primary Area Needing Intervention: {deficient_area}

CURRENT PERFORMANCE:
EMT Score Averages:
- EMT1 (Visual Emotion Matching): {emt1_avg:.2f}%
- EMT2 (Situation-to-Expression): {emt2_avg:.2f}%
- EMT3 (Expression Labeling): {emt3_avg:.2f}%
- EMT4 (Label-to-Expression): {emt4_avg:.2f}%

EMT-SPECIFIC INTERVENTION STRATEGIES:

EMT1 - Visual Emotion Recognition (Visual-to-visual matching):
Focus: Visual Emotion Recognition
Proven Strategies:
- Emotion flashcard pairs for matching practice
- Mirror expression practice with emotion cards
- Digital emotion matching games with progressive difficulty
- Pattern recognition activities with facial expressions

EMT2 - Situation-to-Expression Connection (Verbal context to visual expression):
Focus: Contextual Understanding
Proven Strategies:
- Story-based emotion discussions with character analysis
- Scenario cards with emotional contexts for matching
- Role-playing emotional situations with expression practice
- Situational emotion analysis activities

EMT3 - Expression Labeling (Visual to verbal labeling):
Focus: Emotion Vocabulary Building
Proven Strategies:
- Emotion word wall development and daily practice
- Expression-label matching games and activities
- Emotion vocabulary journals with daily entries
- Vocabulary building through visual-verbal connections

EMT4 - Label-to-Expression Matching (Verbal label to visual expression):
Focus: Emotion Label Comprehension
Proven Strategies:
- Emotion word-to-face games and quick responses
- Verbal emotion cues practice with audio support
- Group emotion word activities and competitions
- Label comprehension through interactive exercises

INSTRUCTIONS:
1. Focus primarily on the deficient area ({deficient_area}) using the proven strategies above
2. Select 3-5 specific activities from the relevant EMT strategy set
3. Adapt activities to be age-appropriate and engaging
4. Include supporting activities from other EMT areas to maintain overall development
5. Create a 4-week progressive implementation timeline
6. Provide measurable success metrics specific to the deficient area

Your response MUST be a valid JSON object matching this schema EXACTLY:
{schema}

Here's an example of a valid response structure (adapt content to the current situation):
{example}

IMPORTANT REQUIREMENTS:
1. Return ONLY the JSON object, no other text
2. Ensure the JSON structure matches the schema exactly
3. Include at least 3 strategies (maximum 5)
4. Make all strategies specific to the deficient area ({deficient_area})
5. Use the proven EMT-specific strategies provided above
6. Include a 4-week timeline with progressive activities
7. Provide measurable success metrics
8. Double-check that your response is valid JSON
9. ENSURE ALL CONTENT IS POSITIVE, SAFE, AND AGE-APPROPRIATE

Focus on creating specific, actionable strategies that address the deficient area while maintaining development in other areas. All content must be suitable for teachers to use with children in educational settings."""

    GEMINI_TEMPLATE = BASE_TEMPLATE + """
FINAL CHECK:
1. Your response must start with an opening curly brace
2. Your response must end with a closing curly brace
3. Use double quotes for all strings
4. No trailing commas
5. No comments or additional text"""

    OPENAI_TEMPLATE = BASE_TEMPLATE + """
Note: Format your response as a JSON object without any additional text or explanation."""

    @classmethod
    def get_prompt(cls, provider: str, data: Dict[str, Any]) -> str:
        """Get formatted prompt for specified provider.
        
        Args:
            provider: LLM provider name ('gemini', 'openai', etc.)
            data: Dictionary containing template variables
            
        Returns:
            Formatted prompt string
        """
        # Add schema and example to data
        data['schema'] = json.dumps(InterventionPlan.model_json_schema(), indent=2)
        data['example'] = json.dumps(cls.EXAMPLE_RESPONSE, indent=2)
        
        # Select template based on provider
        template = {
            'gemini': cls.GEMINI_TEMPLATE,
            'openai': cls.OPENAI_TEMPLATE
        }.get(provider, cls.BASE_TEMPLATE)

        return template.format(**data)