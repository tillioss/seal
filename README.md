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

## API Endpoints

### POST /score

Generate an intervention plan based on EMT scores.

**Request Body**:

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

### GET /health

Check service health status.

## Quick Start

1. Clone the repository:

```bash
git clone https://github.com/yourusername/seal.git
cd seal
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your Gemini API key
```

5. Run the service:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000` with interactive documentation at `/docs`.

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

## Configuration

The service can be configured using environment variables:

- `GOOGLE_API_KEY`: Your Gemini API key (required)
- `LLM_PROVIDER`: LLM provider to use (default: "gemini")

## Development

For development instructions and deployment guide, see [DEPLOYMENT.md](DEPLOYMENT.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
