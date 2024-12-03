from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time
import pandas as pd
import os
import json
from datetime import datetime

import os
import sys
from pathlib import Path

# Add the project root to the Python path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from data.templates.intervention_templates import TEMPLATES

# Set environment variable for tokenizer
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def create_enhanced_prompt(test_case: str, templates: list) -> str:
    """Create a prompt that includes context from templates"""
    template_context = "\nReference Activities from EMT Templates:\n"
    for template in templates:
        template_context += f"\n{template['type'].upper()}:\n"
        template_context += f"{template['content'].strip()}\n"
    
    prompt = f"""
Based on the following case and EMT activity templates, create a detailed intervention plan:

CASE:
{test_case}

{template_context}

Please provide 5 specific, actionable intervention strategies that incorporate relevant EMT activities.
For each strategy, include:
1. Which EMT activities are being utilized
2. How to implement the strategy
3. Expected outcomes

Format your response as a clear, numbered list.
"""
    return prompt

def save_results(results: list, base_filename: str = "model_comparison"):
    """Save results to files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save detailed results as JSON
    detailed_results = {
        "timestamp": timestamp,
        "results": [{
            "model": r["model"],
            "latency": r["latency"],
            "total_tokens": r["total_tokens"],
            "full_response": r["response"]
        } for r in results]
    }
    
    json_path = f"test/results/{base_filename}_{timestamp}.json"
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, "w") as f:
        json.dump(detailed_results, f, indent=2)
    
    # Save metrics as CSV
    df = pd.DataFrame(results)[["model", "latency", "total_tokens"]]
    csv_path = f"test/results/{base_filename}_{timestamp}.csv"
    df.to_csv(csv_path, index=False)
    
    print(f"\nResults saved to:")
    print(f"Detailed results: {json_path}")
    print(f"Metrics: {csv_path}")

def test_single_model(model_name: str, test_prompt: str):
    """Test a single model and return results"""
    print(f"\n{'='*50}")
    print(f"Testing {model_name}")
    print(f"{'='*50}")
    
    try:
        torch.cuda.empty_cache()
        
        print("Loading model and tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Fix for missing pad token
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            low_cpu_mem_usage=True
        )
        
        print("Generating response...")
        start_time = time.time()
        
        inputs = tokenizer(
            test_prompt, 
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                attention_mask=inputs.attention_mask,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                num_return_sequences=1
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        if response.startswith(test_prompt):
            response = response[len(test_prompt):].strip()
            
        latency = time.time() - start_time
        
        input_tokens = len(inputs.input_ids[0])
        output_tokens = len(outputs[0])
        
        del model
        del tokenizer
        torch.cuda.empty_cache()
        
        return {
            "model": model_name,
            "latency": f"{latency:.2f}s",
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "response": response
        }
        
    except Exception as e:
        print(f"Error testing {model_name}: {str(e)}")
        return None

def main():
    test_case = """
                Given a class of 25 students showing difficulties in emotional recognition and expression:
                - Average EMT scores:
                    * EMT1 (Visual Emotion Matching): 65%
                    * EMT2 (Emotion Description): 58%
                    * EMT3 (Expression Labeling): 62%
                    * EMT4 (Label Matching): 60%
                - Main challenges: 
                    * Difficulty recognizing subtle emotional expressions
                    * Limited emotional vocabulary
                    * Struggles with matching verbal descriptions to expressions
                - Age group: 8-10 years
               """
    
    # Create enhanced prompt with templates
    full_prompt = create_enhanced_prompt(test_case, TEMPLATES)
    
    models = [ # This one worked before
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "sshleifer/tiny-gpt2",                      # Known to be stable
        "facebook/opt-125m"                    # Simple but reliable
    ]
    
    results = []
    for model_name in models:
        result = test_single_model(model_name, full_prompt)
        if result:
            results.append(result)
            
            print("\nResults for this model:")
            print(f"Latency: {result['latency']}")
            print(f"Total tokens: {result['total_tokens']}")
            print("\nResponse:")
            print("-" * 50)
            print(result['response'])
            print("-" * 50)
            print("\nWaiting 5 seconds before next model...")
            time.sleep(5)
    
    if results:
        print("\n\nFinal Comparison:")
        df = pd.DataFrame(results)
        print("\nPerformance Metrics:")
        print(df[["model", "latency", "total_tokens"]])
        
        print("\nDetailed Responses:")
        for result in results:
            print(f"\n{result['model']}:")
            print("-" * 50)
            print(result['response'])
            print("-" * 50)
        
        # Save all results
        save_results(results)

if __name__ == "__main__":
    main()

