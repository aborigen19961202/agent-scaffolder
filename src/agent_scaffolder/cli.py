#!/usr/bin/env python3
"""
cli.py - Deterministic repository scaffolder and operational rules generator.

Deploys standard autonomous agent repository infrastructure:
- AGENTS.md (full 7-section discipline code)
- CLAUDE.md & GEMINI.md (single-source pointers)
- docs/ (architecture.md, roadmap.md, journal.md, journal/)
- experiments/ (README.md, _template/meta.json, _template/summary.md)
- scripts/ (run_cli_agent.py)
- .agents/skills/cli-agent-runner/ (SKILL.md)
- tests/ & .gitignore
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple

AGENTS_TEMPLATE = """# {PROJECT_NAME} — Operational Rules & Agent Discipline

Universal rules for Codex, Claude, Gemini, and other agents working on this project. `CLAUDE.md` and `GEMINI.md` import this file.

## 1. Authority, Scope & Execution Discipline
- The user defines scope, goals, and constraints. Explicit instructions override defaults.
- Context and analytical questions ("what is wrong?", "analyze X") permit investigation and reporting only. Do not modify files or environment state without a direct directive.
- Surgical changes only: touch only what is strictly required. Clean up only your own changes. Do not refactor adjacent working code.
- Report-and-stop: complete the assigned step, report the verified result concisely, and stop. Do not start subsequent stages or append speculative "Next Steps".
- Zero conversational noise: start directly with substance. Omit pleasantries, confirmation cliches ("understood", "great"), and redundant recaps.
- Persistence lifecycle: when instructed to fixate or save state, complete the full lifecycle: update the journal (`docs/journal.md`), stage, commit with a concise message, and push to the remote repository so work is never stranded locally.
- Platform boundaries: when investigating tools, bugs, or runtime behaviors, use official documentation, web search, public APIs, and CLI help. Never disassemble or reverse-engineer internal platform/runtime binaries unless explicitly directed.

## 2. Epistemic Vigilance & Truth
- Explicitly distinguish verified facts and observations from interpretations and hypotheses. The strength of a claim must never exceed its underlying evidence.
- Syntactic validity != logical truth: passing schema validation, linters, or format checks is not proof of correctness.
- Falsification over ritual: testing must actively probe failure modes and boundary edge cases rather than merely passing nominal checks.
- Honest failure: a failed run or disproven hypothesis is an objective result. Never redefine criteria post-hoc.
- Reject premature closure: models naturally default to premature closure and false confidence. Explicitly identify unknowns, fragile assumptions, and logical dead ends.
- No artificial defect quotas: if an artifact is valid, accept an empty defect list `[]` / clean state deterministically.
- Telemetry integrity: collect duration, token usage, and performance metrics strictly through scripts or tool outputs. Missing metrics are not zero; never invent or infer unavailable telemetry.

## 3. Evidence Before Accepting Changes (Baseline vs. Candidate)
- Candidate evaluation: every proposed change must address an explicit need and state its expected benefit against the current baseline.
- Regression rejection: do not promote a candidate with observed regressions or inconclusive evidence into the accepted version. Revert candidate changes when a regression occurs.
- Preserve evidence: preserve both accepted versions and rejected candidate data so decisions remain auditable.

## 4. Machine Over Manual Labor
- Fix the generator, never the artifact: never manually patch generated output. Resolve defects by updating code, prompts, schemas, or validators, followed by clean regeneration.
- Prompt universality: keep system prompts, worker instructions, and schemas domain-neutral and free of ad-hoc hotfixes for specific test cases.

## 5. Deterministic Scaffolding & Token Economy
- LLMs are stochastic data processors, not reliable state machines. System transitions, data contracts, retries, and data invariants belong to deterministic code/scripts.
- Delegate mechanical tasks (file operations, conversions, deterministic comparisons) to tools and scripts rather than burning model tokens.

