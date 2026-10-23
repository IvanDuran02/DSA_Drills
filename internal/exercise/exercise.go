package exercise

import (
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strings"

	"gopkg.in/yaml.v3"
)

type TargetComplexity struct {
	Time  string `yaml:"time"`
	Space string `yaml:"space"`
}

type Followup struct {
	ID            string `yaml:"id"`
	Title         string `yaml:"title"`
	Description   string `yaml:"description"`
	StarterPath   string `yaml:"starter_path"`
	TestPath      string `yaml:"test_path"`
	ReferencePath string `yaml:"reference_path"`
}

type Exercise struct {
	ID                 string            `yaml:"id"`
	Name               string            `yaml:"name"`
	Category           string            `yaml:"category"`
	Difficulty         string            `yaml:"difficulty"` // Easy, Medium, Hard
	Level              int               `yaml:"level"`      // 1: Template, 2: Implementation, 3: Application
	RecommendedMinutes int               `yaml:"recommended_minutes"`
	TargetComplexity   TargetComplexity  `yaml:"target_complexity"`
	FunctionSignature  string            `yaml:"function_signature"`
	StarterPath        string            `yaml:"starter_path"`
	TestPath           string            `yaml:"test_path"`
	ReferencePath      string            `yaml:"reference_path"`
	Description        string            `yaml:"description"`
	Hints              map[int]string    `yaml:"hints"`
	Variants           []string          `yaml:"variants"`
	Followup           *Followup         `yaml:"followup,omitempty"`
}

type ExerciseRegistry struct {
	exercises map[string]*Exercise
}

func LoadRegistry(metadataDir string) (*ExerciseRegistry, error) {
	reg := &ExerciseRegistry{
		exercises: make(map[string]*Exercise),
	}

	entries, err := os.ReadDir(metadataDir)
	if err != nil {
		return nil, fmt.Errorf("failed to read metadata dir %s: %w", metadataDir, err)
	}

	for _, entry := range entries {
		if entry.IsDir() || (!strings.HasSuffix(entry.Name(), ".yaml") && !strings.HasSuffix(entry.Name(), ".yml")) {
			continue
		}

		filePath := filepath.Join(metadataDir, entry.Name())
		data, err := os.ReadFile(filePath)
		if err != nil {
			return nil, fmt.Errorf("failed to read exercise file %s: %w", filePath, err)
		}

		var ex Exercise
		if err := yaml.Unmarshal(data, &ex); err != nil {
			return nil, fmt.Errorf("failed to parse yaml in %s: %w", filePath, err)
		}

		if err := Validate(&ex); err != nil {
			return nil, fmt.Errorf("invalid exercise in %s: %w", filePath, err)
		}

		reg.exercises[ex.ID] = &ex
	}

	return reg, nil
}

func Validate(e *Exercise) error {
	if e.ID == "" {
		return fmt.Errorf("exercise ID cannot be empty")
	}
	if e.Name == "" {
		return fmt.Errorf("exercise Name cannot be empty")
	}
	if e.Category == "" {
		return fmt.Errorf("exercise Category cannot be empty")
	}
	if e.StarterPath == "" {
		return fmt.Errorf("exercise StarterPath cannot be empty")
	}
	if e.TestPath == "" {
		return fmt.Errorf("exercise TestPath cannot be empty")
	}
	if e.ReferencePath == "" {
		return fmt.Errorf("exercise ReferencePath cannot be empty")
	}
	if e.RecommendedMinutes <= 0 {
		e.RecommendedMinutes = 10
	}
	return nil
}

func (r *ExerciseRegistry) Get(id string) (*Exercise, bool) {
	ex, ok := r.exercises[id]
	return ex, ok
}

func (r *ExerciseRegistry) All() []*Exercise {
	list := make([]*Exercise, 0, len(r.exercises))
	for _, ex := range r.exercises {
		list = append(list, ex)
	}
	sort.Slice(list, func(i, j int) bool {
		if list[i].Category != list[j].Category {
			return list[i].Category < list[j].Category
		}
		return list[i].ID < list[j].ID
	})
	return list
}

func (r *ExerciseRegistry) FilterByCategory(category string) []*Exercise {
	var list []*Exercise
	catLower := strings.ToLower(category)
	for _, ex := range r.exercises {
		if strings.ToLower(ex.Category) == catLower {
			list = append(list, ex)
		}
	}
	sort.Slice(list, func(i, j int) bool {
		return list[i].ID < list[j].ID
	})
	return list
}

func (r *ExerciseRegistry) Categories() []string {
	catMap := make(map[string]bool)
	for _, ex := range r.exercises {
		catMap[ex.Category] = true
	}
	cats := make([]string, 0, len(catMap))
	for c := range catMap {
		cats = append(cats, c)
	}
	sort.Strings(cats)
	return cats
}

func (r *ExerciseRegistry) Count() int {
	return len(r.exercises)
}
