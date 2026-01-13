"""
Batch prompt runner: runs all EMT and curriculum cases from quick_test_cases.json
using models/gemini-2.5-pro and saves results to CSV.

Usage (from repo root, venv active):
  python test/batch_prompt_runner.py --input test/quick_test_cases.json --out results_batch.csv
"""

import os
import json
import argparse
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

from app.prompts.intervention import InterventionPrompt
from app.prompts.curriculum import CurriculumPrompt


def load_model(model_name: str = "models/gemini-2.5-pro"):
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY missing in environment/.env")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)


def run_emt_case(model, case: Dict[str, Any]) -> Dict[str, Any]:
    payload = case["input"]
    scores = payload["scores"]
    meta = payload["metadata"]
    prompt_data = {
        "class_id": meta["class_id"],
        "num_students": meta["num_students"],
        "deficient_area": meta["deficient_area"],
        "emt1_avg": sum(scores["EMT1"]) / max(1, len(scores["EMT1"])),
        "emt2_avg": sum(scores["EMT2"]) / max(1, len(scores["EMT2"])),
        "emt3_avg": sum(scores["EMT3"]) / max(1, len(scores["EMT3"])),
        "emt4_avg": sum(scores["EMT4"]) / max(1, len(scores["EMT4"]))
    }
    prompt = InterventionPrompt.get_prompt("gemini", prompt_data)
    resp = model.generate_content([
        {"text": "You are an expert Educational Intervention Specialist. Return ONLY valid JSON."},
        {"text": prompt},
    ])
    text = resp.text or ""
    return {
        "type": "emt",
        "name": case.get("name", ""),
        "description": case.get("description", ""),
        "input": json.dumps(payload, ensure_ascii=False),
        "raw_response": text
    }


def run_curriculum_case(model, case: Dict[str, Any]) -> Dict[str, Any]:
    payload = case["input"]
    prompt_data = {
        "grade_level": payload["grade_level"],
        "skill_areas": payload["skill_areas"],
        "score": payload["score"],
    }
    prompt = CurriculumPrompt.get_prompt("gemini", prompt_data)
    resp = model.generate_content([{ "text": prompt }])
    text = resp.text or ""
    return {
        "type": "curriculum",
        "name": case.get("name", ""),
        "description": case.get("description", ""),
        "input": json.dumps(payload, ensure_ascii=False),
        "raw_response": text
    }


def main():
    parser = argparse.ArgumentParser(description="Batch run SEAL prompts and save CSV")
    parser.add_argument("--input", required=True, help="Path to quick_test_cases.json")
    parser.add_argument("--out", default=None, help="Output CSV path (optional)")
    args = parser.parse_args()

    cases = json.load(open(args.input, "r", encoding="utf-8"))
    model = load_model("models/gemini-2.5-pro")

    results: List[Dict[str, Any]] = []

    for case in cases.get("emt_cases", []):
        try:
            results.append(run_emt_case(model, case))
        except Exception as e:
            results.append({
                "type": "emt",
                "name": case.get("name", ""),
                "description": case.get("description", ""),
                "input": json.dumps(case.get("input", {}), ensure_ascii=False),
                "raw_response": f"ERROR: {e}"
            })

    for case in cases.get("curriculum_cases", []):
        try:
            results.append(run_curriculum_case(model, case))
        except Exception as e:
            results.append({
                "type": "curriculum",
                "name": case.get("name", ""),
                "description": case.get("description", ""),
                "input": json.dumps(case.get("input", {}), ensure_ascii=False),
                "raw_response": f"ERROR: {e}"
            })

    df = pd.DataFrame(results, columns=["type", "name", "description", "input", "raw_response"])

    out_csv = args.out or f"test/results/batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    Path(Path(out_csv).parent).mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)

    print(f"Saved {len(df)} rows to {out_csv}")


if __name__ == "__main__":
    main()