## 6. Unix Philosophy & Component Design
- Single responsibility: each skill, script, or component has one clear responsibility with explicit inputs, outputs, and dependencies.
- Composition via transparent interfaces: compose simple components through plain text or structured data formats. Each component must allow independent verification, replacement, and repair.
- Standard tools over custom scripts: prioritize battle-tested, mature industry tools over unverified custom scripts or fragile makeshift solutions.
- Surgical constraints over artificial walls: guide agents with clear operational vectors and criteria rather than erecting walls of artificial bans or arbitrary step limits.

## 7. Simplicity First (Karpathy Rules)
- Think before coding: state assumptions explicitly. If uncertain, ask a targeted clarifying question rather than guessing.
- Implement the simplest design that completely satisfies the requirements. No speculative abstractions, unrequested configurability, or defensive overhead for hypothetical features.
- Match existing style. Every changed line must trace directly to the user's explicit request.
"""

GITIGNORE_CONTENT = """# Environments & dependencies
.venv/
venv/
env/
__pycache__/
*.pyc
node_modules/

# Logs & caches
*.log
.cache/
.pytest_cache/

# OS & IDE
.DS_Store
Thumbs.db
.idea/
.vscode/
*.swp

# Local credentials & secrets
.env
.env.local
*.local
"""

DOCS_ARCHITECTURE = """# Architecture & System Boundaries

## 1. Overview
High-level description of {PROJECT_NAME} purpose, core components, and responsibilities.

## 2. Component Boundaries & Invariants
- Explicit input and output contracts for each module.
- Deterministic invariants enforced across the system.
- Direct dependencies must be declared and minimal.

## 3. Technology Stack & Runtime Constraints
- Runtime platform, language versions, and external dependencies.
"""

DOCS_ROADMAP = """# Roadmap & Milestones

Milestones track approved goals and verifiable completion criteria. A milestone is achieved only when its criteria are satisfied with inspectable evidence.

## Milestones
- **M1: Foundation & Baseline**
  - **Outcome**: Core repository structure, deterministic validation tools, and basic environment setup.
  - **Completion Criteria**: Baseline checks and tests execute deterministically.
"""

DOCS_JOURNAL = """# Project Journal

Short index of decisions, experiments, and verifiable milestones with links to artifacts. Older entries are moved to `docs/journal/YYYY-MM.md`.

## Active Log
- **{DATE}**: Project initialized with deterministic scaffolding, epistemic operational rules (`AGENTS.md`), and documentation baseline.
"""

EXPERIMENTS_README = """# Experiments Directory

Standard directory structure for storing reproducible evaluations, benchmarks, and experimental runs.

## Directory Structure
Each experiment lives in its own subdirectory named `experiments/<experiment-id>/`:

```text
experiments/<experiment-id>/
├── meta.json        # Machine-readable execution parameters (model, timestamps, telemetry)
├── summary.md       # Epistemic report: hypothesis, baseline, observed result, decision
└── artifacts/       # Raw outputs, intermediate JSONs, or generated logs
```

## Rules
- Define the hypothesis and concrete success criteria *before* running.
- Record both successful and failed runs. Never delete a failed experiment.
- A candidate change is accepted only if comparison against the baseline demonstrates improvement without regressions.
"""

EXPERIMENT_META_TEMPLATE = """{{
  "experiment_id": "EXP-YYYYMMDD-01",
  "timestamp": "{DATE}T00:00:00Z",
  "model": "gemini-3.8-flash-high",
  "hypothesis": "Description of what is being tested",
  "baseline": "commit-or-run-id",
  "status": "candidate | accepted | rejected",
  "duration_sec": 0.0,
  "telemetry": {{
    "input_tokens": 0,
    "output_tokens": 0,
    "total_tokens": 0
  }}
}}
"""

EXPERIMENT_SUMMARY_TEMPLATE = """# Experiment Summary: [ID]

## 1. Hypothesis & Objective
- **Hypothesis:** [What is expected to improve or change]
- **Success Criteria:** [Falsifiable, concrete criteria defined beforehand]

## 2. Experimental Setup
- **Baseline:** [Reference to previous version or baseline run]
- **Candidate:** [What specific change was introduced]
- **Target / Inputs:** [Input data, prompt, or test suite used]

