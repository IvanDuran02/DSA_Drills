package db

import (
	"database/sql"
	"fmt"
	"os"
	"path/filepath"
	"time"

	_ "modernc.org/sqlite"
)

type DB struct {
	Conn *sql.DB
}

type ExerciseProgress struct {
	ExerciseID            string     `json:"exercise_id"`
	Variant               string     `json:"variant"`
	MasteryLevel          int        `json:"mastery_level"` // 1: Not Started, 2: Learning, 3: Improving, 4: Proficient, 5: Mastered
	TotalAttempts         int        `json:"total_attempts"`
	SuccessfulAttempts    int        `json:"successful_attempts"`
	FirstAttemptSuccess   bool       `json:"first_attempt_success"`
	AvgCompletionTimeSec  float64    `json:"avg_completion_time_sec"`
	BestCompletionTimeSec float64    `json:"best_completion_time_sec"`
	TotalHintsUsed        int        `json:"total_hints_used"`
	LastPracticeAt        *time.Time `json:"last_practice_at"`
	NextReviewAt          *time.Time `json:"next_review_at"`
	IntervalDays          int        `json:"interval_days"`
	Streak                int        `json:"streak"`
	FollowupCompleted     bool       `json:"followup_completed"`
	CreatedAt             time.Time  `json:"created_at"`
	UpdatedAt             time.Time  `json:"updated_at"`
}

type Attempt struct {
	ID                 int64      `json:"id"`
	ExerciseID         string     `json:"exercise_id"`
	SessionID          string     `json:"session_id"`
	Variant            string     `json:"variant"`
	StartTime          time.Time  `json:"start_time"`
	EndTime            *time.Time `json:"end_time"`
	DurationSec        float64    `json:"duration_sec"`
	TimeToFirstTestSec float64    `json:"time_to_first_test_sec"`
	Status             string     `json:"status"` // "passed", "failed", "incomplete"
	TestRunsCount      int        `json:"test_runs_count"`
	BasicPassed        int        `json:"basic_passed"`
	EdgePassed         int        `json:"edge_passed"`
	StressPassed       int        `json:"stress_passed"`
	HintLevelUsed      int        `json:"hint_level_used"`
	ConfidenceRating   int        `json:"confidence_rating"`
	Mistakes           string     `json:"mistakes"`
	CreatedAt          time.Time  `json:"created_at"`
}

type MistakeLog struct {
	ID         int64     `json:"id"`
	AttemptID  int64     `json:"attempt_id"`
	ExerciseID string    `json:"exercise_id"`
	Category   string    `json:"category"`
	MistakeID  string    `json:"mistake_id"`
	Notes      string    `json:"notes"`
	LoggedAt   time.Time `json:"logged_at"`
}

type SavedAttempt struct {
	ID          int64     `json:"id"`
	ExerciseID  string    `json:"exercise_id"`
	Label       string    `json:"label"`
	CodeContent string    `json:"code_content"`
	SavedAt     time.Time `json:"saved_at"`
}

func InitDB(dbPath string) (*DB, error) {
	if err := os.MkdirAll(filepath.Dir(dbPath), 0755); err != nil {
		return nil, fmt.Errorf("failed to create db directory: %w", err)
	}

	conn, err := sql.Open("sqlite", dbPath)
	if err != nil {
		return nil, fmt.Errorf("failed to open database: %w", err)
	}

	// PRAGMA settings for performance and integrity
	if _, err := conn.Exec(`
		PRAGMA journal_mode = WAL;
		PRAGMA synchronous = NORMAL;
		PRAGMA busy_timeout = 5000;
	`); err != nil {
		conn.Close()
		return nil, fmt.Errorf("failed to configure sqlite pragma: %w", err)
	}

	database := &DB{Conn: conn}
	if err := database.migrate(); err != nil {
		conn.Close()
		return nil, fmt.Errorf("failed to run migrations: %w", err)
	}

	return database, nil
}

func (d *DB) Close() error {
	if d.Conn != nil {
		return d.Conn.Close()
	}
	return nil
}

