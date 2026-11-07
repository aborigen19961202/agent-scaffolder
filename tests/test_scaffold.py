import tempfile
from pathlib import Path
from agent_scaffolder.cli import scaffold


def test_scaffold_creates_standard_files():
    with tempfile.TemporaryDirectory() as tmp_dir:
        target = Path(tmp_dir)
        created, skipped = scaffold(target, "TEST-PROJECT")

        assert created == 16
        assert skipped == 0

        # Invariant checks
        assert (target / "AGENTS.md").is_file()
        assert (target / "CLAUDE.md").read_text(encoding="utf-8").strip() == "@AGENTS.md"
        assert (target / "GEMINI.md").read_text(encoding="utf-8").strip() == "@AGENTS.md"
        assert (target / "docs" / "architecture.md").is_file()
        assert (target / "docs" / "roadmap.md").is_file()
        assert (target / "docs" / "journal.md").is_file()
        assert (target / "experiments" / "README.md").is_file()
        assert (target / "scripts" / "run_cli_agent.py").is_file()
        assert (target / ".agents" / "skills" / "cli-agent-runner" / "SKILL.md").is_file()

        # Check project name interpolation
        agents_content = (target / "AGENTS.md").read_text(encoding="utf-8")
        assert "TEST-PROJECT" in agents_content


def test_scaffold_does_not_overwrite_without_force():
    with tempfile.TemporaryDirectory() as tmp_dir:
        target = Path(tmp_dir)
        scaffold(target, "TEST-PROJECT")

        # Second run without force
        created, skipped = scaffold(target, "TEST-PROJECT", force=False)
        assert created == 0
        assert skipped == 16


def test_scaffold_overwrites_with_force():
    with tempfile.TemporaryDirectory() as tmp_dir:
        target = Path(tmp_dir)
        scaffold(target, "TEST-PROJECT")

        # Second run with force
        created, skipped = scaffold(target, "TEST-PROJECT", force=True)
        assert created == 16
        assert skipped == 0