## 3. Observations & Evidence
- **Observations:** [Factual findings, test results, execution errors]
- **Regressions:** [Any degradation observed in other areas]

## 4. Decision
- **Status:** [ACCEPTED | REJECTED | INCONCLUSIVE]
- **Rationale:** [Concrete evidence justifying acceptance or rejection]
"""

SKILL_CLI_RUNNER = """---
name: cli-agent-runner
description: Execute Antigravity CLI (agy) agents and skills cleanly and deterministically. Use when running headless CLI agent tasks, inspecting raw semantic outputs, or verifying skills. Do not use for interactive TUI sessions or manual user chats.
---

# CLI Agent Runner

Automate and standardize execution of Antigravity CLI (`agy.exe`) agents in non-interactive (print) mode.

## 1. Principles & Subagent Rules

1. **No Fake Delegation (Anti-Roleplay):**
   - An LLM in a single CLI `--print` invocation cannot spawn a subagent through pure text instructions.
   - Never instruct an agent to "pass to a subagent" unless:
     a) A formal subagent is declared in `.agents/agents/<name>.md`, or
     b) The task is split into multiple distinct CLI runs orchestrated by a script.
   - If a skill requires multiple roles, execute them as sequential CLI turns with intermediate artifacts saved to disk.

2. **Required CLI Flags in Headless Mode:**
   - `--print "<prompt>"`: Run non-interactively.
   - `--output-format text`: Always output clean readable text. Never use `stream-json` for direct human inspection.
   - `--dangerously-skip-permissions`: Mandatory in headless mode if tools, files, or subagents are involved, to prevent the process from hanging on stdin prompts.
   - `--model "<model>"`: Explicitly specify the target model (default: `gemini-3.8-flash-high`).

## 2. Standard Runner Script

Always use the deterministic runner script rather than typing ad-hoc shell commands:

```bash
python scripts/run_cli_agent.py \\
  --cwd "<target_working_directory>" \\
  --prompt "<prompt_or_skill_invocation>" \\
  --out-dir "<artifacts_output_directory>"
```

### Parameters

* `--cwd`: Target workspace root.
* `--prompt`: The instruction or skill trigger (e.g., `"Use <skill-name>. Topic: ..."`).
* `--out-dir`: Optional directory to save a markdown report containing the prompt, output, duration, and status.
* `--model`: Optional model override (default: `gemini-3.8-flash-high`).
* `--timeout`: Execution timeout in seconds (default: 180s).

## 3. Workflow for Running an Agent Task

1. **Verify Target Environment:**
   Ensure the target workspace (`--cwd`) contains any required `.agents/skills/` or `.agents/agents/`.
2. **Execute via Runner:**
   Run `scripts/run_cli_agent.py` with the appropriate parameters.
3. **Inspect Semantic Output:**
   - Read the output directly from stdout or from the generated report in `--out-dir`.
   - Verify that the response is substantive, follows the required constraints, and does not contain simulated delegation or empty roleplay.
4. **Log Results:**
   If running an evaluation, link the saved artifact in the project journal or experiment record.
"""

RUN_CLI_AGENT_SCRIPT = """#!/usr/bin/env python3
\"\"\"
run_cli_agent.py - Deterministic runner for Antigravity CLI (agy) agents.

Provides a clean, reliable execution harness for running agy in headless
print mode with proper permissions, timeouts, step limits, and output capture.
\"\"\"

import argparse
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

_telemetry_lock = threading.Lock()
KNOWN_AGY_PATHS = [
    Path(os.environ.get("LOCALAPPDATA", "")) / "agy" / "bin" / "agy.exe",
    Path.home() / "AppData" / "Local" / "agy" / "bin" / "agy.exe",
]


def find_agy(custom_path=None):
    if custom_path:
        p = Path(custom_path).resolve()
        if p.is_file():
            return str(p)
        raise FileNotFoundError(f"Specified agy executable not found at {p}")
    for p in KNOWN_AGY_PATHS:
        if p.is_file():
            return str(p)
    which_agy = shutil.which("agy") or shutil.which("agy.exe")
    if which_agy:
        return which_agy
    raise FileNotFoundError("Could not find agy.exe. Specify path via --agy-path.")


