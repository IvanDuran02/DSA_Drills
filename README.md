# Algorithm Drills — Google SWE Interview Training System

A high-performance algorithm implementation gym designed to help you master core algorithm patterns for Google SWE coding interviews.

Built with a **hybrid architecture**:
- **Application Engine:** Standalone native Go executable (`drills`) powered by **Bubble Tea**, **Lip Gloss**, **Cobra**, and pure-Go **SQLite**.
- **Exercise Engine:** **Python 3.14+** leveraging native standard library `heapq` max-heap operations, **pytest**, and **Hypothesis**.

---

## Architecture Highlights

1. **Native Speed:** All application logic—exercise discovery, practice sessions, timers, spaced repetition scheduling, analytics, mistake tracking, and database operations—is written in Go and runs in sub-milliseconds without touching Python.
2. **Subprocess Isolation:** Python is only invoked when executing student code or running `drills doctor`, running with explicit timeouts to prevent infinite loops from hanging the application.
3. **Structured Test Reports:** Pytest test results stream structured JSON back to the Go CLI and TUI.
4. **Full Interactive Terminal UI:** Built with Bubble Tea and Lip Gloss, inspired by lazygit. Launch `drills` with no arguments to enter the dashboard.
5. **Python 3.14 Native Max-Heaps:** All max-heap exercises natively use `heapq.heappush_max`, `heapq.heappop_max`, `heapq.heapify_max`, `heapq.heappushpop_max`, and `heapq.heapreplace_max`.

---

## Installation & Setup

### Requirements
- **Go 1.23+**
- **Python 3.14+**

### 1. Build and Setup Environment
```bash
# Clone and enter directory
cd algorithm-drills

# Set up Python 3.14 virtual environment and install test dependencies
make setup

# Compile native drills executable
make build

# (Optional) Install to $GOPATH/bin for global PATH access
make install
```

### 2. Verify System Health
Run `drills doctor` to verify your environment:
```bash
./bin/drills doctor
```
Output:
```text
ALGORITHM DRILLS — SYSTEM DOCTOR
─────────────────────────────────────────────────────────────────
 ✔  Host Architecture                : OS: darwin, Arch: arm64, Go Runtime: go1.26.1
 ✔  Python Interpreter Version       : Python 3.14.3 (.venv/bin/python3)
 ✔  Python 3.14 Native Max-Heap APIs : All 5 native max-heap APIs supported
 ✔  Python Dependencies              : pytest, hypothesis, pytest-timeout, pyyaml installed
 ✔  Exercise Metadata Library        : 88 exercises loaded across 9 categories
 ✔  SQLite Database Health           : Database OK at .drills/progress.db (integrity: ok)
 ✔  Test Runner Infrastructure       : Structured JSON test runner present
─────────────────────────────────────────────────────────────────
All system health checks passed! Environment is ready for interview practice.
```

---

## Interactive Terminal UI (TUI) Mode

Launch `drills` with no arguments to open the interactive dashboard:
```bash
./bin/drills
```

