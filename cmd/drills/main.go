package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/user/algorithm-drills/internal/app"
)

func findProjectRoot() string {
	// 1. Explicit DRILLS_HOME environment variable
	if env := os.Getenv("DRILLS_HOME"); env != "" {
		if fi, err := os.Stat(filepath.Join(env, "exercises", "metadata")); err == nil && fi.IsDir() {
			return env
		}
	}

	// 2. Check current working directory and walk up parent directories
	cwd, err := os.Getwd()
	if err == nil {
		curr := cwd
		for {
			if fi, err := os.Stat(filepath.Join(curr, "exercises", "metadata")); err == nil && fi.IsDir() {
				return curr
			}
			parent := filepath.Dir(curr)
			if parent == curr {
				break
			}
			curr = parent
		}
	}

	// 3. Check executable relative path (e.g. if installed in <root>/bin/drills)
	if exe, err := os.Executable(); err == nil {
		exeDir := filepath.Dir(exe)
		candidate := filepath.Clean(filepath.Join(exeDir, ".."))
		if fi, err := os.Stat(filepath.Join(candidate, "exercises", "metadata")); err == nil && fi.IsDir() {
			return candidate
		}
	}

	// 4. Saved project root marker at ~/.config/drills/root
	if home, err := os.UserHomeDir(); err == nil {
		rootFile := filepath.Join(home, ".config", "drills", "root")
		if data, err := os.ReadFile(rootFile); err == nil {
			path := strings.TrimSpace(string(data))
			if fi, err := os.Stat(filepath.Join(path, "exercises", "metadata")); err == nil && fi.IsDir() {
				return path
			}
		}
	}

	if cwd != "" {
		return cwd
	}
	return "."
}

func main() {
	projectRoot := findProjectRoot()

	application, err := app.NewApp(projectRoot)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error initializing application: %v\n", err)
		os.Exit(1)
	}
	defer application.Close()

	if err := application.RootCmd.Execute(); err != nil {
		os.Exit(1)
	}
}
