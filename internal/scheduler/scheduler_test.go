package scheduler_test

import (
	"testing"
	"time"

	"github.com/user/algorithm-drills/internal/db"
	"github.com/user/algorithm-drills/internal/exercise"
	"github.com/user/algorithm-drills/internal/scheduler"
)

func TestSpacedRepetitionProgression(t *testing.T) {
	ex := &exercise.Exercise{
		ID:                 "graph-dfs",
		Category:           "graphs",
		RecommendedMinutes: 8,
	}

	p := &db.ExerciseProgress{
		ExerciseID:   "graph-dfs",
		MasteryLevel: 1,
		IntervalDays: 1,
	}

	intervals := []int{1, 3, 7, 14}

	// First pass
	scheduler.UpdateProgressOnAttempt(p, ex, true, 300, 0, intervals)
	if p.SuccessfulAttempts != 1 {
		t.Fatalf("expected 1 successful attempt, got %d", p.SuccessfulAttempts)
	}
	if p.MasteryLevel != 2 { // Learning
		t.Fatalf("expected mastery 2 (Learning), got %d", p.MasteryLevel)
	}
	if p.IntervalDays != 3 {
		t.Fatalf("expected interval 3 days, got %d", p.IntervalDays)
	}

	// Simulate next day practice
	yesterday := time.Now().UTC().Add(-25 * time.Hour)
	p.LastPracticeAt = &yesterday

	// Second pass
	scheduler.UpdateProgressOnAttempt(p, ex, true, 280, 0, intervals)
	if p.SuccessfulAttempts != 2 {
		t.Fatalf("expected 2 successful attempts, got %d", p.SuccessfulAttempts)
	}
	if p.MasteryLevel != 3 { // Improving
		t.Fatalf("expected mastery 3 (Improving), got %d", p.MasteryLevel)
	}
	if p.IntervalDays != 7 {
		t.Fatalf("expected interval 7 days, got %d", p.IntervalDays)
	}

	// Failure resets streak and interval
	p.LastPracticeAt = &yesterday
	scheduler.UpdateProgressOnAttempt(p, ex, false, 0, 0, intervals)
	if p.Streak != 0 {
		t.Fatalf("expected streak 0 on failure, got %d", p.Streak)
	}
	if p.IntervalDays != 1 {
		t.Fatalf("expected interval 1 day on failure, got %d", p.IntervalDays)
	}
}