def _is_valid_json_output(text: str) -> bool:
    s = (text or "").strip()
    if s.startswith("```json"):
        s = s[7:].strip()
    elif s.startswith("```"):
        s = s[3:].strip()
    if s.endswith("```"):
        s = s[:-3].strip()
    has_obj = s.startswith("{") and s.endswith("}")
    has_arr = s.startswith("[") and s.endswith("]")
    if not (has_obj or has_arr):
        return False
    try:
        json.loads(s)
        return True
    except Exception:
        return False


def _run_agent_stream(
    cmd: List[str],
    cwd: Path,
    timeout: int,
    max_steps: Optional[int] = None,
    is_complete_fn: Optional[Callable[[str], bool]] = None,
) -> Tuple[str, str, Optional[str], float, int, Dict[str, Any]]:
    start_time = time.time()
    proc = subprocess.Popen(
        cmd,
        cwd=str(cwd),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )

    q: queue.Queue = queue.Queue()

    def reader(pipe, q):
        try:
            for line in iter(pipe.readline, ""):
                q.put(line)
        finally:
            pipe.close()

    t_thread = threading.Thread(target=reader, args=(proc.stdout, q), daemon=True)
    t_thread.start()

    response_text = ""
    status = None
    step_count = 0
    usage: Dict[str, Any] = {}

    try:
        while True:
            now = time.time()
            if (now - start_time) >= timeout:
                status = "timeout"
                break

            try:
                line = q.get(timeout=0.2)
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                    ev_type = ev.get("event")
                    if ev_type == "step_update":
                        su = ev.get("step_update", {})
                        idx = su.get("step_index", 0)
                        step_count = max(step_count, idx)
                        if max_steps is not None and step_count >= max_steps:
                            status = "max_steps_exceeded"
                            break
                    elif ev_type == "result":
                        res = ev.get("result", {})
                        response_text = res.get("response", "")
                        usage = res.get("usage", {})
                        num_turns = res.get("num_turns", 0)
                        if num_turns > step_count:
                            step_count = num_turns
                        status = "success"
                        break
                except Exception:
                    pass
            except queue.Empty:
                ret = proc.poll()
                if ret is not None:
                    while not q.empty():
                        try:
                            l = q.get_nowait().strip()
                            if l:
                                ev = json.loads(l)
                                if ev.get("event") == "result":
                                    response_text = ev.get("result", {}).get("response", "")
                                    usage = ev.get("result", {}).get("usage", {})
                        except Exception:
                            pass
                    status = "success" if ret == 0 else f"failed (code {ret})"
                    break
    finally:
        if proc.poll() is None:
            proc.kill()
            try:
                proc.wait(timeout=2)
            except Exception:
                pass

    duration = time.time() - start_time
    if step_count == 0 and status == "success":
        step_count = 1
    stderr = ""
    try:
        stderr = proc.stderr.read()
    except Exception:
        pass

    return response_text, stderr, status, duration, step_count, usage


