#!/usr/bin/env python3
"""Master library generator for Algorithm Drills"""

import os
from pathlib import Path
import yaml

from scripts.lib_graphs import GRAPH_EXERCISES
from scripts.lib_trees import TREE_EXERCISES
from scripts.lib_binary_search import BINARY_SEARCH_EXERCISES
from scripts.lib_heaps import HEAP_EXERCISES
from scripts.lib_sliding_window import SLIDING_WINDOW_EXERCISES
from scripts.lib_backtracking import BACKTRACKING_EXERCISES
from scripts.lib_dp import DP_EXERCISES
from scripts.lib_stacks import STACK_EXERCISES
from scripts.lib_linked_lists import LINKED_LIST_EXERCISES

ROOT = Path(__file__).resolve().parent.parent

ALL_CATEGORIES = [
    GRAPH_EXERCISES,
    TREE_EXERCISES,
    BINARY_SEARCH_EXERCISES,
    HEAP_EXERCISES,
    SLIDING_WINDOW_EXERCISES,
    BACKTRACKING_EXERCISES,
    DP_EXERCISES,
    STACK_EXERCISES,
    LINKED_LIST_EXERCISES,
]

def main():
    total = 0
    for category_list in ALL_CATEGORIES:
        for ex in category_list:
            cat = ex["category"]
            ex_id = ex["id"]
            filename = ex["file"]

            starter_rel = f"drills/{cat}/{filename}"
            ref_rel = f"reference/{cat}/{filename}"
            test_rel = f"tests/{cat}/test_{filename}"
            meta_rel = f"exercises/metadata/{ex_id}.yaml"

            starter_path = ROOT / starter_rel
            ref_path = ROOT / ref_rel
            test_path = ROOT / test_rel
            meta_path = ROOT / meta_rel

            # Ensure directories exist
            starter_path.parent.mkdir(parents=True, exist_ok=True)
            ref_path.parent.mkdir(parents=True, exist_ok=True)
            test_path.parent.mkdir(parents=True, exist_ok=True)
            meta_path.parent.mkdir(parents=True, exist_ok=True)

            # 1. Write starter file
            starter_path.write_text(ex["starter"])

            # 2. Write reference file
            ref_path.write_text(ex["reference"])

            # 3. Write test file
            test_path.write_text(ex["test"])

            # 4. Write metadata YAML
            metadata = {
                "id": ex_id,
                "name": ex["name"],
                "category": cat,
                "difficulty": ex["difficulty"],
                "level": ex.get("level", 1),
                "recommended_minutes": ex.get("recommended_minutes", 10),
                "target_complexity": {
                    "time": ex["time_complexity"],
                    "space": ex["space_complexity"],
                },
                "function_signature": ex["starter"],
                "starter_path": starter_rel,
                "test_path": test_rel,
                "reference_path": ref_rel,
                "description": f"Implement {ex['name']} in Python 3.14+.\n\nTarget Time: {ex['time_complexity']}\nTarget Space: {ex['space_complexity']}",
                "hints": ex.get("hints", {}),
                "variants": ["default"],
            }
            with open(meta_path, "w") as f:
                yaml.dump(metadata, f, sort_keys=False)

            total += 1

    print(f"Successfully generated {total} algorithm exercises across {len(ALL_CATEGORIES)} categories!")

if __name__ == "__main__":
    main()
