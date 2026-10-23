package runner

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/user/algorithm-drills/internal/config"
)

type TestCaseResult struct {
	Name            string  `json:"name"`
	Level           string  `json:"level"`
	Status          string  `json:"status"` // "passed", "failed", "error", "skipped", "unimplemented"
	DurationMs      float64 `json:"duration_ms"`
	Message         string  `json:"message"`
	IsUnimplemented bool    `json:"is_unimplemented"`
}

type TestReport struct {
	ExerciseID      string           `json:"exercise_id"`
	Level           string           `json:"level"`
	Total           int              `json:"total"`
	Passed          int              `json:"passed"`
	Failed          int              `json:"failed"`
	Errors          int              `json:"errors"`
	Skipped         int              `json:"skipped"`
	Unimplemented   int              `json:"unimplemented"`
	IsUnimplemented bool             `json:"is_unimplemented"`
	DurationMs      float64          `json:"duration_ms"`
	Tests           []TestCaseResult `json:"tests"`
}

type PythonRunner struct {
	ProjectRoot string
	Config      *config.Config
	PythonPath  string
}

func NewPythonRunner(projectRoot string, cfg *config.Config) (*PythonRunner, error) {
	runner := &PythonRunner{
		ProjectRoot: projectRoot,
		Config:      cfg,
	}

	pyPath, err := runner.locatePython()
	if err != nil {
		return nil, err
	}
	runner.PythonPath = pyPath
	return runner, nil
}

func (r *PythonRunner) locatePython() (string, error) {
	// 1. If explicit path in config
	if r.Config.Python.PythonPath != "" {
		if _, err := os.Stat(r.Config.Python.PythonPath); err == nil {
			return r.Config.Python.PythonPath, nil
		}
	}

	// 2. Check virtualenv
	venvDirs := []string{
		filepath.Join(r.ProjectRoot, r.Config.Python.VenvPath, "bin", "python3"),
		filepath.Join(r.ProjectRoot, r.Config.Python.VenvPath, "bin", "python"),
		filepath.Join(r.ProjectRoot, ".venv", "bin", "python3"),
		filepath.Join(r.ProjectRoot, ".venv", "bin", "python"),
	}
	for _, p := range venvDirs {
		if fi, err := os.Stat(p); err == nil && !fi.IsDir() {
			return p, nil
		}
	}

	// 3. Check system PATH for python3.14
	if path, err := exec.LookPath("python3.14"); err == nil {
		return path, nil
	}

	// 4. Check system python3 version
	if path, err := exec.LookPath("python3"); err == nil {
		out, err := exec.Command(path, "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')").Output()
		if err == nil {
			ver := strings.TrimSpace(string(out))
			if strings.HasPrefix(ver, "3.14") || strings.HasPrefix(ver, "3.15") {
				return path, nil
			}
		}
	}

	return "", fmt.Errorf("Python 3.14+ not found. Please create a virtual environment in .venv with Python 3.14 or run 'make setup'")
}

func (r *PythonRunner) RunTests(
	ctx context.Context,
	exerciseID string,
	testFileRel string,
	target string, // "student" or "reference"
	level string,  // "all", "basic", "edge", "stress"
	implFileRel string,
	timeoutSec int,
) (*TestReport, error) {
	if timeoutSec <= 0 {
		timeoutSec = r.Config.Testing.TimeoutSeconds
		if timeoutSec <= 0 {
			timeoutSec = 15
		}
	}

	testFileAbs := filepath.Join(r.ProjectRoot, testFileRel)
	if _, err := os.Stat(testFileAbs); err != nil {
		return nil, fmt.Errorf("test file not found: %s", testFileAbs)
	}

	runnerScriptAbs := filepath.Join(r.ProjectRoot, "test_runner", "runner.py")
	if _, err := os.Stat(runnerScriptAbs); err != nil {
		return nil, fmt.Errorf("runner script not found: %s", runnerScriptAbs)
	}

	args := []string{
		runnerScriptAbs,
		"--exercise", exerciseID,
		"--test-file", testFileAbs,
		"--target", target,
		"--level", level,
	}

	if implFileRel != "" {
		implAbs := filepath.Join(r.ProjectRoot, implFileRel)
		args = append(args, "--impl-file", implAbs)
	}

	ctxTimeout, cancel := context.WithTimeout(ctx, time.Duration(timeoutSec)*time.Second)
	defer cancel()

	cmd := exec.CommandContext(ctxTimeout, r.PythonPath, args...)
	cmd.Dir = r.ProjectRoot

	// Set PYTHONPATH to include project root so imports like `tests.loader` work smoothly
	cmd.Env = append(os.Environ(),
		fmt.Sprintf("PYTHONPATH=%s", r.ProjectRoot),
		"PYTHONDONTWRITEBYTECODE=1",
	)

	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	err := cmd.Run()
	if errors.Is(ctxTimeout.Err(), context.DeadlineExceeded) {
		return nil, fmt.Errorf("test execution timed out after %d seconds (possible infinite loop)", timeoutSec)
	}

	output := stdout.String()
	// Extract JSON between markers
	startMarker := "===DRILLS_JSON_START==="
	endMarker := "===DRILLS_JSON_END==="

	startIdx := strings.Index(output, startMarker)
	endIdx := strings.Index(output, endMarker)

	if startIdx == -1 || endIdx == -1 || startIdx >= endIdx {
		// Output did not contain json markers; error out with stderr and stdout snippet
		return nil, fmt.Errorf("failed to parse structured test output.\nSTDOUT: %s\nSTDERR: %s\nERR: %v",
			strings.TrimSpace(output), strings.TrimSpace(stderr.String()), err)
	}

	jsonBytes := []byte(strings.TrimSpace(output[startIdx+len(startMarker) : endIdx]))
	var report TestReport
	if err := json.Unmarshal(jsonBytes, &report); err != nil {
		return nil, fmt.Errorf("failed to unmarshal test JSON: %w (raw output: %s)", err, string(jsonBytes))
	}

	return &report, nil
}