func (d *DB) migrate() error {
	schema := `
	CREATE TABLE IF NOT EXISTS exercise_progress (
		exercise_id TEXT PRIMARY KEY,
		variant TEXT NOT NULL DEFAULT 'default',
		mastery_level INTEGER NOT NULL DEFAULT 1,
		total_attempts INTEGER NOT NULL DEFAULT 0,
		successful_attempts INTEGER NOT NULL DEFAULT 0,
		first_attempt_success BOOLEAN NOT NULL DEFAULT 0,
		avg_completion_time_sec REAL NOT NULL DEFAULT 0.0,
		best_completion_time_sec REAL NOT NULL DEFAULT 0.0,
		total_hints_used INTEGER NOT NULL DEFAULT 0,
		last_practice_at DATETIME,
		next_review_at DATETIME,
		interval_days INTEGER NOT NULL DEFAULT 1,
		streak INTEGER NOT NULL DEFAULT 0,
		followup_completed BOOLEAN NOT NULL DEFAULT 0,
		created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
		updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
	);

	CREATE TABLE IF NOT EXISTS attempts (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		exercise_id TEXT NOT NULL,
		session_id TEXT NOT NULL DEFAULT '',
		variant TEXT NOT NULL DEFAULT 'default',
		start_time DATETIME NOT NULL,
		end_time DATETIME,
		duration_sec REAL NOT NULL DEFAULT 0.0,
		time_to_first_test_sec REAL NOT NULL DEFAULT 0.0,
		status TEXT NOT NULL DEFAULT 'incomplete',
		test_runs_count INTEGER NOT NULL DEFAULT 0,
		basic_passed INTEGER NOT NULL DEFAULT 0,
		edge_passed INTEGER NOT NULL DEFAULT 0,
		stress_passed INTEGER NOT NULL DEFAULT 0,
		hint_level_used INTEGER NOT NULL DEFAULT 0,
		confidence_rating INTEGER NOT NULL DEFAULT 0,
		mistakes TEXT NOT NULL DEFAULT '',
		created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
	);

	CREATE TABLE IF NOT EXISTS mistake_logs (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		attempt_id INTEGER NOT NULL DEFAULT 0,
		exercise_id TEXT NOT NULL,
		category TEXT NOT NULL,
		mistake_id TEXT NOT NULL,
		notes TEXT NOT NULL DEFAULT '',
		logged_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
	);

	CREATE TABLE IF NOT EXISTS saved_attempts (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		exercise_id TEXT NOT NULL,
		label TEXT NOT NULL,
		code_content TEXT NOT NULL,
		saved_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
	);
	`
	_, err := d.Conn.Exec(schema)
	return err
}

func (d *DB) GetProgress(exerciseID string) (*ExerciseProgress, error) {
	row := d.Conn.QueryRow(`
		SELECT exercise_id, variant, mastery_level, total_attempts, successful_attempts,
		       first_attempt_success, avg_completion_time_sec, best_completion_time_sec,
		       total_hints_used, last_practice_at, next_review_at, interval_days,
		       streak, followup_completed, created_at, updated_at
		FROM exercise_progress
		WHERE exercise_id = ?
	`, exerciseID)

	p := &ExerciseProgress{}
	var lastPractice, nextReview sql.NullTime
	err := row.Scan(
		&p.ExerciseID, &p.Variant, &p.MasteryLevel, &p.TotalAttempts, &p.SuccessfulAttempts,
		&p.FirstAttemptSuccess, &p.AvgCompletionTimeSec, &p.BestCompletionTimeSec,
		&p.TotalHintsUsed, &lastPractice, &nextReview, &p.IntervalDays,
		&p.Streak, &p.FollowupCompleted, &p.CreatedAt, &p.UpdatedAt,
	)
	if err == sql.ErrNoRows {
		return &ExerciseProgress{
			ExerciseID:   exerciseID,
			Variant:      "default",
			MasteryLevel: 1, // Not Started
			IntervalDays: 1,
		}, nil
	}
	if err != nil {
		return nil, err
	}

	if lastPractice.Valid {
		p.LastPracticeAt = &lastPractice.Time
	}
	if nextReview.Valid {
		p.NextReviewAt = &nextReview.Time
	}
	return p, nil
}

