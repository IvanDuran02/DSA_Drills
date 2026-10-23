# Daily Practice Workflow

## Recommended Daily Routine

### 1. Interactive Terminal UI (TUI) Mode (Default)

Simply launch:
```bash
./bin/drills
```
With no arguments, `drills` opens the full lazygit-inspired dashboard.

1. **Review Dashboard:** View today's personalized training plan and any overdue reviews.
2. **Press Enter:** Begins the first exercise of your daily workout session.
3. **Press 'e':** Suspends the TUI and opens Neovim (or `$EDITOR`) directly on the starter file.
4. **Implement Code:** Write your algorithm solution from memory.
5. **Save & Exit Editor:** Automatically returns to the interactive practice screen.
6. **Press 't':** Executes automated tests in an isolated Python subprocess and streams structured results.
7. **Press 'h':** Requests an incremental hint (Level 1 to 5) if blocked.
8. **Press 'f':** When tests pass, prompts you for confidence rating (1-5) and mistake classification, records attempt in SQLite, updates spaced repetition schedules, and returns to the dashboard.

---

### 2. Direct CLI Mode (Scriptable)

For quick shell access or scripting:

```bash
# Verify environment health
drills doctor

# View today's training plan
drills today --minutes 60

# Start a timed practice session
drills start graph-bfs

# Open in editor
$EDITOR drills/graphs/bfs.py

# Run tests
drills test graph-bfs

# Finish attempt and update spaced repetition
drills finish graph-bfs --confidence 5

# Check progress and spaced review queue
drills progress
drills review
```
