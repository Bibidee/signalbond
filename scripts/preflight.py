from pathlib import Path
import ast, shutil, subprocess, sys
ROOT = Path(__file__).resolve().parents[1]
contracts = list((ROOT / "contracts").glob("*.py"))
if len(contracts) != 1: raise SystemExit(f"expected exactly one deployable contract, found {len(contracts)}")
source = contracts[0]
ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
lint = shutil.which("genvm-lint") or shutil.which("genvm-lint.exe")
if not lint:
    sibling = Path(sys.executable).with_name("genvm-lint.exe")
    if sibling.exists(): lint = str(sibling)
if not lint: raise SystemExit("genvm-lint is required; install genvm-linter before preflight")
subprocess.run([lint, "check", str(source), "--json"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "-m", "pytest", "tests/direct", "-q"], cwd=ROOT, check=True)
print("preflight passed")
