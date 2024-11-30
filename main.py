import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from data.synthetic_data import generate_student_scores
from models.rag_engine import RAGEngine
from utils.prompt_generator import PromptGenerator
from data.templates.intervention_templates import TEMPLATES
from tqdm import tqdm

from models.llm_interface import LLMInterface
def main():
    try:
        print("\n1. Initializing components...")
        rag = RAGEngine()
        llm = LLMInterface()
        
        print("\n2. Setting up knowledge base...")
        if not rag.load_knowledge_base():
            print("Creating new knowledge base...")
            rag.create_knowledge_base(TEMPLATES)
        
        print("\n3. Generating synthetic data...")
        batches = generate_student_scores(num_classes=4)
        
        print("\n4. Generating intervention plans...")
        for batch in batches:
            print(f"\nClass {batch['metadata']['class_id']} (Deficient in {batch['metadata']['deficient_area']}):")
            print("-" * 50)
            
            contexts = rag.get_intervention_context(batch)
            prompt = PromptGenerator.generate_intervention_prompt(batch, contexts)
            intervention = llm.generate(prompt)
            
            print(f"EMT Averages:")
            for emt, scores in batch['scores'].items():
                # Ensure we're working with numbers
                numeric_scores = [float(score) for score in scores]
                avg = sum(numeric_scores) / len(numeric_scores)
                print(f"{emt}: {avg:.2f}")
            print("\nIntervention Plan:")
            print(intervention)
            print("-" * 50)
        
    except Exception as e:
        print(f"Error: {e}")
        # Print more detailed error information
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()