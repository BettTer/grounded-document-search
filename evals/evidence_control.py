import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "evals" / "runs"

CASE_ID = "revive-properly-summoned-link"
OMITTED_ID = "ecclesia-extra-deck-lock"
OLLAMA = "http://127.0.0.1:11434"


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def live_inputs():
    sys.path.insert(0, str(ROOT))
    from grounded_search.index import read_evidence

    cases = json.loads((ROOT / "evals/yugioh-smoke.json").read_text(encoding="utf-8"))
    case = next(row for row in cases if row["case_id"] == CASE_ID)
    question = case["question"]["en"]
    result = subprocess.check_output(
        [sys.executable, "-m", "grounded_search", "search", question, "--corpus", "yugioh", "--k", "5"],
        cwd=ROOT, text=True,
    )
    hits = json.loads(result)
    evidence = {row[1]: row[4] for row in read_evidence("yugioh")}
    complete = {key: evidence[key] for key in case["expected_evidence_ids"]}
    groups = {
        "A": {hit["evidence_id"]: hit["body"] for hit in hits},
        "B": complete,
        "C": {key: body for key, body in complete.items() if key != OMITTED_ID},
    }

    instruction = (
        "Answer using only the evidence below. Cite the supporting evidence IDs for each "
        "conclusion. If evidence is incomplete, state what it supports and what is missing."
    )
    prompts = {}
    for group, rows in groups.items():
        passages = "\n\n".join(f"[{key}]\n{body}" for key, body in rows.items())
        prompts[group] = f"{instruction}\n\nQuestion:\n{question}\n\nEvidence:\n{passages}\n"
    return prompts, hits


def frozen_inputs():
    document = (ROOT / "docs/evidence-control-experiment.md").read_text(encoding="utf-8")
    _, section_heading, section = document.partition("\n## English\n")
    if not section_heading:
        raise ValueError("The public experiment document is missing its English section.")
    english = section.split("\n## ", 1)[0]
    blocks = re.findall(r"^### ([ABC]) · [^\n]+\n\n```text\n(.*?)^```$", english, re.MULTILINE | re.DOTALL)
    if [group for group, _ in blocks] != ["A", "B", "C"]:
        raise ValueError("Expected exactly three English prompt blocks (A, B, C).")
    return dict(blocks), None


def prepare(frozen):
    prompts, hits = frozen_inputs() if frozen else live_inputs()
    run_dir = RUNS / f"evidence-control-{datetime.now():%Y%m%d-%H%M%S-%f}"
    run_dir.mkdir(parents=True)
    if hits is not None:
        save_json(run_dir / "retrieval.json", hits)
    groups = {}
    for group, prompt in prompts.items():
        groups[group] = re.findall(r"^\[([a-z0-9-]+)\]$", prompt, re.MULTILINE)
        (run_dir / f"{group}.txt").write_text(prompt, encoding="utf-8")
        print(f"{group}: {', '.join(groups[group])}")
    save_json(run_dir / "groups.json", groups)
    print(f"Inputs saved to: {run_dir.relative_to(ROOT)}")


def run(run_dir, model):
    groups = json.loads((run_dir / "groups.json").read_text(encoding="utf-8"))
    prompts = {group: (run_dir / f"{group}.txt").read_text(encoding="utf-8") for group in groups}
    if any((run_dir / f"{group}.response.json").exists() for group in groups):
        raise ValueError("This run already contains model responses. Use prepare to start a new run.")
    with urlopen(f"{OLLAMA}/api/tags", timeout=5) as response:
        available = [entry["name"] for entry in json.load(response)["models"]]
    if model not in available:
        raise ValueError(f"Model {model} is not installed. Available tags: {', '.join(available)}")

    for group, prompt in prompts.items():
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "think": False,
            "options": {"temperature": 0},
        }
        save_json(run_dir / f"{group}.request.json", payload)
        request = Request(
            f"{OLLAMA}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        print(f"Running group {group} with {model}", flush=True)
        with urlopen(request, timeout=600) as response:
            result = json.load(response)
        save_json(run_dir / f"{group}.response.json", result)
        print(result["message"]["content"], end="\n\n")
    print(f"Responses saved to: {run_dir}")


def main():
    parser = argparse.ArgumentParser(description="Prepare or run the three evidence controls.")
    commands = parser.add_subparsers(dest="command", required=True)
    preparation = commands.add_parser("prepare", help="Save the three inputs for review.")
    preparation.add_argument("--frozen", action="store_true", help="Replay the published inputs without a database.")
    execute = commands.add_parser("run", help="Send the prepared inputs to an installed Ollama model.")
    execute.add_argument("run_dir", type=Path)
    execute.add_argument("--model", default="gemma4:e4b", help="An installed model tag from ollama list.")
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            prepare(args.frozen)
        else:
            run(args.run_dir, args.model)
    except HTTPError as error:
        parser.exit(1, f"Ollama HTTP {error.code}: {error.read().decode(errors='replace')}\n")
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Experiment failed: {error}\n")


if __name__ == "__main__":
    main()
