package session

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"time"
)

type ActiveSession struct {
	ExerciseID         string    `json:"exercise_id"`
	SessionID          string    `json:"session_id"`
	Variant            string    `json:"variant"`
	StartTime          time.Time `json:"start_time"`
	TimeToFirstTestSec float64   `json:"time_to_first_test_sec"`
	TestRunsCount      int       `json:"test_runs_count"`
	BasicPassed        int       `json:"basic_passed"`
	EdgePassed         int       `json:"edge_passed"`
	StressPassed       int       `json:"stress_passed"`
	HintLevelUsed      int       `json:"hint_level_used"`
	LastTestedAt       time.Time `json:"last_tested_at"`
}

func GetSessionFilePath(projectRoot string) string {
	return filepath.Join(projectRoot, ".drills", "active_session.json")
}

func LoadActiveSession(projectRoot string) (*ActiveSession, error) {
	path := GetSessionFilePath(projectRoot)
	data, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			return nil, nil
		}
		return nil, err
	}

	var s ActiveSession
	if err := json.Unmarshal(data, &s); err != nil {
		return nil, err
	}
	return &s, nil
}

func SaveActiveSession(projectRoot string, s *ActiveSession) error {
	path := GetSessionFilePath(projectRoot)
	if err := os.MkdirAll(filepath.Dir(path), 0755); err != nil {
		return err
	}
	data, err := json.MarshalIndent(s, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(path, data, 0644)
}

func ClearActiveSession(projectRoot string) error {
	path := GetSessionFilePath(projectRoot)
	if err := os.Remove(path); err != nil && !os.IsNotExist(err) {
		return err
	}
	return nil
}

func StartSession(projectRoot, exerciseID, variant string) (*ActiveSession, error) {
	s := &ActiveSession{
		ExerciseID: exerciseID,
		SessionID:  fmt.Sprintf("sess_%d", time.Now().Unix()),
		Variant:    variant,
		StartTime:  time.Now().UTC(),
	}
	if err := SaveActiveSession(projectRoot, s); err != nil {
		return nil, err
	}
	return s, nil
}

func RecordTestRun(projectRoot string, basicPassed, edgePassed, stressPassed int) (*ActiveSession, error) {
	s, err := LoadActiveSession(projectRoot)
	if err != nil || s == nil {
		return nil, err
	}

	now := time.Now().UTC()
	s.TestRunsCount++
	if s.TimeToFirstTestSec == 0 {
		s.TimeToFirstTestSec = now.Sub(s.StartTime).Seconds()
	}
	s.BasicPassed = basicPassed
	s.EdgePassed = edgePassed
	s.StressPassed = stressPassed
	s.LastTestedAt = now

	if err := SaveActiveSession(projectRoot, s); err != nil {
		return nil, err
	}
	return s, nil
}