func (d *DB) GetAllProgress() (map[string]*ExerciseProgress, error) {
	rows, err := d.Conn.Query(`
		SELECT exercise_id, variant, mastery_level, total_attempts, successful_attempts,
		       first_attempt_success, avg_completion_time_sec, best_completion_time_sec,
		       total_hints_used, last_practice_at, next_review_at, interval_days,
		       streak, followup_completed, created_at, updated_at
		FROM exercise_progress
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	results := make(map[string]*ExerciseProgress)
	for rows.Next() {
		p := &ExerciseProgress{}
		var lastPractice, nextReview sql.NullTime
		if err := rows.Scan(
			&p.ExerciseID, &p.Variant, &p.MasteryLevel, &p.TotalAttempts, &p.SuccessfulAttempts,
			&p.FirstAttemptSuccess, &p.AvgCompletionTimeSec, &p.BestCompletionTimeSec,
			&p.TotalHintsUsed, &lastPractice, &nextReview, &p.IntervalDays,
			&p.Streak, &p.FollowupCompleted, &p.CreatedAt, &p.UpdatedAt,
		); err != nil {
			return nil, err
		}
		if lastPractice.Valid {
			p.LastPracticeAt = &lastPractice.Time
		}
		if nextReview.Valid {
			p.NextReviewAt = &nextReview.Time
		}
		results[p.ExerciseID] = p
	}
	return results, nil
}

func (d *DB) SaveProgress(p *ExerciseProgress) error {
	now := time.Now().UTC()
	var lastPracticeVal, nextReviewVal *time.Time
	if p.LastPracticeAt != nil {
		t := p.LastPracticeAt.UTC()
		lastPracticeVal = &t
	}
	if p.NextReviewAt != nil {
		t := p.NextReviewAt.UTC()
		nextReviewVal = &t
	}

	query := `
		INSERT INTO exercise_progress (
			exercise_id, variant, mastery_level, total_attempts, successful_attempts,
			first_attempt_success, avg_completion_time_sec, best_completion_time_sec,
			total_hints_used, last_practice_at, next_review_at, interval_days,
			streak, followup_completed, created_at, updated_at
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		ON CONFLICT(exercise_id) DO UPDATE SET
			variant = excluded.variant,
			mastery_level = excluded.mastery_level,
			total_attempts = excluded.total_attempts,
			successful_attempts = excluded.successful_attempts,
			first_attempt_success = excluded.first_attempt_success,
			avg_completion_time_sec = excluded.avg_completion_time_sec,
			best_completion_time_sec = excluded.best_completion_time_sec,
			total_hints_used = excluded.total_hints_used,
			last_practice_at = excluded.last_practice_at,
			next_review_at = excluded.next_review_at,
			interval_days = excluded.interval_days,
			streak = excluded.streak,
			followup_completed = excluded.followup_completed,
			updated_at = excluded.updated_at
	`
	_, err := d.Conn.Exec(query,
		p.ExerciseID, p.Variant, p.MasteryLevel, p.TotalAttempts, p.SuccessfulAttempts,
		p.FirstAttemptSuccess, p.AvgCompletionTimeSec, p.BestCompletionTimeSec,
		p.TotalHintsUsed, lastPracticeVal, nextReviewVal, p.IntervalDays,
		p.Streak, p.FollowupCompleted, now, now,
	)
	return err
}

func (d *DB) RecordAttempt(a *Attempt) (int64, error) {
	now := time.Now().UTC()
	var endTimeVal *time.Time
	if a.EndTime != nil {
		t := a.EndTime.UTC()
		endTimeVal = &t
	}

	res, err := d.Conn.Exec(`
		INSERT INTO attempts (
			exercise_id, session_id, variant, start_time, end_time, duration_sec,
			time_to_first_test_sec, status, test_runs_count, basic_passed,
			edge_passed, stress_passed, hint_level_used, confidence_rating,
			mistakes, created_at
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	`,
		a.ExerciseID, a.SessionID, a.Variant, a.StartTime.UTC(), endTimeVal,
		a.DurationSec, a.TimeToFirstTestSec, a.Status, a.TestRunsCount,
		a.BasicPassed, a.EdgePassed, a.StressPassed, a.HintLevelUsed,
		a.ConfidenceRating, a.Mistakes, now,
	)
	if err != nil {
		return 0, err
	}
	return res.LastInsertId()
}

func (d *DB) LogMistake(m *MistakeLog) error {
	now := time.Now().UTC()
	_, err := d.Conn.Exec(`
		INSERT INTO mistake_logs (attempt_id, exercise_id, category, mistake_id, notes, logged_at)
		VALUES (?, ?, ?, ?, ?, ?)
	`, m.AttemptID, m.ExerciseID, m.Category, m.MistakeID, m.Notes, now)
	return err
}

func (d *DB) GetMistakeFrequency(category string) (map[string]int, error) {
	query := `SELECT mistake_id, COUNT(*) FROM mistake_logs`
	args := []any{}
	if category != "" {
		query += ` WHERE category = ?`
		args = append(args, category)
	}
	query += ` GROUP BY mistake_id ORDER BY COUNT(*) DESC`

	rows, err := d.Conn.Query(query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	counts := make(map[string]int)
	for rows.Next() {
		var id string
		var cnt int
		if err := rows.Scan(&id, &cnt); err != nil {
			return nil, err
		}
		counts[id] = cnt
	}
	return counts, nil
}

func (d *DB) SaveCodeAttempt(exerciseID, label, codeContent string) error {
	now := time.Now().UTC()
	_, err := d.Conn.Exec(`
		INSERT INTO saved_attempts (exercise_id, label, code_content, saved_at)
		VALUES (?, ?, ?, ?)
	`, exerciseID, label, codeContent, now)
	return err
}

func (d *DB) GetSavedAttempts(exerciseID string) ([]SavedAttempt, error) {
	rows, err := d.Conn.Query(`
		SELECT id, exercise_id, label, code_content, saved_at
		FROM saved_attempts
		WHERE exercise_id = ?
		ORDER BY saved_at DESC
	`, exerciseID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var list []SavedAttempt
	for rows.Next() {
		var s SavedAttempt
		if err := rows.Scan(&s.ID, &s.ExerciseID, &s.Label, &s.CodeContent, &s.SavedAt); err != nil {
			return nil, err
		}
		list = append(list, s)
	}
	return list, nil
}

func (d *DB) GetRecentAttempts(limit int) ([]Attempt, error) {
	rows, err := d.Conn.Query(`
		SELECT id, exercise_id, session_id, variant, start_time, end_time,
		       duration_sec, time_to_first_test_sec, status, test_runs_count,
		       basic_passed, edge_passed, stress_passed, hint_level_used,
		       confidence_rating, mistakes, created_at
		FROM attempts
		ORDER BY created_at DESC
		LIMIT ?
	`, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var attempts []Attempt
	for rows.Next() {
		var a Attempt
		var endTime sql.NullTime
		if err := rows.Scan(
			&a.ID, &a.ExerciseID, &a.SessionID, &a.Variant, &a.StartTime, &endTime,
			&a.DurationSec, &a.TimeToFirstTestSec, &a.Status, &a.TestRunsCount,
			&a.BasicPassed, &a.EdgePassed, &a.StressPassed, &a.HintLevelUsed,
			&a.ConfidenceRating, &a.Mistakes, &a.CreatedAt,
		); err != nil {
			return nil, err
		}
		if endTime.Valid {
			a.EndTime = &endTime.Time
		}
		attempts = append(attempts, a)
	}
	return attempts, nil
}
