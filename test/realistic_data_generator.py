"""
Realistic Test Data Generator for SEAL
Generates realistic EMT scores and curriculum data for testing
"""

import random
import json
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from pathlib import Path
import numpy as np

@dataclass
class ClassProfile:
    """Represents a realistic class profile"""
    class_id: str
    grade_level: str
    num_students: int
    emt_scores: Dict[str, List[float]]
    curriculum_score: float
    skill_areas: List[str]
    characteristics: Dict[str, Any]

class RealisticDataGenerator:
    """Generates realistic test data based on educational research patterns"""
    
    def __init__(self):
        # Realistic EMT score patterns based on educational research
        self.emt_patterns = {
            "high_performing": {
                "EMT1": (75, 90),  # Visual recognition - typically higher
                "EMT2": (70, 85),  # Situation-expression - moderate
                "EMT3": (65, 80),  # Vocabulary - can be challenging
                "EMT4": (60, 75)   # Label comprehension - often lowest
            },
            "average_performing": {
                "EMT1": (60, 75),
                "EMT2": (55, 70),
                "EMT3": (50, 65),
                "EMT4": (45, 60)
            },
            "struggling": {
                "EMT1": (40, 60),
                "EMT2": (35, 55),
                "EMT3": (30, 50),
                "EMT4": (25, 45)
            },
            "mixed_abilities": {
                "EMT1": (45, 85),  # Wide range
                "EMT2": (40, 80),
                "EMT3": (35, 75),
                "EMT4": (30, 70)
            }
        }
        
        # Grade-specific characteristics
        self.grade_characteristics = {
            "1": {
                "typical_emt_range": (40, 80),
                "common_challenges": ["basic_emotion_recognition", "vocabulary_development"],
                "skill_areas": ["emotional_awareness"],
                "class_size_range": (15, 25)
            },
            "2": {
                "typical_emt_range": (50, 85),
                "common_challenges": ["situation_understanding", "emotional_regulation"],
                "skill_areas": ["emotional_awareness", "emotional_regulation"],
                "class_size_range": (18, 28)
            },
            "5": {
                "typical_emt_range": (60, 90),
                "common_challenges": ["complex_emotions", "anger_management"],
                "skill_areas": ["emotional_awareness", "emotional_regulation", "anger_management"],
                "class_size_range": (20, 30)
            }
        }
    
    def generate_emt_scores(self, pattern: str, num_students: int, deficient_area: str = None) -> Dict[str, List[float]]:
        """Generate realistic EMT scores for a class"""
        if pattern not in self.emt_patterns:
            pattern = "average_performing"
        
        scores = {}
        base_ranges = self.emt_patterns[pattern].copy()
        
        # If deficient area specified, make it significantly lower
        if deficient_area and deficient_area in base_ranges:
            min_score, max_score = base_ranges[deficient_area]
            base_ranges[deficient_area] = (min_score - 20, max_score - 15)
        
        for emt_area, (min_score, max_score) in base_ranges.items():
            # Generate scores with some correlation between students
            base_ability = random.uniform(0.3, 0.7)  # Student base ability level
            scores[emt_area] = []
            
            for _ in range(num_students):
                # Add individual variation
                individual_factor = random.uniform(0.8, 1.2)
                score = base_ability * (max_score - min_score) + min_score
                score *= individual_factor
                
                # Add some noise
                noise = random.uniform(-5, 5)
                score += noise
                
                # Clamp to realistic range
                score = max(0, min(100, score))
                scores[emt_area].append(round(score, 1))
        
        return scores
    
    def generate_curriculum_score(self, grade_level: str, skill_area: str) -> float:
        """Generate realistic curriculum performance score"""
        grade_info = self.grade_characteristics.get(grade_level, self.grade_characteristics["2"])
        min_score, max_score = grade_info["typical_emt_range"]
        
        # Add some variation based on skill area
        skill_variations = {
            "emotional_awareness": (0, 0),
            "emotional_regulation": (-5, 5),
            "anger_management": (-10, 0)
        }
        
        variation = skill_variations.get(skill_area, (0, 0))
        score = random.uniform(min_score, max_score)
        score += random.uniform(variation[0], variation[1])
        
        return max(0, min(100, round(score, 1)))
    
    def generate_class_profile(self, grade_level: str, pattern: str = None, deficient_area: str = None) -> ClassProfile:
        """Generate a complete realistic class profile"""
        if pattern is None:
            patterns = list(self.emt_patterns.keys())
            pattern = random.choice(patterns)
        
        grade_info = self.grade_characteristics.get(grade_level, self.grade_characteristics["2"])
        num_students = random.randint(*grade_info["class_size_range"])
        
        # Generate class ID
        class_id = f"CLASS_{grade_level}_{random.randint(1, 9)}{chr(65 + random.randint(0, 25))}_{random.randint(2023, 2024)}"
        
        # Generate EMT scores
        emt_scores = self.generate_emt_scores(pattern, num_students, deficient_area)
        
        # Generate curriculum score
        skill_areas = grade_info["skill_areas"]
        if len(skill_areas) > 1:
            primary_skill = random.choice(skill_areas)
        else:
            primary_skill = skill_areas[0]
        
        curriculum_score = self.generate_curriculum_score(grade_level, primary_skill)
        
        # Generate characteristics
        characteristics = {
            "learning_environment": random.choice(["traditional", "progressive", "mixed"]),
            "socioeconomic_diversity": random.choice(["low", "medium", "high"]),
            "special_needs_students": random.randint(0, min(5, num_students // 5)),
            "english_learners": random.randint(0, min(8, num_students // 3)),
            "behavioral_challenges": random.choice(["low", "moderate", "high"]),
            "parent_involvement": random.choice(["low", "medium", "high"])
        }
        
        return ClassProfile(
            class_id=class_id,
            grade_level=grade_level,
            num_students=num_students,
            emt_scores=emt_scores,
            curriculum_score=curriculum_score,
            skill_areas=skill_areas,
            characteristics=characteristics
        )
    
    def generate_test_dataset(self, num_classes_per_grade: int = 5) -> List[ClassProfile]:
        """Generate a comprehensive test dataset"""
        profiles = []
        
        for grade in ["1", "2", "5"]:
            for i in range(num_classes_per_grade):
                # Vary the patterns and deficient areas
                patterns = list(self.emt_patterns.keys())
                pattern = random.choice(patterns)
                
                # Sometimes specify a deficient area
                deficient_area = None
                if random.random() < 0.6:  # 60% chance of having a deficient area
                    deficient_area = random.choice(["EMT1", "EMT2", "EMT3", "EMT4"])
                
                profile = self.generate_class_profile(grade, pattern, deficient_area)
                profiles.append(profile)
        
        return profiles
    
    def create_emt_test_cases(self, profiles: List[ClassProfile]) -> List[Dict[str, Any]]:
        """Convert profiles to EMT test cases"""
        test_cases = []
        
        for profile in profiles:
            # Calculate averages
            emt_averages = {}
            for emt_area, scores in profile.emt_scores.items():
                emt_averages[emt_area] = round(sum(scores) / len(scores), 1)
            
            # Find most deficient area
            deficient_area = min(emt_averages.keys(), key=lambda k: emt_averages[k])
            
            test_case = {
                "name": f"EMT_{profile.grade_level}_{profile.class_id}",
                "input_data": {
                    "scores": profile.emt_scores,
                    "metadata": {
                        "class_id": profile.class_id,
                        "deficient_area": deficient_area,
                        "num_students": profile.num_students
                    }
                },
                "expected_focus_areas": [f"EMT{deficient_area[-1]}", "Emotional Learning"],
                "test_type": "emt",
                "description": f"Grade {profile.grade_level} class with {profile.characteristics['learning_environment']} environment",
                "grade_level": profile.grade_level,
                "characteristics": profile.characteristics
            }
            test_cases.append(test_case)
        
        return test_cases
    
    def create_curriculum_test_cases(self, profiles: List[ClassProfile]) -> List[Dict[str, Any]]:
        """Convert profiles to curriculum test cases"""
        test_cases = []
        
        for profile in profiles:
            # Create multiple test cases per profile for different skill areas
            for skill_area in profile.skill_areas:
                # Generate score variation for this skill area
                base_score = profile.curriculum_score
                variation = random.uniform(-15, 15)
                skill_score = max(0, min(100, base_score + variation))
                
                test_case = {
                    "name": f"CURR_{profile.grade_level}_{skill_area}_{profile.class_id}",
                    "input_data": {
                        "grade_level": profile.grade_level,
                        "skill_areas": [skill_area],
                        "score": round(skill_score, 1)
                    },
                    "expected_focus_areas": [skill_area.replace("_", " ").title()],
                    "test_type": "curriculum",
                    "description": f"Grade {profile.grade_level} {skill_area} intervention",
                    "grade_level": profile.grade_level,
                    "characteristics": profile.characteristics
                }
                test_cases.append(test_case)
        
        return test_cases
    
    def save_test_data(self, profiles: List[ClassProfile], output_dir: str = "test/data"):
        """Save generated test data to files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save profiles
        profiles_data = []
        for profile in profiles:
            profiles_data.append({
                "class_id": profile.class_id,
                "grade_level": profile.grade_level,
                "num_students": profile.num_students,
                "emt_scores": profile.emt_scores,
                "curriculum_score": profile.curriculum_score,
                "skill_areas": profile.skill_areas,
                "characteristics": profile.characteristics
            })
        
        with open(output_path / "realistic_profiles.json", 'w') as f:
            json.dump(profiles_data, f, indent=2)
        
        # Save EMT test cases
        emt_cases = self.create_emt_test_cases(profiles)
        with open(output_path / "emt_test_cases.json", 'w') as f:
            json.dump(emt_cases, f, indent=2)
        
        # Save curriculum test cases
        curriculum_cases = self.create_curriculum_test_cases(profiles)
        with open(output_path / "curriculum_test_cases.json", 'w') as f:
            json.dump(curriculum_cases, f, indent=2)
        
        print(f"Generated {len(profiles)} class profiles")
        print(f"Created {len(emt_cases)} EMT test cases")
        print(f"Created {len(curriculum_cases)} curriculum test cases")
        print(f"Data saved to {output_path}")

def main():
    """Generate realistic test data"""
    generator = RealisticDataGenerator()
    
    # Generate comprehensive dataset
    profiles = generator.generate_test_dataset(num_classes_per_grade=8)
    
    # Save all data
    generator.save_test_data(profiles)
    
    # Print summary
    print("\n" + "="*60)
    print("REALISTIC TEST DATA SUMMARY")
    print("="*60)
    
    grade_counts = {}
    pattern_counts = {}
    
    for profile in profiles:
        grade_counts[profile.grade_level] = grade_counts.get(profile.grade_level, 0) + 1
        
        # Determine pattern based on average scores
        avg_scores = [sum(scores) / len(scores) for scores in profile.emt_scores.values()]
        overall_avg = sum(avg_scores) / len(avg_scores)
        
        if overall_avg >= 70:
            pattern = "high_performing"
        elif overall_avg >= 50:
            pattern = "average_performing"
        else:
            pattern = "struggling"
        
        pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
    
    print("Grade Distribution:")
    for grade, count in sorted(grade_counts.items()):
        print(f"  Grade {grade}: {count} classes")
    
    print("\nPerformance Distribution:")
    for pattern, count in pattern_counts.items():
        print(f"  {pattern.replace('_', ' ').title()}: {count} classes")
    
    print(f"\nTotal Classes: {len(profiles)}")
    print(f"Total Students: {sum(p.num_students for p in profiles)}")

if __name__ == "__main__":
    main()
