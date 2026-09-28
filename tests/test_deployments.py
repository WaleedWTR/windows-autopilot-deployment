from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from analyse_deployments import load, metrics  # noqa: E402

def test_dataset_size():
    assert len(load()) == 7

def test_success_rate():
    result = metrics(load())
    assert result["successes"] == 5
    assert result["success_rate"] == 71.4

def test_failure_stage_tracking():
    failures = metrics(load())["failures_by_stage"]
    assert failures["required-app"] == 1
    assert failures["policy"] == 1
