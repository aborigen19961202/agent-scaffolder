# AGENT-SCAFFOLDER — Operational Rules & Agent Discipline

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
