"""
Manual prompt runner: send JSON inputs directly to the two prompt templates

Usage examples (from repo root, with venv active and .env set with GOOGLE_API_KEY):

  # EMT (Intervention) input from file
  python test/manual_prompt_runner.py emt --input test/quick_test_cases.json --case EMT1_Low_Visual_Recognition

  # Curriculum input from JSON file
  python test/manual_prompt_runner.py curriculum --json '{"grade_level":"2","skill_areas":["emotional_awareness"],"score":65.0}'

Notes:
- Uses models/gemini-2.5-pro
- Prints raw model text; no schema enforcement to avoid compatibility issues
"""

import os
import json
import argparse
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
import google.generativeai as genai

from app.prompts.intervention import InterventionPrompt
from app.prompts.curriculum import CurriculumPrompt


def _load_env_and_model(model_name: str = "models/gemini-2.5-pro"):
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY missing in environment/.env")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)


def _read_json_arg(json_arg: str) -> Dict[str, Any]:
    # If it's a path to a file, load it; otherwise parse as JSON string
    p = Path(json_arg)
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return json.loads(json_arg)


def run_emt(model):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--json", dest="json_str", type=str, default=None)
    parser.add_argument("--input", dest="input_path", type=str, default=None,
                        help="File containing an object with 'scores' and 'metadata' or quick_test_cases.json")
    parser.add_argument("--case", dest="case_name", type=str, default=None,
                        help="If using quick_test_cases.json, the case name to pick")
    args, _ = parser.parse_known_args()

    if not args.json_str and not args.input_path:
        raise SystemExit("Provide --json or --input")

    if args.input_path:
        data = _read_json_arg(args.input_path)
        # quick_test_cases.json structure
        if "emt_cases" in data:
            if not args.case_name:
                raise SystemExit("--case required when using quick_test_cases.json")
            case = next((c for c in data["emt_cases"] if c.get("name") == args.case_name), None)
            if not case:
                raise SystemExit(f"Case '{args.case_name}' not found in {args.input_path}")
            payload = case["input"]
        else:
            payload = data
    else:
        payload = _read_json_arg(args.json_str)

    # Build prompt data expected by InterventionPrompt
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
    print(resp.text or "")


def run_curriculum(model):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--json", dest="json_str", type=str, required=True,
                        help='JSON string or path with keys: grade_level, skill_areas, score')
    args, _ = parser.parse_known_args()

    payload = _read_json_arg(args.json_str)
    prompt_data = {
        "grade_level": payload["grade_level"],
        "skill_areas": payload["skill_areas"],
        "score": payload["score"],
    }

    prompt = CurriculumPrompt.get_prompt("gemini", prompt_data)

    resp = model.generate_content([{ "text": prompt }])
    print(resp.text or "")


def main():
    parser = argparse.ArgumentParser(description="Manual prompt runner for SEAL")
    parser.add_argument("mode", choices=["emt", "curriculum"], help="Which prompt to run")
    args, _ = parser.parse_known_args()

    model = _load_env_and_model("models/gemini-2.5-pro")

    if args.mode == "emt":
        run_emt(model)
    else:
        run_curriculum(model)


if __name__ == "__main__":
    main()


