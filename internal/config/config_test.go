package config_test

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/user/algorithm-drills/internal/config"
)

func TestDefaultConfig(t *testing.T) {
	cfg := config.DefaultConfig()
	if cfg.Practice.DefaultSessionMinutes != 60 {
		t.Fatalf("expected 60, got %d", cfg.Practice.DefaultSessionMinutes)
	}
	if len(cfg.Reviews.IntervalsDays) != 4 {
		t.Fatalf("expected 4 intervals, got %d", len(cfg.Reviews.IntervalsDays))
	}
	if cfg.Testing.DefaultLevel != "edge" {
		t.Fatalf("expected edge, got %s", cfg.Testing.DefaultLevel)
	}
}

func TestLoadConfig(t *testing.T) {
	tmpDir := t.TempDir()
	drillsDir := filepath.Join(tmpDir, ".drills")
	if err := os.MkdirAll(drillsDir, 0755); err != nil {
		t.Fatal(err)
	}

	yamlData := `
practice:
  default_session_minutes: 45
reviews:
  intervals_days: [1, 2, 5, 10]
`
	if err := os.WriteFile(filepath.Join(drillsDir, "config.yaml"), []byte(yamlData), 0644); err != nil {
		t.Fatal(err)
	}

	cfg, err := config.LoadConfig(tmpDir)
	if err != nil {
		t.Fatalf("failed to load config: %v", err)
	}
	if cfg.Practice.DefaultSessionMinutes != 45 {
		t.Fatalf("expected 45 minutes, got %d", cfg.Practice.DefaultSessionMinutes)
	}
	if len(cfg.Reviews.IntervalsDays) != 4 || cfg.Reviews.IntervalsDays[1] != 2 {
		t.Fatalf("expected interval [1, 2, 5, 10], got %v", cfg.Reviews.IntervalsDays)
	}
}