def run_agent(
    prompt: str,
    cwd: Path,
    model: str = "gemini-3.8-flash-high",
    timeout: int = 180,
    out_dir: Path = None,
    agy_path: str = None,
    is_complete_fn=None,
    max_steps: Optional[int] = None,
    output_format: str = "stream-json",
):
    agy_bin = find_agy(agy_path)
    cwd = Path(cwd).resolve()
    model = model or "gemini-3.8-flash-high"

    if not cwd.is_dir():
        raise NotADirectoryError(f"Target directory does not exist: {cwd}")

    use_stream = output_format == "stream-json" or max_steps is not None

    if use_stream:
        cmd = [
            agy_bin,
            "--model", model,
            "--dangerously-skip-permissions",
            "--output-format", "stream-json",
            "--print", prompt,
        ]
        stdout, stderr, status, duration, step_count, usage = _run_agent_stream(
            cmd=cmd,
            cwd=cwd,
            timeout=timeout,
            max_steps=max_steps,
            is_complete_fn=is_complete_fn,
        )
    else:
        cmd = [
            agy_bin,
            "--model", model,
            "--dangerously-skip-permissions",
            "--output-format", "text",
            "--print", prompt,
        ]

        import tempfile

        start_time = time.time()
        with tempfile.TemporaryFile(mode="w+b") as out_f, tempfile.TemporaryFile(mode="w+b") as err_f:
            proc = subprocess.Popen(
                cmd,
                cwd=str(cwd),
                stdin=subprocess.DEVNULL,
                stdout=out_f,
                stderr=err_f,
            )
            status = None
            last_size = 0
            last_growth_time = start_time

            while True:
                ret = proc.poll()
                now = time.time()
                if ret is not None:
                    duration = now - start_time
                    status = "success" if ret == 0 else f"failed (code {ret})"
                    break

                out_f.flush()
                out_f.seek(0, os.SEEK_END)
                cur_size = out_f.tell()
                if cur_size != last_size:
                    last_size = cur_size
                    last_growth_time = now
                elif cur_size > 0 and (now - last_growth_time) >= 3.0:
                    out_f.seek(0)
                    cur_text = out_f.read().decode("utf-8", errors="replace").strip()
                    completed = False
                    if is_complete_fn is not None:
                        try:
                            completed = bool(is_complete_fn(cur_text))
                        except Exception:
                            completed = False
                    elif _is_valid_json_output(cur_text):
                        completed = True

                    if completed:
                        proc.kill()
                        try:
                            proc.wait(timeout=5)
                        except Exception:
                            pass
                        duration = time.time() - start_time
                        status = "success"
                        break

                if (now - start_time) >= timeout:
                    proc.kill()
                    try:
                        proc.wait(timeout=5)
                    except Exception:
                        pass
                    duration = time.time() - start_time
                    status = "timeout"
                    break

                time.sleep(0.5)

            out_f.seek(0)
            err_f.seek(0)
            stdout = out_f.read().decode("utf-8", errors="replace").strip()
            stderr = err_f.read().decode("utf-8", errors="replace").strip()
            step_count = 1
            usage = {}

    result = {
        "status": status,
        "duration_sec": round(duration, 2),
        "cwd": str(cwd),
        "model": model,
        "prompt": prompt,
        "output": stdout,
        "stderr": stderr,
        "step_count": step_count,
        "usage": usage,
    }

    if out_dir:
        out_dir = Path(out_dir).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        result_file = out_dir / f"agent_run_{ts}.md"
        with open(result_file, "w", encoding="utf-8") as f:
            f.write(f"# Agent Run Result\\n\\n")
            f.write(f"- **Status:** {status}\\n")
            f.write(f"- **Duration:** {result['duration_sec']}s\\n")
            f.write(f"- **Steps:** {step_count}\\n")
            if usage:
                in_t = usage.get("input_tokens", 0)
                out_t = usage.get("output_tokens", 0)
                cache_t = usage.get("cache_read_tokens", 0)
                tot_t = usage.get("total_tokens", 0)
                f.write(f"- **Tokens:** In={in_t:,}, Out={out_t:,}, CacheRead={cache_t:,}, Total={tot_t:,}\\n")
            f.write(f"- **CWD:** `{cwd}`\\n")
            f.write(f"- **Model:** `{model}`\\n\\n")
            f.write(f"## Prompt\\n\\n```text\\n{prompt}\\n```\\n\\n")
            f.write(f"## Output\\n\\n{stdout}\\n\\n")
            if stderr:
                f.write(f"## Stderr\\n\\n```text\\n{stderr}\\n```\\n")
        result["saved_to"] = str(result_file)

    telem_file = os.environ.get("PROJECT_TELEMETRY_FILE")
    if telem_file:
        try:
            telem_path = Path(telem_file)
            telem_path.parent.mkdir(parents=True, exist_ok=True)
            entry = {
                "timestamp": datetime.now().isoformat(),
                "cwd": str(cwd),
                "model": model,
                "status": status,
                "duration_sec": round(duration, 2),
                "step_count": step_count,
                "usage": usage,
                "out_dir": str(out_dir) if out_dir else None,
            }
            with _telemetry_lock:
                with open(telem_path, "a", encoding="utf-8") as tf:
                    tf.write(json.dumps(entry, ensure_ascii=False) + "\\n")
        except Exception:
            pass

    return result


