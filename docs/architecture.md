# Algorithm Drills — Hybrid Architecture

`drills` is a high-performance algorithm training system designed for Google SWE interview preparation. It uses a **hybrid architecture** combining a native Go CLI & TUI application with a Python 3.14 algorithm exercise engine.

## Architectural Overview

```
+-------------------------------------------------------------------------+
|                              Native Go App                              |
|                                                                         |
|  +--------------------+   +---------------------+   +----------------+  |
|  |  Bubble Tea TUI    |   |  Cobra CLI Commands |   | Spaced Sched.  |  |
|  |  (LazyGit-styled)  |   |  (Scriptable)       |   | (1,3,7,14 day) |  |
|  +--------------------+   +---------------------+   +----------------+  |
|            |                         |                       |          |
|  +-------------------------------------------------------------------+  |
|  |             Shared Application Logic & Services                   |  |
|  |  • Spaced Repetition Scheduler    • Mistake Logging & Frequency   |  |
|  |  • Clean-Room Workspace Manager   • Daily Practice Generator      |  |
|  |  • Session Timers & Checkpoints   • Exercise Metadata Registry    |  |
|  +-------------------------------------------------------------------+  |
|            |                                              |             |
|  +----------------------+                       +--------------------+  |
|  | SQLite Progress DB   |                       | YAML Metadata      |  |
|  | (.drills/progress.db)|                       | (exercises/meta/)  |  |
|  +----------------------+                       +--------------------+  |
+-------------------------------------------------------------------------+
                                 | (Subprocess Isolation)
                                 v
+-------------------------------------------------------------------------+
|                       Python 3.14 Exercise Engine                       |
|                                                                         |
|  • Native heapq Max-Heaps (heappush_max, heappop_max, heapify_max)      |
|  • pytest + Hypothesis + pytest-timeout                                 |
|  • Clean Student Starter Code (drills/...)                             |
|  • Reference Solutions (reference/...)                                 |
|  • Structured JSON Test Runner (test_runner/runner.py)                 |
+-------------------------------------------------------------------------+
```

## Key Principles

1. **Zero Python on Ordinary Commands:**
   Listing exercises, viewing analytics, computing daily workout schedules, checking review dates, and inspecting mistakes run 100% in pure Go with sub-millisecond response times.
2. **Subprocess Isolation:**
   Python is only invoked when testing algorithm implementations or running `drills doctor`. Tests run in isolated subprocesses with explicit timeouts to prevent infinite loops from hanging the CLI or TUI.
3. **Structured JSON Test Output:**
   Pytest hooks stream structured JSON test results to Go rather than fragile terminal output parsing.
4. **Pure Go SQLite:**
   Uses `modernc.org/sqlite` avoiding CGO and external database servers.
5. **Clean-Room Resettability:**
   Previous attempts are archived safely in SQLite and `.drills/backups/`.
