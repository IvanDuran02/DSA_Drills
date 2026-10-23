package doctor

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"

	"github.com/user/algorithm-drills/internal/config"
	"github.com/user/algorithm-drills/internal/db"
	"github.com/user/algorithm-drills/internal/exercise"
	"github.com/user/algorithm-drills/internal/runner"
	"github.com/user/algorithm-drills/internal/ui"
)

type CheckResult struct {
	Name    string
	Passed  bool
	Message string
}

func RunDoctor(projectRoot string, cfg *config.Config) []CheckResult {
	var results []CheckResult

	// 1. Host and Architecture
	results = append(results, CheckResult{
		Name:    "Host Architecture",
		Passed:  true,
		Message: fmt.Sprintf("OS: %s, Arch: %s, Go Runtime: %s", runtime.GOOS, runtime.GOARCH, runtime.Version()),
	})

	// 2. Python 3.14+ detection
	pyRunner, err := runner.NewPythonRunner(projectRoot, cfg)
	if err != nil {
		results = append(results, CheckResult{
			Name:    "Python 3.14+ Installation",
			Passed:  false,
			Message: fmt.Sprintf("Failed to locate Python 3.14+: %v", err),
		})
		return results
	}

	cmdVer := exec.Command(pyRunner.PythonPath, "--version")
	outVer, err := cmdVer.Output()
	if err != nil {
		results = append(results, CheckResult{
			Name:    "Python Interpreter Execution",
			Passed:  false,
			Message: fmt.Sprintf("Failed to run %s: %v", pyRunner.PythonPath, err),
		})
	} else {
		verStr := strings.TrimSpace(string(outVer))
		is314 := strings.Contains(verStr, "3.14") || strings.Contains(verStr, "3.15")
		results = append(results, CheckResult{
			Name:    "Python Interpreter Version",
			Passed:  is314,
			Message: fmt.Sprintf("%s (%s)", verStr, pyRunner.PythonPath),
		})
	}

	// 3. Python 3.14 Native max-heap APIs
	maxHeapCheck := `
import sys, heapq
required = ['heappush_max', 'heappop_max', 'heapify_max', 'heappushpop_max', 'heapreplace_max']
missing = [fn for fn in required if not hasattr(heapq, fn)]
if missing:
    print('Missing: ' + ', '.join(missing))
    sys.exit(1)
print('All 5 native max-heap APIs supported')
`
	cmdHeap := exec.Command(pyRunner.PythonPath, "-c", maxHeapCheck)
	outHeap, err := cmdHeap.CombinedOutput()
	if err != nil {
		results = append(results, CheckResult{
			Name:    "Python 3.14 Native Max-Heap APIs",
			Passed:  false,
			Message: fmt.Sprintf("heapq max-heap check failed: %s", strings.TrimSpace(string(outHeap))),
		})
	} else {
		results = append(results, CheckResult{
			Name:    "Python 3.14 Native Max-Heap APIs",
			Passed:  true,
			Message: strings.TrimSpace(string(outHeap)),
		})
	}

	// 4. Required Python Packages
	pkgCheck := `
import sys
packages = ['pytest', 'hypothesis', 'pytest_timeout', 'yaml']
missing = []
for p in packages:
    try:
        __import__(p)
    except ImportError:
        missing.append(p)
if missing:
    print('Missing packages: ' + ', '.join(missing))
    sys.exit(1)
print('pytest, hypothesis, pytest-timeout, pyyaml installed')
`
	cmdPkg := exec.Command(pyRunner.PythonPath, "-c", pkgCheck)
	outPkg, err := cmdPkg.CombinedOutput()
	if err != nil {
		results = append(results, CheckResult{
			Name:    "Python Dependencies",
			Passed:  false,
			Message: strings.TrimSpace(string(outPkg)),
		})
	} else {
		results = append(results, CheckResult{
			Name:    "Python Dependencies",
			Passed:  true,
			Message: strings.TrimSpace(string(outPkg)),
		})
	}

	// 5. Exercise Metadata Registry
	metaDir := filepath.Join(projectRoot, "exercises", "metadata")
	reg, err := exercise.LoadRegistry(metaDir)
	if err != nil {
		results = append(results, CheckResult{
			Name:    "Exercise Metadata Library",
			Passed:  false,
			Message: fmt.Sprintf("Failed loading metadata: %v", err),
		})
	} else {
		results = append(results, CheckResult{
			Name:    "Exercise Metadata Library",
			Passed:  true,
			Message: fmt.Sprintf("%d exercises loaded across %d categories", reg.Count(), len(reg.Categories())),
		})
	}

	// 6. SQLite Database Health & Integrity
	dbPath := filepath.Join(projectRoot, ".drills", "progress.db")
	database, err := db.InitDB(dbPath)
	if err != nil {
		results = append(results, CheckResult{
			Name:    "SQLite Database Health",
			Passed:  false,
			Message: fmt.Sprintf("Failed opening DB at %s: %v", dbPath, err),
		})
	} else {
		var integrity string
		row := database.Conn.QueryRow("PRAGMA integrity_check;")
		if err := row.Scan(&integrity); err != nil || integrity != "ok" {
			results = append(results, CheckResult{
				Name:    "SQLite Database Health",
				Passed:  false,
				Message: fmt.Sprintf("Database integrity check failed: %s (%v)", integrity, err),
			})
		} else {
			results = append(results, CheckResult{
				Name:    "SQLite Database Health",
				Passed:  true,
				Message: fmt.Sprintf("Database OK at %s (integrity: ok)", dbPath),
			})
		}
		_ = database.Close()
	}

	// 7. Structured Test Runner Script
	runnerPath := filepath.Join(projectRoot, "test_runner", "runner.py")
	if fi, err := os.Stat(runnerPath); err != nil || fi.IsDir() {
		results = append(results, CheckResult{
			Name:    "Test Runner Infrastructure",
			Passed:  false,
			Message: fmt.Sprintf("runner.py missing at %s", runnerPath),
		})
	} else {
		results = append(results, CheckResult{
			Name:    "Test Runner Infrastructure",
			Passed:  true,
			Message: fmt.Sprintf("Structured JSON test runner present at %s", runnerPath),
		})
	}

	return results
}

func PrintDoctorReport(results []CheckResult) bool {
	allPassed := true
	fmt.Println()
	fmt.Println(ui.TitleStyle.Render("ALGORITHM DRILLS — SYSTEM DOCTOR"))
	fmt.Println(ui.Divider(65))

	for _, res := range results {
		var icon string
		if res.Passed {
			icon = ui.SuccessStyle.Render("✔")
		} else {
			icon = ui.DangerStyle.Render("✖")
			allPassed = false
		}
		fmt.Printf(" %s  %-32s : %s\n", icon, res.Name, res.Message)
	}

	fmt.Println(ui.Divider(65))
	if allPassed {
		fmt.Println(ui.SuccessStyle.Render("All system health checks passed! Environment is ready for interview practice."))
	} else {
		fmt.Println(ui.DangerStyle.Render("One or more checks failed. Please review issues above."))
	}
	fmt.Println()
	return allPassed
}