def main_runner():
    parser = argparse.ArgumentParser(description="Run an Antigravity agent in CLI.")
    parser.add_argument("--cwd", default=".", help="Working directory for the agent.")
    parser.add_argument("--prompt", required=True, help="Prompt text to run.")
    parser.add_argument("--model", default="gemini-3.8-flash-high", help="Model to use.")
    parser.add_argument("--timeout", type=int, default=180, help="Timeout in seconds.")
    parser.add_argument("--max-steps", type=int, default=None, help="Maximum agent steps before terminating.")
    parser.add_argument("--output-format", default="text", choices=["text", "stream-json"], help="Output format.")
    parser.add_argument("--out-dir", default=None, help="Directory to save the markdown report.")
    parser.add_argument("--agy-path", default=None, help="Custom path to agy.exe.")

    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    res = run_agent(
        prompt=args.prompt,
        cwd=Path(args.cwd),
        model=args.model,
        timeout=args.timeout,
        max_steps=args.max_steps,
        output_format=args.output_format,
        out_dir=Path(args.out_dir) if args.out_dir else None,
        agy_path=args.agy_path,
    )

    print(f"[{res['status'].upper()}] Duration: {res['duration_sec']}s")
    if "saved_to" in res:
        print(f"Saved: {res['saved_to']}")
    print("\\n--- Output ---")
    print(res["output"])
    if res["stderr"]:
        print("\\n--- Stderr ---", file=sys.stderr)
        print(res["stderr"], file=sys.stderr)

    if res["status"] != "success":
        sys.exit(1)
"""


def scaffold(target_path: Path, project_name: str, force: bool = False) -> Tuple[int, int]:
    target = target_path.resolve()
    target.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")

    files = {
        target / ".gitignore": GITIGNORE_CONTENT,
        target / "AGENTS.md": AGENTS_TEMPLATE.format(PROJECT_NAME=project_name),
        target / "CLAUDE.md": "@AGENTS.md\n",
        target / "GEMINI.md": "@AGENTS.md\n",
        target / "docs" / "architecture.md": DOCS_ARCHITECTURE.format(PROJECT_NAME=project_name),
        target / "docs" / "roadmap.md": DOCS_ROADMAP,
        target / "docs" / "journal.md": DOCS_JOURNAL.format(DATE=date_str),
        target / "docs" / "journal" / ".gitkeep": "",
        target / "experiments" / "README.md": EXPERIMENTS_README,
        target / "experiments" / "_template" / "meta.json": EXPERIMENT_META_TEMPLATE.format(DATE=date_str),
        target / "experiments" / "_template" / "summary.md": EXPERIMENT_SUMMARY_TEMPLATE,
        target / "scripts" / "run_cli_agent.py": RUN_CLI_AGENT_SCRIPT,
        target / "scripts" / ".gitkeep": "",
        target / "tests" / ".gitkeep": "",
        target / ".agents" / "skills" / ".gitkeep": "",
        target / ".agents" / "skills" / "cli-agent-runner" / "SKILL.md": SKILL_CLI_RUNNER,
    }

    created = 0
    skipped = 0

    for file_path, content in files.items():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if file_path.exists() and not force:
            skipped += 1
            continue
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        created += 1

    return created, skipped


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold an autonomous agent project infrastructure."
    )
    parser.add_argument("target", help="Target directory for the new project.")
    parser.add_argument(
        "--name",
        default=None,
        help="Project name (default: directory name in uppercase).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files in target directory.",
    )

    args = parser.parse_args()
    target_dir = Path(args.target)
    proj_name = args.name or target_dir.resolve().name.upper()

    print(f"Scaffolding project '{proj_name}' at: {target_dir.resolve()}")
    created, skipped = scaffold(target_dir, proj_name, force=args.force)
    print(f"Completed: {created} files created, {skipped} skipped.")


if __name__ == "__main__":
    main()
