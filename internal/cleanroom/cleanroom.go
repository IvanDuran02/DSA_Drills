package cleanroom

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/user/algorithm-drills/internal/db"
	"github.com/user/algorithm-drills/internal/exercise"
)

func BackupAndReset(
	projectRoot string,
	ex *exercise.Exercise,
	database *db.DB,
	cleanTemplate string,
) (string, error) {
	starterAbs := filepath.Join(projectRoot, ex.StarterPath)

	// Check if current file has code to backup
	currentCode, err := os.ReadFile(starterAbs)
	if err == nil && len(strings.TrimSpace(string(currentCode))) > 0 {
		codeStr := string(currentCode)
		// Only backup if it contains something more than the default raise NotImplementedError
		if !strings.Contains(codeStr, "raise NotImplementedError") || len(strings.TrimSpace(codeStr)) > 200 {
			timestamp := time.Now().UTC().Format("20060102_150405")
			backupDir := filepath.Join(projectRoot, ".drills", "backups", ex.ID)
			if err := os.MkdirAll(backupDir, 0755); err != nil {
				return "", fmt.Errorf("failed to create backup dir: %w", err)
			}
			backupFile := filepath.Join(backupDir, fmt.Sprintf("%s.py", timestamp))
			if err := os.WriteFile(backupFile, currentCode, 0644); err != nil {
				return "", fmt.Errorf("failed to write backup file: %w", err)
			}

			// Also persist to SQLite
			if database != nil {
				_ = database.SaveCodeAttempt(ex.ID, fmt.Sprintf("Backup %s", timestamp), codeStr)
			}
		}
	}

	// Write clean template
	if err := os.MkdirAll(filepath.Dir(starterAbs), 0755); err != nil {
		return "", fmt.Errorf("failed to create starter file directory: %w", err)
	}

	if err := os.WriteFile(starterAbs, []byte(cleanTemplate), 0644); err != nil {
		return "", fmt.Errorf("failed to write clean starter template: %w", err)
	}

	return starterAbs, nil
}

func RecoverAttempt(
	projectRoot string,
	ex *exercise.Exercise,
	database *db.DB,
	attemptID int64,
) error {
	starterAbs := filepath.Join(projectRoot, ex.StarterPath)

	saved, err := database.GetSavedAttempts(ex.ID)
	if err != nil {
		return err
	}

	var target *db.SavedAttempt
	for _, s := range saved {
		if s.ID == attemptID {
			target = &s
			break
		}
	}
	if target == nil {
		return fmt.Errorf("saved attempt #%d not found for exercise %s", attemptID, ex.ID)
	}

	// Backup current before overwriting
	currentCode, err := os.ReadFile(starterAbs)
	if err == nil && len(currentCode) > 0 {
		timestamp := time.Now().UTC().Format("20060102_150405")
		_ = database.SaveCodeAttempt(ex.ID, fmt.Sprintf("Pre-recover %s", timestamp), string(currentCode))
	}

	return os.WriteFile(starterAbs, []byte(target.CodeContent), 0644)
}
