# Scoring, Mastery, and Spaced Repetition

## Spaced Repetition Intervals

Algorithm Drills implements spaced repetition to cement algorithmic patterns into long-term memory:

- Default intervals: **1 day -> 3 days -> 7 days -> 14 days -> 30 days -> 60 days -> 90 days**.

### Performance Adjustments:
1. **Independent Success (within recommended time, no hints):**
   Advances to next interval in sequence.
2. **Success with Significant Hints (>= 3 hints):**
   Interval resets or remains at 1 day.
3. **Slow Implementation (> 2x recommended time):**
   Interval set to 1 day for reinforcement.
4. **Failed / Incomplete Attempt:**
   Interval resets to 1 day; review streak resets to 0.
5. **Intra-Day Attempts:**
   Repeated successful attempts on the same calendar day do not artificially inflate the spaced repetition interval.

## Mastery Levels

Mastery is computed across multiple sessions:

| Level | Badge | Criteria |
|---|---|---|
| **1. Not Started** | ⚪ Not Started | 0 attempts |
| **2. Learning** | 🔵 Learning | 1 successful attempt |
| **3. Improving** | 🟡 Improving | 2+ successful attempts |
| **4. Proficient** | 🟢 Proficient | 3+ successful passes across different days, streak >= 2, avg time <= 1.5x target |
| **5. Mastered** | ⭐ Mastered | 4+ independent passes across spaced intervals, streak >= 3, best time <= target, hints <= 1 |
