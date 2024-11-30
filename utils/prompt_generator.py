class PromptGenerator:
    @staticmethod
    def generate_intervention_prompt(batch, contexts):
        scores = batch['scores']
        metadata = batch['metadata']
        class_id = metadata['class_id']
        deficient_area = metadata['deficient_area']
        
        # Calculate averages for each EMT area - ensure we're working with numbers
        emt_averages = {}
        for emt, score_list in scores.items():
            # Convert any string numbers to float
            numeric_scores = [float(score) for score in score_list]
            emt_averages[emt] = sum(numeric_scores) / len(numeric_scores)
        
        prompt = f"""<|system|>You are an EMT specialist who creates focused intervention plans. Prioritize addressing the most deficient areas.</s>
<|user|>Create an intervention plan for Class {class_id}:

EMT Score Averages:
EMT1 (Visual Matching): {emt_averages['EMT1']:.2f}
EMT2 (Emotion Description): {emt_averages['EMT2']:.2f}
EMT3 (Expression Labeling): {emt_averages['EMT3']:.2f}
EMT4 (Label Matching): {emt_averages['EMT4']:.2f}

Main Area Needing Intervention: {deficient_area}

Available EMT strategies:
{chr(10).join(contexts)}

Format your response as:
1. Analysis (2-3 lines focusing on {deficient_area})
2. Primary Interventions (3-4 specific activities)
3. 4-week Implementation Timeline
4. Success Metrics (2-3 measurable targets)</s>
<|assistant|>"""
        return prompt