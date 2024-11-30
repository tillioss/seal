import random
import numpy as np

def generate_emt_scores(num_students=30, base_mean=75, deficient_mean=45, std_dev=10):
    """Generate scores with one EMT area being deficient"""
    normal_scores = np.random.normal(base_mean, std_dev, num_students)
    deficient_scores = np.random.normal(deficient_mean, std_dev, num_students)
    
    # Ensure scores are within 0-100 range
    normal_scores = np.clip(normal_scores, 0, 100)
    deficient_scores = np.clip(deficient_scores, 0, 100)
    
    return normal_scores.round(), deficient_scores.round()

def generate_student_scores(num_classes=4, students_per_class=30):
    batches = []
    
    # Generate 4 classes, each with a different EMT deficiency
    for i in range(num_classes):
        emt1_scores, emt2_scores, emt3_scores, emt4_scores = [], [], [], []
        
        normal_scores, deficient_scores = generate_emt_scores(students_per_class)
        
        # Assign deficient scores to different EMT areas for each class
        if i == 0:  # Class with EMT1 deficiency
            emt1_scores = deficient_scores
            emt2_scores = emt3_scores = emt4_scores = normal_scores
            deficient_area = "EMT1"
        elif i == 1:  # Class with EMT2 deficiency
            emt2_scores = deficient_scores
            emt1_scores = emt3_scores = emt4_scores = normal_scores
            deficient_area = "EMT2"
        elif i == 2:  # Class with EMT3 deficiency
            emt3_scores = deficient_scores
            emt1_scores = emt2_scores = emt4_scores = normal_scores
            deficient_area = "EMT3"
        else:  # Class with EMT4 deficiency
            emt4_scores = deficient_scores
            emt1_scores = emt2_scores = emt3_scores = normal_scores
            deficient_area = "EMT4"
        
        # Calculate overall class average
        all_scores = np.concatenate([emt1_scores, emt2_scores, emt3_scores, emt4_scores])
        class_avg = np.mean(all_scores)
        
        batch = {
            'scores': {
                'EMT1': emt1_scores.tolist(),
                'EMT2': emt2_scores.tolist(),
                'EMT3': emt3_scores.tolist(),
                'EMT4': emt4_scores.tolist(),
            },
            'metadata': {
                'class_id': f'C{i+1}',
                'num_students': students_per_class,
                'deficient_area': deficient_area,
                'class_average': round(class_avg, 2)
            }
        }
        batches.append(batch)
    
    return batches