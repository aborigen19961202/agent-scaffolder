# agent-scaffolder

Deterministic repository scaffolder and operational discipline generator for autonomous LLM agents (Antigravity, Codex, Claude, Gemini).

## Overview

`agent-scaffolder` bootstraps a production-ready, epistemic development environment for autonomous agent systems. It enforces bounded agency, single source of truth operational rules, Unix component design, and reproducible experiment tracking.

## Standard Scaffolding Structure

Running `agent-scaffold` creates the following canonical repository structure:

```text
my-project/
├── .agents/
│   └── skills/
│       └── cli-agent-runner/     # Standard headless agy CLI runner skill
├── docs/
│   ├── architecture.md           # System boundaries & component invariants
│   ├── roadmap.md                # Milestones with falsifiable criteria
│   ├── journal.md                # Active decision log (YYYY-MM archives)
│   └── journal/
├── experiments/                  # Candidate vs Baseline experiment framework
│   ├── README.md
│   └── _template/
│       ├── meta.json             # Machine-readable execution & telemetry
│       └── summary.md            # Epistemic report template
├── scripts/
│   └── run_cli_agent.py          # Deterministic Python harness for CLI agents
├── tests/                        # Deterministic test suite
├── .gitignore                    # Python, Node, OS, IDE, and secret exclusions
├── AGENTS.md                     # Single source of truth operational rules
├── CLAUDE.md                     # Pointer: @AGENTS.md
└── GEMINI.md                     # Pointer: @AGENTS.md
```

## The 7 Core Operational Rules in `AGENTS.md`

1. **Authority & Scope:** Clarifications vs Directives, Report-and-stop, Persistence lifecycle (`journal -> stage -> commit -> push`).
2. **Epistemic Vigilance:** Facts vs hypotheses, form vs substance, test falsification, anti-premature closure, telemetry integrity.
3. **Evidence Before Acceptance:** Baseline vs Candidate protocol, regression rollback.
4. **Machine Over Manual Labor:** Fix the generator (code/prompts/schemas), never patch generated artifacts manually.
5. **Deterministic Scaffolding:** LLM as stochastic data processor inside typed code constraints and token economy.
6. **Unix Philosophy:** Single responsibility, composition via transparent text/structured interfaces, mature standard tools.
7. **Simplicity First:** Karpathy guidelines, surgical changes, no speculative abstractions.

## Installation & Usage

### Local Usage
```bash
git clone https://github.com/aborigen19961202/agent-scaffolder.git
cd agent-scaffolder
pip install -e .
```

### CLI Command
```bash
# Basic usage (derives project name from directory)
agent-scaffold "path/to/my-project"

# Explicit project name
agent-scaffold "path/to/my-project" --name "PROJECT-NAME"

# Overwrite existing files
agent-scaffold "path/to/my-project" --force
```

## License

MIT
