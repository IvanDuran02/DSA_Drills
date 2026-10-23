package config

import (
	"os"
	"path/filepath"

	"gopkg.in/yaml.v3"
)

type Config struct {
	Practice  PracticeConfig  `yaml:"practice"`
	Reviews   ReviewsConfig   `yaml:"reviews"`
	Testing   TestingConfig   `yaml:"testing"`
	Interface InterfaceConfig `yaml:"interface"`
	Python    PythonConfig    `yaml:"python"`
}

type PracticeConfig struct {
	DefaultSessionMinutes int    `yaml:"default_session_minutes"`
	DefaultHintLevel      int    `yaml:"default_hint_level"`
	Editor                string `yaml:"editor"`
	PreferredLanguage     string `yaml:"preferred_language"`
}

type ReviewsConfig struct {
	IntervalsDays []int `yaml:"intervals_days"`
}

type TestingConfig struct {
	DefaultLevel       string `yaml:"default_level"`
	TimeoutSeconds     int    `yaml:"timeout_seconds"`
	HypothesisExamples int    `yaml:"hypothesis_examples"`
}

type InterfaceConfig struct {
	Theme                  string `yaml:"theme"`
	ShowComplexityTargets  bool   `yaml:"show_complexity_targets"`
}

type PythonConfig struct {
	VenvPath   string `yaml:"venv_path"`
	PythonPath string `yaml:"python_path"`
}

func DefaultConfig() *Config {
	editor := os.Getenv("EDITOR")
	if editor == "" {
		editor = "vim"
	}

	return &Config{
		Practice: PracticeConfig{
			DefaultSessionMinutes: 60,
			DefaultHintLevel:      0,
			Editor:                editor,
			PreferredLanguage:     "python",
		},
		Reviews: ReviewsConfig{
			IntervalsDays: []int{1, 3, 7, 14},
		},
		Testing: TestingConfig{
			DefaultLevel:       "edge",
			TimeoutSeconds:     15,
			HypothesisExamples: 100,
		},
		Interface: InterfaceConfig{
			Theme:                 "default",
			ShowComplexityTargets: true,
		},
		Python: PythonConfig{
			VenvPath:   ".venv",
			PythonPath: "",
		},
	}
}

// LoadConfig attempts to read config from .drills/config.yaml or returns default config.
func LoadConfig(projectRoot string) (*Config, error) {
	cfg := DefaultConfig()

	paths := []string{
		filepath.Join(projectRoot, ".drills", "config.yaml"),
		filepath.Join(os.Getenv("HOME"), ".config", "drills", "config.yaml"),
	}

	for _, p := range paths {
		data, err := os.ReadFile(p)
		if err == nil {
			if err := yaml.Unmarshal(data, cfg); err == nil {
				return cfg, nil
			}
		}
	}

	return cfg, nil
}
