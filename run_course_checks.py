"""Collect authentic course evidence inside the Skills Network Theia Lab."""

from datetime import datetime, timezone
import os
from pathlib import Path
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "submission"


def collect(name, command, directory=ROOT):
    """Run one check, save its actual output, and stop on failure."""
    print(f"Running {name}...", flush=True)
    completed = subprocess.run(
        command, cwd=directory, capture_output=True, text=True, check=False
    )
    log = (
        f"UTC: {datetime.now(timezone.utc).isoformat()}\n"
        f"Directory: {directory}\n$ {shlex.join(command)}\n"
        f"{completed.stdout}{completed.stderr}\nExit status: {completed.returncode}\n"
    )
    (EVIDENCE / f"{name}.txt").write_text(log, encoding="utf-8")
    print(log, flush=True)
    if completed.returncode:
        raise SystemExit(completed.returncode)


def main():
    """Create submission snippets and run live model, Flask, and lint checks."""
    EVIDENCE.mkdir(exist_ok=True)
    os.environ.setdefault("PYLINTHOME", str(ROOT / ".pylint_cache"))
    snippets = {
        "2a_emotion_detection": "checkpoints/task2/emotion_detection.py",
        "3a_output_formatting": "checkpoints/task3/emotion_detection.py",
        "5a_unit_testing": "test_emotion_detection.py",
        "6a_server": "server.py",
        "7a_error_handling_function": "EmotionDetection/emotion_detection.py",
        "7b_error_handling_server": "server.py",
        "8a_server_modified": "server.py",
    }
    for name, source in snippets.items():
        (EVIDENCE / f"{name}.txt").write_text(
            (ROOT / source).read_text(encoding="utf-8"), encoding="utf-8"
        )
    collect(
        "2b_application_creation",
        [sys.executable, "-c", 'from emotion_detection import emotion_detector; '
         'print(emotion_detector("I love this new technology."))'],
        ROOT / "checkpoints/task2",
    )
    collect(
        "3b_formatted_output_test",
        [sys.executable, "-c", 'from emotion_detection import emotion_detector; '
         'result = emotion_detector("I am so happy I am doing this"); '
         'print(result); assert result["dominant_emotion"] == "joy"'],
        ROOT / "checkpoints/task3",
    )
    collect(
        "4b_packaging_test",
        [sys.executable, "-c", 'from EmotionDetection.emotion_detection import emotion_detector; '
         'result = emotion_detector("I hate working long hours"); '
         'print(result); assert result["dominant_emotion"] == "anger"'],
    )
    collect("5b_unit_testing_result", [sys.executable, "test_emotion_detection.py"])
    collect("offline_tests", [sys.executable, "-m", "unittest", "-v", "test_offline"])
    collect(
        "7_http_400_check",
        [sys.executable, "-c", 'import requests; '
         'from EmotionDetection.emotion_detection import URL, HEADERS, emotion_detector; '
         'response = requests.post(URL, headers=HEADERS, '
         'json={"raw_document": {"text": ""}}, timeout=30); '
         'print("Actual Watson blank-input HTTP status:", response.status_code); '
         'assert response.status_code == 400; '
         'print("Package blank result:", emotion_detector(""))'],
    )
    collect("8b_static_code_analysis", [sys.executable, "-m", "pylint", "server.py"])
    print("All checks passed. Capture the two required deployed-interface screenshots.")


if __name__ == "__main__":
    main()
