from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re

class LLMInterface:
    def __init__(self, model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):  # Much smaller model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )

    def generate(self, prompt, max_length=2048):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        outputs = self.model.generate(
            **inputs,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.3,
            max_new_tokens=max_length,
            min_new_tokens=100,
            num_return_sequences=1,
            pad_token_id=self.tokenizer.eos_token_id,
            eos_token_id=self.tokenizer.eos_token_id
        )
        
        # Get the full response
        full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the assistant's response
        # Look for the last <|assistant|> tag and take everything after it
        if "<|assistant|>" in full_response:
            response = full_response.split("<|assistant|>")[-1].strip()
        else:
            # If no tag found, remove the prompt from the beginning
            response = full_response[len(prompt):].strip()
        
        # Clean up any remaining system or user prompts
        response = re.sub(r'<\|system\|>.*?<\|user\|>', '', response, flags=re.DOTALL)
        response = re.sub(r'<\|user\|>.*?<\|assistant\|>', '', response, flags=re.DOTALL)
        
        return response.strip()