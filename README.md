# SEAL (Social Emotional Adaptive Learning)

An AI-powered system that analyzes student performance data and automatically generates targeted intervention plans.

## Overview

This system uses Retrieval-Augmented Generation (RAG) and Large Language Models to analyze student performance metrics and create personalized educational intervention strategies. It processes class-level data, identifies areas of deficiency, and generates specific recommendations based on educational best practices stored in its knowledge base.

## Core Components

### 1. RAG Engine (`models/rag_engine.py`)
- Manages the knowledge base of educational interventions
- Retrieves relevant context for generating interventions
- Handles storage and retrieval of intervention templates

### 2. LLM Interface (`models/llm_interface.py`)
- Interfaces with the Language Model
- Processes prompts and generates intervention plans
- Manages model interactions and responses

### 3. Data Generation (`data/synthetic_data.py`)
- Generates synthetic student performance data
- Creates test scenarios for system validation
- Simulates various educational metrics (EMTs)

### 4. Prompt Generator (`utils/prompt_generator.py`)
- Creates structured prompts for the LLM
- Combines student data with retrieved context
- Ensures consistent prompt formatting

## Workflow

1. **Initialization**
   - System components are initialized
   - Knowledge base is loaded or created if not exists

2. **Data Processing**
   - Student performance data is generated/loaded
   - Data is organized by class and educational metrics

3. **Intervention Generation**
   - System analyzes class performance
   - Retrieves relevant intervention strategies
   - Generates customized intervention plans

4. **Output**
   - Displays class statistics
   - Shows EMT averages
   - Presents detailed intervention plans

## Usage

```
python main.py
```


## Requirements

- Python 3.x
- Required environment variables:
  - `TOKENIZERS_PARALLELISM="false"`

## Error Handling

The system includes comprehensive error handling with:
- Detailed error messages
- Stack trace information for debugging
- Graceful failure handling

## Data Structure

Student data is organized in batches with:
- Class metadata
- EMT scores
- Deficiency indicators
- Performance metrics

## Future Improvements

1. Add support for real-time data input
2. Implement more sophisticated analysis metrics
3. Add a user interface for easier interaction
4. Expand knowledge base templates