### Keyboard Navigation:
- **`1` – `8`**: Direct jump between tabs:
  - `1`: **Dashboard** (Today's workout, overdue alerts, overall mastery)
  - `2`: **Exercises** (Browse 88 drills across 9 categories, press `/` to search)
  - `3`: **Details** (Specifications, time/space targets, attempt history)
  - `4`: **Practice** (Active session, live timer, run tests, hint deck)
  - `5`: **Daily Plan** (Configurable 30/60/90 minute workout plan)
  - `6`: **Reviews** (Spaced repetition queue with overdue indicators)
  - `7`: **Analytics** (Category progress bars, recurring mistake frequencies)
  - `8`: **Settings** (Configured editor, timeout, review intervals)
- **`j` / `k` or `↑` / `↓`**: Navigate lists and menus.
- **`Enter`**: Select item / start drill.
- **`e`**: Launch `$EDITOR` (defaults to Neovim) directly on the starter file. The TUI cleanly suspends and resumes when the editor closes.
- **`t`**: Execute automated tests against your implementation in an isolated subprocess.
- **`h`**: Request incremental hints (Level 1: Minimal test case, Level 2: Area to investigate, Level 3: Invariant, Level 4: Concept, Level 5: Reference solution).
- **`f`**: Finish completed drill (verifies tests pass, opens hurdle classification modal, and records attempt).
- **`r`**: Clean-room reset (safely archives current code before resetting starter code).
- **`?`**: Toggle keyboard shortcuts help overlay.
- **`q`**: Return to previous screen or quit.

---

## CLI Commands (Scriptable)

All commands can also be run directly from your shell:

```bash
# List all exercises or filter by category
drills list
drills list --category graphs

# Show exercise details and specifications
drills show graph-bfs

# Start a timed practice session
drills start graph-bfs
drills start graph-bfs --fresh    # clean-room fresh attempt (archives prior code)

# Test your implementation
drills test graph-bfs
drills test graph-bfs --level basic
drills test graph-bfs --level edge
drills test graph-bfs --level stress
drills test --category trees
drills test --all --target reference

# Finish drill and record performance
drills finish graph-bfs --confidence 5 --mistakes visited_state

# Spaced repetition & training generator
drills today --minutes 60
drills review --due

# Progress & Analytics
drills progress
drills stats
drills mistakes

# Hints & Clean-Room Recovery
drills hint graph-bfs --level 2
drills recover graph-bfs
```

---

## Complete Exercise Library (88 Drills)

The repository includes **88 fully implemented and verified exercises**:

- **Graphs (17):** Adjacency list, DFS (recursive & iterative), BFS, Connected components (DFS & BFS), Cycle detection (undirected & directed), Topological sort (DFS & Kahn's), Union-Find (path compression & rank/size), Multi-source BFS, Grid DFS (Number of Islands), Grid BFS (Shortest path), Dijkstra, Bipartite graph detection.
- **Trees (10):** Preorder, Inorder, Postorder, Iterative inorder DFS, Level-order BFS, Max tree depth, Validate BST, Lowest common ancestor, Tree diameter, Serialize/Deserialize.
- **Binary Search (7):** Standard binary search, Lower bound, Upper bound, First & last occurrence, Search in rotated sorted array, Binary search on answer (Koko bananas), Find minimum in rotated array.
- **Heaps (10):** Native min-heap, Python 3.14 native max-heap (`heappush_max`, `heappop_max`), Heap construction (`heapify` & `heapify_max`), Replacement operations (`heapreplace` & `heapreplace_max`), Kth largest element, Top K frequent elements, Merge K sorted lists, Median from data stream (two-heaps), Priority queue with removals, Legacy negated-value max-heap.
- **Sliding Window & Two Pointers (10):** Fixed-size window, Variable-size window, Longest unique substring, Minimum window substring, Two Sum II (sorted), 3Sum, Fast/slow cycle detection, Range sum query prefix sums, Subarray sum equals K, Sliding window maximum.
- **Backtracking (8):** Subsets, Subsets with duplicates, Permutations, Combinations, Combination sum, Palindrome partitioning, Word search, Generate parentheses.
- **Dynamic Programming (14):** Fibonacci (memoization & tabulation), Climbing stairs, House robber, Coin change, 0/1 Knapsack, LCS, LIS, Unique grid paths, Edit distance, Target sum 2D memo, Take-or-skip recursion, Partition equal subset sum, Kadane's maximum subarray.
- **Stacks (6):** Basic stack operations, Valid parentheses, Monotonic stack (previous smaller), Daily temperatures, Next greater element (circular), Min stack.
- **Linked Lists (6):** Reverse linked list, Merge two sorted lists, Cycle entry point (Floyd's II), Middle of linked list, Remove Nth node from end, LRU cache.

---

## Testing & Verification

Run the entire verification test suite:

```bash
# Run Go framework tests
make test-go

# Run all 88 reference implementation tests
make test-ref

# Verify student starters are clean and unimplemented
./bin/drills test graph-bfs
```

---

## Spaced Repetition & Mastery

Exercises progress through 5 mastery tiers:
1. ⚪ **Not Started** (0 attempts)
2. 🔵 **Learning** (1 successful attempt)
3. 🟡 **Improving** (2+ successful attempts)
4. 🟢 **Proficient** (3+ passes across different days, streak >= 2, avg time <= 1.5x target)
5. ⭐ **Mastered** (4+ independent passes across spaced intervals, streak >= 3, best time <= target, hints <= 1)

Spaced reviews automatically schedule at **1 day -> 3 days -> 7 days -> 14 days -> 30 days -> 60 days -> 90 days** intervals, adjusting based on speed and hint dependency.

---

## License
MIT
