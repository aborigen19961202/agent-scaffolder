# Architecture & System Boundaries

## 1. Overview
`agent-scaffolder` is a zero-dependency CLI package and Python library that deploys standard autonomous agent environments with bounded agency, single source of truth rules (`AGENTS.md`), and deterministic validation tools.

## 2. Invariants & Contracts
- Zero external dependencies outside Python 3.9+ standard library.
- Deterministic output: running with the same parameters on an empty folder produces identical file trees.
- Non-destructive by default: existing files are never overwritten unless `--force` is specified.

## 3. Structure
- `agent_scaffolder.cli`: CLI entrypoint and template definitions.
- `agent_scaffolder.scaffold()`: Core library function.
