
# SEAL Prompt Experimentation Guide

## Overview
This guide helps you experiment with different prompt configurations and analyze their outputs for the SEAL project.

## Quick Start

### 1. Test the API
```bash
# Start the SEAL API server (use port 8001 if 8000 is blocked)
cd /path/to/seal
python -m uvicorn app.main:app --reload --port 8001

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
