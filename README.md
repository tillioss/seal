# SEAL (Social Emotional Adaptive Learning)

An AI-powered system that analyzes student performance data and generates targeted intervention plans using advanced language models.

## Overview

SEAL is a REST API service that helps educators create personalized intervention strategies for students based on their emotional intelligence metrics. It uses Google's Gemini AI to generate contextually relevant and age-appropriate interventions through two specialized endpoints:

1. **EMT Score-based Interventions** - Analyzes class performance data to generate targeted intervention plans
2. **Curriculum-based Interventions** - Provides grade-appropriate emotional learning activities based on skill areas and performance scores

## Features

- **EMT Score Analysis**: Process and analyze Emotional Measurement Task (EMT) scores across four key areas:
  - EMT1: Visual Emotion Matching
  - EMT2: Emotion Description
  - EMT3: Expression Labeling
  - EMT4: Label Matching

- **Curriculum Interventions**: Grade-specific emotional learning activities for:
  - Emotional Awareness
  - Emotional Regulation
  - Anger Management
  - Supports grades 1, 2, and 5

- **Intervention Generation**: Creates detailed intervention plans including:
  - Performance analysis
  - Targeted strategies
  - Implementation timelines
  - Success metrics
  - Resource requirements

- **API Features**:
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

### 1. Generate EMT-based Intervention Plan

```bash
POST /score
```

Analyzes class EMT performance data and generates targeted intervention strategies.

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

### 2. Generate Curriculum-based Intervention Plan

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

Returns the health status of both intervention and curriculum services.

## Project Structure

```
seal/
├── app/
│   ├── llm/
│   │   ├── gateway.py              # Base LLM gateway and EMT intervention implementation
│   │   ├── curriculum_gateway.py   # Curriculum-specific intervention implementation
│   │   └── __init__.py
│   ├── prompts/
│   │   ├── intervention.py         # EMT intervention prompt templates
│   │   ├── curriculum.py           # Curriculum intervention prompt templates
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── base.py                 # EMT score and intervention schemas
│   │   ├── curriculum.py           # Curriculum-specific schemas
│   │   └── __init__.py
│   ├── main.py                     # FastAPI application with all endpoints
│   └── __init__.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── example.env                     # Environment configuration template
└── README.md
```

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

Run the test suite:

```bash
pytest
```

## Requirements

- Python 3.8+
- All dependencies listed in `requirements.txt`
- Google API key for Gemini AI
- Minimum 4GB RAM recommended
- Internet connection for API access

## Supported Grade Levels & Skill Areas

### Grade Levels
- Grade 1
- Grade 2  
- Grade 5

### Skill Areas
- **Emotional Awareness**: Understanding and identifying emotions
- **Emotional Regulation**: Managing and controlling emotional responses
- **Anger Management**: Specific strategies for anger control and expression

## Future Improvements

1. Add support for additional grade levels
2. Expand skill areas and intervention types
3. Implement real-time data input capabilities
4. Add a user interface for easier interaction
5. Develop assessment tracking features
6. Add multi-language support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

For questions or support, please open an issue on GitHub.
