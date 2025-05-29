# SEAL (Social Emotional Adaptive Learning)

An AI-powered system that analyzes student performance data and generates targeted intervention plans using advanced language models.

## Overview

SEAL is a REST API service that helps educators create personalized intervention strategies for students based on their emotional intelligence metrics. It uses the Gemini Pro LLM to generate contextually relevant and age-appropriate interventions.

## Features

- **EMT Score Analysis**: Process and analyze Emotional Measurement Task (EMT) scores across four key areas:

  - EMT1: Visual Emotion Matching
  - EMT2: Emotion Description
  - EMT3: Expression Labeling
  - EMT4: Label Matching

- **Intervention Generation**: Creates detailed intervention plans including:

  - Performance analysis
  - Targeted strategies
  - Implementation timelines
  - Success metrics

- **API Features**:
  - JSON schema validation
  - Automatic retries with exponential backoff
  - Health check endpoint
  - Structured logging
  - CORS support

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
   cp .env.example .env
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

### 1. Generate Intervention Plan

```bash
POST /score
```

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

### 2. Health Check

```bash
GET /health
```

## Project Structure

```
seal/
├── app/
│   ├── llm/
│   │   ├── gateway.py        # LLM gateway interface
│   │   └── __init__.py
│   ├── prompts/
│   │   ├── intervention.py   # Prompt templates
│   │   └── __init__.py
│   ├── schemas.py           # Data models
│   ├── main.py             # FastAPI application
│   └── __init__.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

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

- Python 3.x
- All dependencies listed in `requirements.txt`
- Minimum 4GB RAM recommended
- Internet connection for API access

## Future Improvements

1. Add support for real-time data input
2. Implement more sophisticated analysis metrics
3. Add a user interface for easier interaction
4. Expand knowledge base templates

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Student data is organized in batches with:

- Class metadata
- EMT scores
- Deficiency indicators
- Performance metrics
