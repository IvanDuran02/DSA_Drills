#!/usr/bin/env python3
"""
Structured test runner for Algorithm Drills.
Executes pytest with custom hooks to emit structured JSON test results.
"""

import argparse
import importlib
import json
import os
import sys
import time
from typing import Any, Dict, List
import pytest


class StructuredResultCollector:
    """Pytest plugin that collects structured test results."""

    def __init__(self, exercise_id: str, level: str):
        self.exercise_id = exercise_id
        self.level = level
        self.start_time = 0.0
        self.end_time = 0.0
        self.tests: List[Dict[str, Any]] = []
        self.has_not_implemented = False
        self.passed_count = 0
        self.failed_count = 0
        self.error_count = 0
        self.skipped_count = 0

    def pytest_sessionstart(self, session):
        self.start_time = time.time()

    def pytest_sessionfinish(self, session, exitstatus):
        self.end_time = time.time()

    def pytest_runtest_makereport(self, item, call):
        if call.when == "call" or (call.when == "setup" and call.excinfo is not None):
            duration_ms = (call.stop - call.start) * 1000.0 if hasattr(call, "stop") else 0.0
            test_name = item.name
            
            # Check markers or prefixes for level categorization (basic, edge, stress)
            test_level = "basic"
            if "edge" in test_name.lower():
                test_level = "edge"
            elif "stress" in test_name.lower() or "property" in test_name.lower() or "hypothesis" in test_name.lower():
                test_level = "stress"
            for marker in getattr(item, "own_markers", []):
                if marker.name in ("basic", "edge", "stress"):
                    test_level = marker.name

            status = "passed"
            message = ""
            is_unimplemented = False

            if call.excinfo is not None:
                exc_type = call.excinfo.type
                exc_value = str(call.excinfo.value)
                if exc_type is NotImplementedError or "NotImplementedError" in str(exc_type):
                    is_unimplemented = True
                    self.has_not_implemented = True
                    status = "unimplemented"
                    message = "NotImplementedError: Exercise is not implemented yet."
                else:
                    if call.when == "setup":
                        status = "error"
                        self.error_count += 1
                    else:
                        status = "failed"
                        self.failed_count += 1
                    message = f"{call.excinfo.typename}: {exc_value}"
            else:
                self.passed_count += 1

            self.tests.append({
                "name": test_name,
                "level": test_level,
                "status": status,
                "duration_ms": round(duration_ms, 2),
                "message": message,
                "is_unimplemented": is_unimplemented,
            })

    def to_dict(self) -> Dict[str, Any]:
        total = len(self.tests)
        unimplemented_count = sum(1 for t in self.tests if t["status"] == "unimplemented")
        # If all executed tests or all non-skipped tests failed due to NotImplementedError
        is_entirely_unimplemented = (
            self.has_not_implemented and
            (unimplemented_count + self.skipped_count == total or self.passed_count == 0)
        )

        return {
            "exercise_id": self.exercise_id,
            "level": self.level,
            "total": total,
            "passed": self.passed_count,
            "failed": self.failed_count,
            "errors": self.error_count,
            "skipped": self.skipped_count,
            "unimplemented": unimplemented_count,
            "is_unimplemented": is_entirely_unimplemented,
            "duration_ms": round((self.end_time - self.start_time) * 1000.0, 2),
            "tests": self.tests,
        }


def run_tests(
    exercise_id: str,
    test_path: str,
    target: str = "student",
    level: str = "all",
    impl_path: str = None,
) -> Dict[str, Any]:
    # Set environment variables so test files import the right target
    if target == "reference":
        os.environ["DRILLS_TARGET"] = "reference"
    else:
        os.environ["DRILLS_TARGET"] = "student"

    if impl_path:
        os.environ["DRILLS_IMPL_PATH"] = os.path.abspath(impl_path)
    else:
        os.environ.pop("DRILLS_IMPL_PATH", None)

    collector = StructuredResultCollector(exercise_id, level)

    pytest_args = [
        "-q",
        "--tb=short",
        "--import-mode=importlib",
        "-o", "python_files=test_*.py",
        "-o", "timeout=10",
        test_path,
    ]

    # Filter by level keyword if requested
    if level == "basic":
        pytest_args.extend(["-k", "basic or not (edge or stress or property)"])
    elif level == "edge":
        pytest_args.extend(["-k", "edge"])
    elif level == "stress":
        pytest_args.extend(["-k", "stress or property"])

    pytest.main(pytest_args, plugins=[collector])
    return collector.to_dict()


def main():
    parser = argparse.ArgumentParser(description="Structured pytest runner for drills")
    parser.add_argument("--exercise", required=True, help="Exercise ID")
    parser.add_argument("--test-file", required=True, help="Path to test file")
    parser.add_argument("--target", default="student", choices=["student", "reference"], help="Target code to test")
    parser.add_argument("--level", default="all", choices=["all", "basic", "edge", "stress"], help="Test level")
    parser.add_argument("--impl-file", default=None, help="Custom implementation file path")
    args = parser.parse_args()

    result = run_tests(
        exercise_id=args.exercise,
        test_path=args.test_file,
        target=args.target,
        level=args.level,
        impl_path=args.impl_file,
    )

    print("===DRILLS_JSON_START===")
    print(json.dumps(result, indent=2))
    print("===DRILLS_JSON_END===")


if __name__ == "__main__":
    main()
