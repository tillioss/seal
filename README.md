# SEAL (Social Emotional Adaptive Learning)

An AI-powered system that analyzes student performance data and generates targeted intervention plans using advanced language models with detailed EMT-specific scenarios.

## Overview

SEAL is a REST API service that helps educators create personalized intervention strategies for students based on their emotional intelligence metrics. It uses Google's Gemini AI to generate contextually relevant and age-appropriate interventions through two specialized assessment tools:

1. **EMT Assessment Tool (Q1)** - Analyzes class performance data across four EMT areas with detailed scenario-based interventions
2. **Curriculum Assessment Tool (Q2)** - Provides grade-appropriate emotional learning activities based on skill areas and performance scores

## Features

### EMT Assessment Tool - Detailed Scenario-Based Interventions

Process and analyze Emotional Measurement Task (EMT) scores across four key areas with specific intervention strategies:

- **EMT1: Visual Emotion Matching** (Visual-to-visual matching)
  - Emotion flashcard pairs for matching practice
  - Mirror expression practice with emotion cards
  - Digital emotion matching games with progressive difficulty
  - Pattern recognition activities with facial expressions

- **EMT2: Situation-to-Expression Connection** (Verbal context to visual expression)
  - Story-based emotion discussions with character analysis
  - Scenario cards with emotional contexts for matching
  - Role-playing emotional situations with expression practice
  - Situational emotion analysis activities

- **EMT3: Expression Labeling** (Visual to verbal labeling)
  - Emotion word wall development and daily practice
  - Expression-label matching games and activities
  - Emotion vocabulary journals with daily entries
  - Vocabulary building through visual-verbal connections

- **EMT4: Label-to-Expression Matching** (Verbal label to visual expression)
  - Emotion word-to-face games and quick responses
  - Verbal emotion cues practice with audio support
  - Group emotion word activities and competitions
  - Label comprehension through interactive exercises

### Curriculum Assessment Tool

Grade-specific emotional learning activities for:
- **Emotional Awareness**: Understanding and identifying emotions
- **Emotional Regulation**: Managing and controlling emotional responses  
- **Anger Management**: Specific strategies for anger control and expression
- Supports grades 1, 2, and 5

### Intervention Generation

Creates detailed intervention plans including:
- Performance analysis with EMT-specific focus areas
- Targeted strategies based on proven EMT methodologies
- 4-week progressive implementation timelines
- Measurable success metrics
- Specific resource requirements
- Age-appropriate and classroom-ready activities

### 🛡️ Safety System

Comprehensive content validation to ensure all AI-generated content is appropriate for children:
- Multi-layer safety validation with severity classification
- Child-focused protection against harmful or inappropriate content
- Configurable safety levels for different environments
- Real-time content filtering and violation logging
- See [SAFETY.md](SAFETY.md) for detailed documentation

### API Features

- JSON schema validation
- Automatic retries with exponential backoff
- Health check endpoint
- Structured logging
- CORS support
- Data privacy compliance (aggregated scores only sent to AI)

## Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/seal.git
   cd seal
   ```

2. **Set up a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**

   Copy the example environment file and configure your settings:

   ```bash
   cp example.env .env
   # Edit .env with your configuration
   ```

   Required environment variables:

   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   TOKENIZERS_PARALLELISM=false
   LLM_PROVIDER=gemini  # Optional, defaults to gemini if not set
   ```

5. **Start the API server**

   ```bash
   python -m uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

6. **Access the API documentation**
   - OpenAPI docs: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### 1. EMT Assessment Tool - Generate Intervention Plan

```bash
POST /score
```

Analyzes class EMT performance data and generates targeted intervention strategies using detailed EMT-specific scenarios.

Example request:

```json
{
  "scores": {
    "EMT1": [65.0, 70.0, 68.0],
    "EMT2": [58.0, 62.0, 60.0],
    "EMT3": [72.0, 75.0, 70.0],
    "EMT4": [63.0, 65.0, 64.0]
  },
  "metadata": {
    "class_id": "C1",
    "deficient_area": "EMT2",
    "num_students": 3
  }
}
```

The API will automatically select appropriate intervention strategies from the EMT2 scenario set (Situation-to-Expression Connection) including story-based discussions, scenario cards, and role-playing activities.

### 2. Curriculum Assessment Tool - Generate Learning Plan

```bash
POST /curriculum
```

Provides grade-appropriate emotional learning activities based on skill areas and performance.

Example request:

```json
{
  "grade_level": "2",
  "skill_areas": ["emotional_awareness", "emotional_regulation"],
  "score": 65.5
}
```

### 3. Health Check

```bash
GET /health
```

Returns the health status of both assessment tools and services.

## Project Structure

```
seal/
├── app/
│   ├── llm/
│   │   ├── gateway.py              # EMT assessment tool with detailed scenarios
│   │   ├── curriculum_gateway.py   # Curriculum assessment tool implementation
│   │   └── __init__.py
│   ├── prompts/
│   │   ├── intervention.py         # EMT scenarios and intervention strategies
│   │   ├── curriculum.py           # Curriculum intervention templates
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── base.py                 # EMT score and intervention schemas
│   │   ├── curriculum.py           # Curriculum-specific schemas
│   │   └── __init__.py
│   ├── safety/
│   │   ├── guardrails.py           # Content safety validation
│   │   └── __init__.py
│   ├── main.py                     # FastAPI application with both assessment tools
│   └── __init__.py
├── data/
│   └── synthetic_data.py           # EMT test data generation
├── test/
│   ├── compare_llms.py             # Model comparison testing
│   └── results/                    # Test results storage
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── example.env                     # Environment configuration template
├── SAFETY.md                       # Safety system documentation
├── DEPLOYMENT.md                   # Deployment instructions
└── README.md
```

## Assessment Tool Details

### EMT Assessment Tool (Q1 Implementation)

The EMT Assessment Tool processes emotional measurement task scores and generates intervention plans using detailed, scenario-based strategies. Each EMT area has specific proven interventions:

- **Comprehensive scenario library** with 3+ detailed strategies per EMT area
- **Progressive difficulty levels** from basic to complex emotions
- **Multi-modal approaches** including visual, verbal, and interactive components
- **Classroom-ready activities** with specific resource requirements
- **Measurable outcomes** with quantitative and qualitative metrics

### Curriculum Assessment Tool (Q2 Implementation)

The Curriculum Assessment Tool provides grade-specific interventions across three skill areas:

- **10 predefined interventions** covering emotional awareness, regulation, and anger management
- **Grade-appropriate activities** for grades 1, 2, and 5
- **Structured implementation plans** with clear steps and timelines
- **Developmental considerations** matching cognitive and emotional capabilities

## Data Privacy

SEAL is designed with data privacy in mind:

- **Individual student scores** are accepted by the API but **never sent to the AI model**
- Only **aggregated class averages** are included in prompts sent to the LLM
- No personally identifiable information is processed or stored
- All AI interactions use anonymized, class-level data only

## Docker Support

1. **Build the image**

   ```bash
   docker build -t seal .
   ```

2. **Run the container**

   ```bash
   docker-compose up
   ```

## Testing

Run the model comparison tests to evaluate different LLM performance:

```bash
python test/compare_llms.py
```

Results are saved in `test/results/` with detailed performance metrics and response quality analysis.

## Future Improvements

1. Add support for additional grade levels
2. Expand EMT scenario library with more detailed interventions
3. Implement real-time assessment data input capabilities
4. Add a user interface for easier interaction with both assessment tools
5. Develop progress tracking and outcome measurement features
6. Add multi-language support for diverse classrooms

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

For questions or support, please open an issue on GitHub.
