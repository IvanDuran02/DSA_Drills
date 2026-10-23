package db_test

import (
	"path/filepath"
	"testing"
	"time"

	"github.com/user/algorithm-drills/internal/db"
)

func TestDBLifecycle(t *testing.T) {
	tmpDir := t.TempDir()
	dbPath := filepath.Join(tmpDir, "test_progress.db")

	database, err := db.InitDB(dbPath)
	if err != nil {
		t.Fatalf("failed to init db: %v", err)
	}
	defer database.Close()

	// 1. Progress CRUD
	p, err := database.GetProgress("graph-dfs")
	if err != nil {
		t.Fatalf("failed to get default progress: %v", err)
	}
	if p.MasteryLevel != 1 {
		t.Fatalf("expected mastery 1, got %d", p.MasteryLevel)
	}

	p.MasteryLevel = 3
	p.SuccessfulAttempts = 2
	p.TotalAttempts = 3
	now := time.Now().UTC()
	p.LastPracticeAt = &now
	next := now.Add(72 * time.Hour)
	p.NextReviewAt = &next

	if err := database.SaveProgress(p); err != nil {
		t.Fatalf("failed to save progress: %v", err)
	}

	loaded, err := database.GetProgress("graph-dfs")
	if err != nil {
		t.Fatalf("failed to load saved progress: %v", err)
	}
	if loaded.MasteryLevel != 3 || loaded.SuccessfulAttempts != 2 {
		t.Fatalf("loaded progress mismatch: %+v", loaded)
	}

	// 2. Attempt logging
	att := &db.Attempt{
		ExerciseID:       "graph-dfs",
		SessionID:        "sess_1",
		Variant:          "default",
		StartTime:        now.Add(-10 * time.Minute),
		EndTime:          &now,
		DurationSec:      600,
		Status:           "passed",
		BasicPassed:      5,
		ConfidenceRating: 5,
	}
	attID, err := database.RecordAttempt(att)
	if err != nil {
		t.Fatalf("failed to record attempt: %v", err)
	}
	if attID <= 0 {
		t.Fatalf("expected positive attempt id, got %d", attID)
	}

	recent, err := database.GetRecentAttempts(10)
	if err != nil {
		t.Fatalf("failed to get recent attempts: %v", err)
	}
	if len(recent) != 1 || recent[0].ExerciseID != "graph-dfs" {
		t.Fatalf("expected 1 recent attempt for graph-dfs, got %d", len(recent))
	}

	// 3. Mistake logs
	err = database.LogMistake(&db.MistakeLog{
		AttemptID:  attID,
		ExerciseID: "graph-dfs",
		Category:   "graphs",
		MistakeID:  "visited_state",
	})
	if err != nil {
		t.Fatalf("failed to log mistake: %v", err)
	}

	freq, err := database.GetMistakeFrequency("graphs")
	if err != nil {
		t.Fatalf("failed to get mistake frequency: %v", err)
	}
	if freq["visited_state"] != 1 {
		t.Fatalf("expected 1 visited_state mistake, got %d", freq["visited_state"])
	}

	// 4. Saved attempts (Clean room)
	err = database.SaveCodeAttempt("graph-dfs", "backup 1", "def dfs(): pass")
	if err != nil {
		t.Fatalf("failed to save code attempt: %v", err)
	}

	saved, err := database.GetSavedAttempts("graph-dfs")
	if err != nil {
		t.Fatalf("failed to get saved attempts: %v", err)
	}
	if len(saved) != 1 || saved[0].Label != "backup 1" {
		t.Fatalf("expected 1 saved attempt, got %d", len(saved))
	}
}
