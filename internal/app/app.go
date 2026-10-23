package app

import (
	"bufio"
	"context"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
	"github.com/spf13/cobra"
	"github.com/user/algorithm-drills/internal/cleanroom"
	"github.com/user/algorithm-drills/internal/config"
	"github.com/user/algorithm-drills/internal/db"
	"github.com/user/algorithm-drills/internal/doctor"
	"github.com/user/algorithm-drills/internal/exercise"
	"github.com/user/algorithm-drills/internal/mistakes"
	"github.com/user/algorithm-drills/internal/runner"
	"github.com/user/algorithm-drills/internal/scheduler"
	"github.com/user/algorithm-drills/internal/session"
	"github.com/user/algorithm-drills/internal/tui"
	"github.com/user/algorithm-drills/internal/ui"
)

type App struct {
	ProjectRoot string
	Config      *config.Config
	DB          *db.DB
	Registry    *exercise.ExerciseRegistry
	RootCmd     *cobra.Command
}

func NewApp(projectRoot string) (*App, error) {
	cfg, err := config.LoadConfig(projectRoot)
	if err != nil {
		return nil, fmt.Errorf("config error: %w", err)
	}

	dbPath := filepath.Join(projectRoot, ".drills", "progress.db")
	database, err := db.InitDB(dbPath)
	if err != nil {
		return nil, fmt.Errorf("db error: %w", err)
	}

	metaDir := filepath.Join(projectRoot, "exercises", "metadata")
	reg, err := exercise.LoadRegistry(metaDir)
	if err != nil {
		// Registry could be empty initially, which is fine
		reg = &exercise.ExerciseRegistry{}
	}

	app := &App{
		ProjectRoot: projectRoot,
		Config:      cfg,
		DB:          database,
		Registry:    reg,
	}

	app.initCommands()
	return app, nil
}

func (a *App) Close() {
	if a.DB != nil {
		_ = a.DB.Close()
	}
}

func (a *App) initCommands() {
	a.RootCmd = &cobra.Command{
		Use:   "drills",
		Short: "Algorithm Drills — Google SWE Interview Training System",
		Long: lipgloss.NewStyle().Foreground(ui.ColorPrimary).Bold(true).Render(
			"⚡ Algorithm Drills: Fast, standalone native algorithm implementation gym for Google SWE prep.",
		),
		RunE: func(cmd *cobra.Command, args []string) error {
			// Launch the interactive Bubble Tea TUI when run with no arguments
			m := tui.NewModel(a.ProjectRoot, a.Config, a.DB, a.Registry)
			p := tea.NewProgram(m, tea.WithAltScreen())
			_, err := p.Run()
			return err
		},
	}

	a.RootCmd.AddCommand(
		a.newListCmd(),
		a.newShowCmd(),
		a.newStartCmd(),
		a.newTestCmd(),
		a.newFinishCmd(),
		a.newResetCmd(),
		a.newRecoverCmd(),
		a.newProgressCmd(),
		a.newStatsCmd(),
		a.newTodayCmd(),
		a.newReviewCmd(),
		a.newSessionCmd(),
		a.newFollowupCmd(),
		a.newMistakesCmd(),
		a.newHintCmd(),
		a.newDoctorCmd(),
	)
}

func (a *App) newListCmd() *cobra.Command {
	var category string
	cmd := &cobra.Command{
		Use:   "list",
		Short: "List all algorithm drills and their mastery status",
		RunE: func(cmd *cobra.Command, args []string) error {
			allProgress, err := a.DB.GetAllProgress()
			if err != nil {
				return err
			}

			var exercises []*exercise.Exercise
			if category != "" {
				exercises = a.Registry.FilterByCategory(category)
			} else {
				exercises = a.Registry.All()
			}

			fmt.Println()
			fmt.Println(ui.TitleStyle.Render("ALGORITHM DRILLS — EXERCISE LIBRARY"))
			fmt.Println(ui.Divider(80))
			fmt.Printf(" %-24s %-16s %-8s %-6s %-18s\n", "ID", "CATEGORY", "DIFF", "TIME", "MASTERY")
			fmt.Println(ui.Divider(80))

			for _, ex := range exercises {
				p := allProgress[ex.ID]
				mastery := 1
				if p != nil {
					mastery = p.MasteryLevel
				}

				fmt.Printf(" %-24s %-16s %-8s %2d min %-18s\n",
					ex.ID,
					ex.Category,
					ui.DifficultyBadge(ex.Difficulty),
					ex.RecommendedMinutes,
					ui.MasteryBadge(mastery),
				)
			}
			fmt.Println(ui.Divider(80))
			fmt.Printf(" Total: %d exercises\n\n", len(exercises))
			return nil
		},
	}
	cmd.Flags().StringVarP(&category, "category", "c", "", "Filter exercises by category")
	return cmd
}

func (a *App) newShowCmd() *cobra.Command {
	return &cobra.Command{
		Use:   "show <exercise-id>",
		Short: "Display detailed specification and status for an exercise",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			id := args[0]
			ex, ok := a.Registry.Get(id)
			if !ok {
				return fmt.Errorf("exercise '%s' not found. Run 'drills list' to view available exercises", id)
			}

			p, err := a.DB.GetProgress(id)
			if err != nil {
				return err
			}

			nextReviewStr := "None"
			if p.NextReviewAt != nil {
				nextReviewStr = p.NextReviewAt.Format("2006-01-02 15:04 UTC")
			}
			lastPracticeStr := "Never"
			if p.LastPracticeAt != nil {
				lastPracticeStr = p.LastPracticeAt.Format("2006-01-02 15:04 UTC")
			}

			fmt.Println()
			cardContent := fmt.Sprintf(
				"%s\n%s\n"+
					"Exercise:       %s\n"+
					"Category:       %s\n"+
					"Difficulty:     %s\n"+
					"Level:          Level %d\n"+
					"Target Time:    %s\n"+
					"Target Space:   %s\n"+
					"Recommended:    %d minutes\n\n"+
					"Status:         %s\n"+
					"Attempts:       %d (%d passed, streak: %d)\n"+
					"Last Attempt:   %s\n"+
					"Next Review:    %s\n\n"+
					"Starter File:   %s\n"+
					"Test File:      %s\n\n"+
					"Specification:\n%s\n",
				ui.TitleStyle.Render("ALGORITHM DRILLS"),
				ui.Divider(60),
				ex.Name,
				ex.Category,
				ui.DifficultyBadge(ex.Difficulty),
				ex.Level,
				ex.TargetComplexity.Time,
				ex.TargetComplexity.Space,
				ex.RecommendedMinutes,
				ui.MasteryBadge(p.MasteryLevel),
				p.TotalAttempts,
				p.SuccessfulAttempts,
				p.Streak,
				lastPracticeStr,
				nextReviewStr,
				ex.StarterPath,
				ex.TestPath,
				strings.TrimSpace(ex.Description),
			)
			fmt.Println(ui.CardStyle.Render(cardContent))
			return nil
		},
	}
}

func (a *App) newStartCmd() *cobra.Command {
	var fresh bool
	var variant string
	cmd := &cobra.Command{
		Use:   "start <exercise-id>",
		Short: "Start a timed practice session for an exercise",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			id := args[0]
			ex, ok := a.Registry.Get(id)
			if !ok {
				return fmt.Errorf("exercise '%s' not found", id)
			}

			if variant == "" {
				variant = "default"
			}

			if fresh {
				// Clean-room reset
				starterAbs, err := cleanroom.BackupAndReset(a.ProjectRoot, ex, a.DB, ex.FunctionSignature)
				if err != nil {
					return fmt.Errorf("failed clean-room reset: %w", err)
				}
				fmt.Printf("%s Backed up previous attempt and reset starter file: %s\n",
					ui.SuccessStyle.Render("✔"), starterAbs)
			}

			sess, err := session.StartSession(a.ProjectRoot, id, variant)
			if err != nil {
				return fmt.Errorf("failed to start session: %w", err)
			}

			fmt.Println()
			fmt.Println(ui.HeaderStyle.Render(fmt.Sprintf(" PRACTICE STARTED: %s ", ex.Name)))
			fmt.Printf(" Category:       %s\n", ex.Category)
			fmt.Printf(" Difficulty:     %s\n", ex.Difficulty)
			fmt.Printf(" Target Time:    %s | Target Space: %s\n", ex.TargetComplexity.Time, ex.TargetComplexity.Space)
			fmt.Printf(" Recommended:    %d minutes\n", ex.RecommendedMinutes)
			fmt.Printf(" Starter File:   %s\n", ex.StarterPath)
			fmt.Printf(" Timer started:  %s\n\n", sess.StartTime.Format("15:04:05 UTC"))
			fmt.Println("Next steps:")
			fmt.Printf(" 1. Open and implement algorithm:   $EDITOR %s\n", ex.StarterPath)
			fmt.Printf(" 2. Run automated tests:            drills test %s\n", ex.ID)
			fmt.Printf(" 3. Record completed session:       drills finish %s\n\n", ex.ID)
			return nil
		},
	}
	cmd.Flags().BoolVar(&fresh, "fresh", false, "Reset starter file cleanly before starting (previous code is safely archived)")
	cmd.Flags().StringVar(&variant, "variant", "default", "Implementation variant (e.g. recursive, iterative)")
	return cmd
}

func (a *App) newTestCmd() *cobra.Command {
	var level string
	var category string
	var all bool
	var target string

	cmd := &cobra.Command{
		Use:   "test [exercise-id]",
		Short: "Execute automated tests against student or reference implementation",
		Args:  cobra.MaximumNArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			ctx := context.Background()
			pyRunner, err := runner.NewPythonRunner(a.ProjectRoot, a.Config)
			if err != nil {
				return err
			}

			if target == "" {
				target = "student"
			}
			if level == "" {
				level = "all"
			}

			var exercisesToTest []*exercise.Exercise
			if all {
				exercisesToTest = a.Registry.All()
			} else if category != "" {
				exercisesToTest = a.Registry.FilterByCategory(category)
			} else if len(args) > 0 {
				id := args[0]
				ex, ok := a.Registry.Get(id)
				if !ok {
					return fmt.Errorf("exercise '%s' not found", id)
				}
				exercisesToTest = []*exercise.Exercise{ex}
			} else {
				// Check if there is an active session
				activeSess, _ := session.LoadActiveSession(a.ProjectRoot)
				if activeSess != nil {
					ex, ok := a.Registry.Get(activeSess.ExerciseID)
					if ok {
						exercisesToTest = []*exercise.Exercise{ex}
					}
				}
				if len(exercisesToTest) == 0 {
					return fmt.Errorf("please specify an exercise ID, or run 'drills test --category <cat>' or 'drills test --all'")
				}
			}

			totalPassed := 0
			totalFailed := 0
			totalUnimplemented := 0

			fmt.Println()
			fmt.Println(ui.TitleStyle.Render(fmt.Sprintf("ALGORITHM DRILLS — TEST RUNNER (%s)", strings.ToUpper(target))))
			fmt.Println(ui.Divider(70))

			for _, ex := range exercisesToTest {
				fmt.Printf(" Testing [%s] %s ... ", ex.ID, ex.Name)
				report, err := pyRunner.RunTests(
					ctx,
					ex.ID,
					ex.TestPath,
					target,
					level,
					"",
					a.Config.Testing.TimeoutSeconds,
				)

				if err != nil {
					fmt.Println(ui.DangerStyle.Render("ERROR"))
					fmt.Printf("   %v\n", err)
					totalFailed++
					continue
				}

				if report.IsUnimplemented {
					fmt.Println(ui.WarningStyle.Render("UNIMPLEMENTED"))
					fmt.Println("   Exercise contains 'raise NotImplementedError'. Implement the starter file.")
					totalUnimplemented++
					continue
				}

				if report.Failed > 0 || report.Errors > 0 {
					fmt.Println(ui.DangerStyle.Render(fmt.Sprintf("FAILED (%d passed, %d failed)", report.Passed, report.Failed+report.Errors)))
					for _, tc := range report.Tests {
						if tc.Status == "failed" || tc.Status == "error" {
							fmt.Printf("   ✖ [%s] %s (%0.1fms): %s\n", tc.Level, tc.Name, tc.DurationMs, tc.Message)
						}
					}
					totalFailed++
				} else {
					fmt.Println(ui.SuccessStyle.Render(fmt.Sprintf("PASSED (%d tests in %0.1fms)", report.Passed, report.DurationMs)))
					totalPassed++
				}

				// If this matches active session, update session checkpoints
				activeSess, _ := session.LoadActiveSession(a.ProjectRoot)
				if activeSess != nil && activeSess.ExerciseID == ex.ID {
					basicPassed, edgePassed, stressPassed := 0, 0, 0
					for _, tc := range report.Tests {
						if tc.Status == "passed" {
							switch tc.Level {
							case "basic":
								basicPassed++
							case "edge":
								edgePassed++
							case "stress":
								stressPassed++
							}
						}
					}
					_, _ = session.RecordTestRun(a.ProjectRoot, basicPassed, edgePassed, stressPassed)
				}
			}

			fmt.Println(ui.Divider(70))
			fmt.Printf(" Summary: %d passed, %d failed, %d unimplemented (Total: %d)\n\n",
				totalPassed, totalFailed, totalUnimplemented, len(exercisesToTest))

			if totalFailed > 0 {
				return fmt.Errorf("tests failed")
			}
			return nil
		},
	}
	cmd.Flags().StringVarP(&level, "level", "l", "all", "Test level: basic, edge, stress, or all")
	cmd.Flags().StringVarP(&category, "category", "c", "", "Test all exercises in category")
	cmd.Flags().BoolVarP(&all, "all", "a", false, "Test all exercises in library")
	cmd.Flags().StringVar(&target, "target", "student", "Target implementation: student or reference")
	return cmd
}

func (a *App) newFinishCmd() *cobra.Command {
	var confidence int
	var mistakesInput string

	cmd := &cobra.Command{
		Use:   "finish [exercise-id]",
		Short: "Record the completed practice session, verify tests, and update spaced repetition schedule",
		Args:  cobra.MaximumNArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			activeSess, err := session.LoadActiveSession(a.ProjectRoot)
			if err != nil {
				return err
			}

			var exID string
			if len(args) > 0 {
				exID = args[0]
			} else if activeSess != nil {
				exID = activeSess.ExerciseID
			} else {
				return fmt.Errorf("no exercise ID provided and no active session found")
			}

			ex, ok := a.Registry.Get(exID)
			if !ok {
				return fmt.Errorf("exercise '%s' not found", exID)
			}

			// Verify test suite passes before recording completion
			pyRunner, err := runner.NewPythonRunner(a.ProjectRoot, a.Config)
			if err != nil {
				return err
			}

			report, err := pyRunner.RunTests(
				context.Background(),
				ex.ID,
				ex.TestPath,
				"student",
				"all",
				"",
				a.Config.Testing.TimeoutSeconds,
			)
			if err != nil {
				return fmt.Errorf("cannot finish: test runner execution error: %w", err)
			}

			if report.IsUnimplemented {
				return fmt.Errorf("cannot finish: exercise is still unimplemented")
			}
			if report.Failed > 0 || report.Errors > 0 {
				return fmt.Errorf("cannot finish: %d tests are failing. Fix all tests before finishing", report.Failed+report.Errors)
			}

			now := time.Now().UTC()
			durationSec := float64(ex.RecommendedMinutes * 60)
			testRuns := 1
			hintsUsed := 0
			variant := "default"
			sessID := ""
			timeToFirstTest := 0.0

			if activeSess != nil && activeSess.ExerciseID == exID {
				durationSec = now.Sub(activeSess.StartTime).Seconds()
				testRuns = activeSess.TestRunsCount
				hintsUsed = activeSess.HintLevelUsed
				variant = activeSess.Variant
				sessID = activeSess.SessionID
				timeToFirstTest = activeSess.TimeToFirstTestSec
			}

			if confidence <= 0 {
				confidence = 4
			}

			// Record attempt
			attempt := &db.Attempt{
				ExerciseID:         exID,
				SessionID:          sessID,
				Variant:            variant,
				StartTime:          now.Add(-time.Duration(durationSec) * time.Second),
				EndTime:            &now,
				DurationSec:        durationSec,
				TimeToFirstTestSec: timeToFirstTest,
				Status:             "passed",
				TestRunsCount:      testRuns,
				BasicPassed:        report.Passed,
				HintLevelUsed:      hintsUsed,
				ConfidenceRating:   confidence,
				Mistakes:           mistakesInput,
			}

			attemptID, err := a.DB.RecordAttempt(attempt)
			if err != nil {
				return fmt.Errorf("failed to record attempt: %w", err)
			}

			// If mistakes were specified, log them
			if mistakesInput != "" {
				mList := strings.Split(mistakesInput, ",")
				for _, m := range mList {
					mClean := strings.TrimSpace(m)
					if mClean != "" {
						_ = a.DB.LogMistake(&db.MistakeLog{
							AttemptID:  attemptID,
							ExerciseID: exID,
							Category:   ex.Category,
							MistakeID:  mClean,
						})
					}
				}
			}

			// Update Progress & Spaced Repetition Schedule
			p, err := a.DB.GetProgress(exID)
			if err != nil {
				return err
			}

			scheduler.UpdateProgressOnAttempt(
				p,
				ex,
				true,
				durationSec,
				hintsUsed,
				a.Config.Reviews.IntervalsDays,
			)

			if err := a.DB.SaveProgress(p); err != nil {
				return fmt.Errorf("failed to save progress: %w", err)
			}

			// Clear active session
			_ = session.ClearActiveSession(a.ProjectRoot)

			fmt.Println()
			fmt.Println(ui.SuccessStyle.Render("✔ DRILL COMPLETED SUCCESSFULLY!"))
			fmt.Println(ui.Divider(60))
			fmt.Printf(" Exercise:        %s\n", ex.Name)
			fmt.Printf(" Elapsed Time:    %0.1f min (recommended: %d min)\n", durationSec/60.0, ex.RecommendedMinutes)
			fmt.Printf(" Test Runs:       %d\n", testRuns)
			fmt.Printf(" Mastery Level:   %s\n", ui.MasteryBadge(p.MasteryLevel))
			fmt.Printf(" Review Streak:   %d\n", p.Streak)
			fmt.Printf(" Next Review:     %s (in %d days)\n", p.NextReviewAt.Format("2006-01-02 15:04 UTC"), p.IntervalDays)
			fmt.Println(ui.Divider(60))
			fmt.Println()
			return nil
		},
	}
	cmd.Flags().IntVar(&confidence, "confidence", 4, "Self-assessed confidence rating (1-5)")
	cmd.Flags().StringVar(&mistakesInput, "mistakes", "", "Comma-separated mistake IDs encountered during drill")
	return cmd
}

func (a *App) newResetCmd() *cobra.Command {
	var variant string
	cmd := &cobra.Command{
		Use:   "reset <exercise-id>",
		Short: "Safely reset exercise starter code (previous attempts are automatically backed up)",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			id := args[0]
			ex, ok := a.Registry.Get(id)
			if !ok {
				return fmt.Errorf("exercise '%s' not found", id)
			}

			starterAbs, err := cleanroom.BackupAndReset(a.ProjectRoot, ex, a.DB, ex.FunctionSignature)
			if err != nil {
				return fmt.Errorf("failed to reset exercise: %w", err)
			}

			fmt.Println()
			fmt.Printf("%s Safely reset starter code for '%s'.\n", ui.SuccessStyle.Render("✔"), ex.Name)
			fmt.Printf(" File: %s\n", starterAbs)
			fmt.Println(" Any previous code has been archived and can be restored with 'drills recover " + id + "'.\n")
			return nil
		},
	}
	cmd.Flags().StringVar(&variant, "variant", "default", "Exercise variant")
	return cmd
}

func (a *App) newRecoverCmd() *cobra.Command {
	var attemptID int64
	cmd := &cobra.Command{
		Use:   "recover <exercise-id>",
		Short: "List or restore previously archived student code attempts",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			id := args[0]
			ex, ok := a.Registry.Get(id)
			if !ok {
				return fmt.Errorf("exercise '%s' not found", id)
			}

			saved, err := a.DB.GetSavedAttempts(id)
			if err != nil {
				return err
			}

			if len(saved) == 0 {
				fmt.Printf("No saved attempts found for exercise '%s'.\n", id)
				return nil
			}

			if attemptID > 0 {
				if err := cleanroom.RecoverAttempt(a.ProjectRoot, ex, a.DB, attemptID); err != nil {
					return fmt.Errorf("failed to recover attempt #%d: %w", attemptID, err)
				}
				fmt.Printf("%s Restored attempt #%d to %s\n", ui.SuccessStyle.Render("✔"), attemptID, ex.StarterPath)
				return nil
			}

			fmt.Println()
			fmt.Println(ui.TitleStyle.Render(fmt.Sprintf("SAVED ATTEMPTS FOR: %s", ex.Name)))
			fmt.Println(ui.Divider(65))
			fmt.Printf(" %-6s %-24s %-20s %-8s\n", "ID", "SAVED AT", "LABEL", "LINES")
			fmt.Println(ui.Divider(65))

			for _, s := range saved {
				lines := len(strings.Split(s.CodeContent, "\n"))
				fmt.Printf(" #%-5d %-24s %-20s %d lines\n",
					s.ID,
					s.SavedAt.Format("2006-01-02 15:04:05 UTC"),
					s.Label,
					lines,
				)
			}
			fmt.Println(ui.Divider(65))
			fmt.Printf("\nTo restore an attempt, run: drills recover %s --id <ID>\n\n", id)
			return nil
		},
	}
	cmd.Flags().Int64Var(&attemptID, "id", 0, "Saved attempt ID to recover")
	return cmd
}

func (a *App) newProgressCmd() *cobra.Command {
	return &cobra.Command{
		Use:   "progress",
		Short: "Display overall learning progress and category breakdown",
		RunE: func(cmd *cobra.Command, args []string) error {
			allProgress, err := a.DB.GetAllProgress()
			if err != nil {
				return err
			}

			totalExercises := a.Registry.Count()
			mastered := 0
			proficient := 0
			improving := 0
			learning := 0
			notStarted := 0

			categoryCounts := make(map[string]int)
			categoryCompleted := make(map[string]int)

			for _, ex := range a.Registry.All() {
				categoryCounts[ex.Category]++
				p := allProgress[ex.ID]
				if p == nil || p.MasteryLevel <= 1 {
					notStarted++
				} else {
					switch p.MasteryLevel {
					case 2:
						learning++
					case 3:
						improving++
					case 4:
						proficient++
					case 5:
						mastered++
					}
					if p.SuccessfulAttempts > 0 {
						categoryCompleted[ex.Category]++
					}
				}
			}

			fmt.Println()
			fmt.Println(ui.TitleStyle.Render("ALGORITHM DRILLS — OVERALL PROGRESS"))
			fmt.Println(ui.Divider(70))
			totalStarted := totalExercises - notStarted
			fmt.Printf(" Total Library:   %d exercises across %d categories\n", totalExercises, len(a.Registry.Categories()))
			fmt.Printf(" Total Progress:  %s\n\n", ui.ProgressBar(totalStarted, totalExercises, 30))

			fmt.Println(" Mastery Breakdown:")
			fmt.Printf("   ⭐ Mastered:    %3d exercises\n", mastered)
			fmt.Printf("   🟢 Proficient:  %3d exercises\n", proficient)
			fmt.Printf("   🟡 Improving:   %3d exercises\n", improving)
			fmt.Printf("   🔵 Learning:    %3d exercises\n", learning)
			fmt.Printf("   ⚪ Not Started: %3d exercises\n\n", notStarted)

			fmt.Println(ui.Divider(70))
			fmt.Println(" Category Breakdown:")
			for _, cat := range a.Registry.Categories() {
				tot := categoryCounts[cat]
				done := categoryCompleted[cat]
				fmt.Printf("   %-22s : %s\n", cat, ui.ProgressBar(done, tot, 20))
			}
			fmt.Println(ui.Divider(70))
			fmt.Println()
			return nil
		},
	}
}

func (a *App) newStatsCmd() *cobra.Command {
	var category string
	var lastStr string

	cmd := &cobra.Command{
		Use:   "stats",
		Short: "Display performance analytics and metrics from attempt history",
		RunE: func(cmd *cobra.Command, args []string) error {
			attempts, err := a.DB.GetRecentAttempts(500)
			if err != nil {
				return err
			}

			totalAttempts := len(attempts)
			passedCount := 0
			var totalDuration float64
			var totalTimeToTest float64
			var totalConfidence float64
			var totalHints int

			for _, at := range attempts {
				if at.Status == "passed" {
					passedCount++
					totalDuration += at.DurationSec
					totalTimeToTest += at.TimeToFirstTestSec
					totalConfidence += float64(at.ConfidenceRating)
					totalHints += at.HintLevelUsed
				}
			}

			avgDurationMin := 0.0
			avgTimeToTestMin := 0.0
			avgConfidence := 0.0
			avgHints := 0.0
			if passedCount > 0 {
				avgDurationMin = (totalDuration / float64(passedCount)) / 60.0
				avgTimeToTestMin = (totalTimeToTest / float64(passedCount)) / 60.0
				avgConfidence = totalConfidence / float64(passedCount)
				avgHints = float64(totalHints) / float64(passedCount)
			}

			fmt.Println()
			fmt.Println(ui.TitleStyle.Render("ALGORITHM DRILLS — PERFORMANCE ANALYTICS"))
			fmt.Println(ui.Divider(65))
			fmt.Printf(" Total Practice Attempts:    %d\n", totalAttempts)
			fmt.Printf(" Successful Implementations: %d\n", passedCount)
			if totalAttempts > 0 {
				passRate := (float64(passedCount) / float64(totalAttempts)) * 100.0
				fmt.Printf(" Overall Success Rate:       %0.1f%%\n", passRate)
			}
			fmt.Printf(" Avg Implementation Time:    %0.1f minutes\n", avgDurationMin)
			fmt.Printf(" Avg Time to First Test:     %0.1f minutes\n", avgTimeToTestMin)
			fmt.Printf(" Avg Confidence (1-5):       %0.1f\n", avgConfidence)
			fmt.Printf(" Avg Hints per Drill:        %0.2f\n", avgHints)
			fmt.Println(ui.Divider(65))
			fmt.Println()
			return nil
		},
	}
	cmd.Flags().StringVarP(&category, "category", "c", "", "Filter stats by category")
	cmd.Flags().StringVar(&lastStr, "last", "", "Time window filter (e.g. 7d, 30d)")
	return cmd
}

func (a *App) newTodayCmd() *cobra.Command {
	var minutes int
	var focus string

	cmd := &cobra.Command{
		Use:   "today",
		Short: "Generate an automated personalized daily practice plan",
		RunE: func(cmd *cobra.Command, args []string) error {
			if minutes <= 0 {
				minutes = a.Config.Practice.DefaultSessionMinutes
				if minutes <= 0 {
					minutes = 60
				}
			}

			allProgress, err := a.DB.GetAllProgress()
			if err != nil {
				return err
			}

			mistakesFreq, _ := a.DB.GetMistakeFrequency("")

			plan := scheduler.GenerateDailyTraining(a.Registry, allProgress, mistakesFreq, minutes, focus)

			fmt.Println()
			header := fmt.Sprintf(" TODAY'S TRAINING — %d MINUTES ", minutes)
			if focus != "" {
				header = fmt.Sprintf(" TODAY'S TRAINING — %d MINUTES (FOCUS: %s) ", minutes, strings.ToUpper(focus))
			}
			fmt.Println(ui.HeaderStyle.Render(header))
			fmt.Println()

			if len(plan.Items) == 0 {
				fmt.Println("No exercises scheduled. You are caught up with all current reviews!")
				return nil
			}

			fmt.Println(ui.Divider(75))
			fmt.Printf(" #  %-22s %-16s %-8s %-16s\n", "EXERCISE", "CATEGORY", "TIME", "SELECTION REASON")
			fmt.Println(ui.Divider(75))

			for i, item := range plan.Items {
				fmt.Printf(" %2d. %-22s %-16s %2d min   %-16s\n",
					i+1,
					item.Exercise.Name,
					item.Exercise.Category,
					item.EstimatedMinutes,
					item.Reason,
				)
			}
			fmt.Println(ui.Divider(75))
			fmt.Printf(" Planned Duration: %d minutes (Target: %d min)\n\n", plan.TotalMinutes, minutes)
			fmt.Printf("To start the first drill, run: drills start %s\n\n", plan.Items[0].Exercise.ID)
			return nil
		},
	}
	cmd.Flags().IntVarP(&minutes, "minutes", "m", 60, "Practice session budget in minutes (30, 60, 90)")
	cmd.Flags().StringVarP(&focus, "focus", "f", "", "Focus on specific category (e.g. graphs, heaps)")
	return cmd
}

func (a *App) newReviewCmd() *cobra.Command {
	var dueOnly bool
	var category string

	cmd := &cobra.Command{
		Use:   "review",
		Short: "View spaced repetition schedule and pending reviews",
		RunE: func(cmd *cobra.Command, args []string) error {
			allProgress, err := a.DB.GetAllProgress()
			if err != nil {
				return err
			}

			now := time.Now().UTC()
			var dueItems []*exercise.Exercise

			for _, ex := range a.Registry.All() {
				if category != "" && !strings.EqualFold(ex.Category, category) {
					continue
				}
				p := allProgress[ex.ID]
				if p != nil && p.NextReviewAt != nil {
					if dueOnly {
						if now.After(*p.NextReviewAt) {
							dueItems = append(dueItems, ex)
						}
					} else {
						dueItems = append(dueItems, ex)
					}
				}
			}

			fmt.Println()
			fmt.Println(ui.TitleStyle.Render("ALGORITHM DRILLS — SPACED REPETITION REVIEW QUEUE"))
			fmt.Println(ui.Divider(80))
			fmt.Printf(" %-22s %-14s %-16s %-18s %-8s\n", "EXERCISE", "CATEGORY", "MASTERY", "NEXT REVIEW", "STATUS")
			fmt.Println(ui.Divider(80))

			if len(dueItems) == 0 {
				if dueOnly {
					fmt.Println(" No overdue reviews found. You are completely caught up!")
				} else {
					fmt.Println(" No exercises have been scheduled for review yet. Run drills start to begin practicing.")
				}
			}

			for _, ex := range dueItems {
				p := allProgress[ex.ID]
				status := "Pending"
				if now.After(*p.NextReviewAt) {
					status = ui.DangerStyle.Render("OVERDUE")
				} else {
					status = ui.SuccessStyle.Render("Scheduled")
				}
				fmt.Printf(" %-22s %-14s %-16s %-18s %s\n",
					ex.Name,
					ex.Category,
					ui.MasteryBadge(p.MasteryLevel),
					p.NextReviewAt.Format("2006-01-02 15:04"),
					status,
				)
			}
			fmt.Println(ui.Divider(80))
			fmt.Println()
			return nil
		},
	}
	cmd.Flags().BoolVarP(&dueOnly, "due", "d", false, "Show only overdue reviews")
	cmd.Flags().StringVarP(&category, "category", "c", "", "Filter reviews by category")
	return cmd
}

func (a *App) newSessionCmd() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "session",
		Short: "Manage multi-exercise practice sessions",
	}

	startCmd := &cobra.Command{
		Use:   "start",
		Short: "Start an interactive timed practice session",
		RunE: func(cmd *cobra.Command, args []string) error {
			fmt.Println()
			fmt.Println(ui.HeaderStyle.Render(" TIMED WORKOUT SESSION "))
			fmt.Println("Interactive practice session initialized.")
			fmt.Println("Run 'drills today' to view your daily schedule, then 'drills start <id>' to begin each drill.")
			fmt.Println()
			return nil
		},
	}

	summaryCmd := &cobra.Command{
		Use:   "summary",
		Short: "Display active session status and elapsed timers",
		RunE: func(cmd *cobra.Command, args []string) error {
			sess, err := session.LoadActiveSession(a.ProjectRoot)
			if err != nil {
				return err
			}
			if sess == nil {
				fmt.Println("No active drill session in progress. Start one with 'drills start <exercise-id>'.")
				return nil
			}

			ex, _ := a.Registry.Get(sess.ExerciseID)
			elapsed := time.Since(sess.StartTime).Round(time.Second)

			fmt.Println()
			fmt.Println(ui.TitleStyle.Render("ACTIVE DRILL SESSION"))
			fmt.Println(ui.Divider(60))
			if ex != nil {
				fmt.Printf(" Exercise:      %s (%s)\n", ex.Name, ex.Category)
				fmt.Printf(" Recommended:   %d minutes\n", ex.RecommendedMinutes)
			} else {
				fmt.Printf(" Exercise:      %s\n", sess.ExerciseID)
			}
			fmt.Printf(" Variant:       %s\n", sess.Variant)
			fmt.Printf(" Elapsed Time:  %s\n", elapsed)
			fmt.Printf(" Test Runs:     %d\n", sess.TestRunsCount)
			fmt.Printf(" Hints Used:    Level %d\n", sess.HintLevelUsed)
			fmt.Println(ui.Divider(60))
			fmt.Printf("\nTo test your code:   drills test %s\n", sess.ExerciseID)
			fmt.Printf("To finish drill:     drills finish %s\n\n", sess.ExerciseID)
			return nil
		},
	}

	cmd.AddCommand(startCmd, summaryCmd)
	return cmd
}

func (a *App) newFollowupCmd() *cobra.Command {
	return &cobra.Command{
		Use:   "followup <exercise-id>",
		Short: "Unlock and display follow-up challenge for completed exercise",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			id := args[0]
			ex, ok := a.Registry.Get(id)
			if !ok {
				return fmt.Errorf("exercise '%s' not found", id)
			}

			p, err := a.DB.GetProgress(id)
			if err != nil {
				return err
			}

			if p.SuccessfulAttempts == 0 {
				fmt.Println(ui.WarningStyle.Render("Follow-up challenge is locked! Complete the base exercise successfully first."))
				return nil
			}

			if ex.Followup == nil {
				fmt.Printf("No specific follow-up challenge configured for '%s'.\n", ex.Name)
				return nil
			}

			fmt.Println()
			fmt.Println(ui.HeaderStyle.Render(fmt.Sprintf(" FOLLOW-UP CHALLENGE: %s ", ex.Followup.Title)))
			fmt.Println(ui.Divider(65))
			fmt.Printf(" Base Exercise: %s\n", ex.Name)
			fmt.Printf(" Challenge:     %s\n\n", ex.Followup.Title)
			fmt.Println(" Description:")
			fmt.Println(strings.TrimSpace(ex.Followup.Description))
			fmt.Println(ui.Divider(65))
			fmt.Println()
			return nil
		},
	}
}

func (a *App) newMistakesCmd() *cobra.Command {
	var category string
	cmd := &cobra.Command{
		Use:   "mistakes",
		Short: "Display mistake frequency analysis and recurring problem patterns",
		RunE: func(cmd *cobra.Command, args []string) error {
			freq, err := a.DB.GetMistakeFrequency(category)
			if err != nil {
				return err
			}

			fmt.Println()
			header := "MISTAKE TRACKING & ERROR FREQUENCY ANALYSIS"
			if category != "" {
				header = fmt.Sprintf("MISTAKE TRACKING — CATEGORY: %s", strings.ToUpper(category))
			}
			fmt.Println(ui.TitleStyle.Render(header))
			fmt.Println(ui.Divider(70))
			fmt.Printf(" %-26s %-32s %-6s\n", "MISTAKE ID", "DESCRIPTION", "COUNT")
			fmt.Println(ui.Divider(70))

			if len(freq) == 0 {
				fmt.Println(" No mistakes logged yet. As you drill, log any hurdles with 'drills finish --mistakes <id>'.")
			}

			for _, m := range mistakes.AllMistakes {
				count := freq[m.ID]
				if count > 0 {
					fmt.Printf(" %-26s %-32s %4d\n", m.ID, m.Name, count)
				}
			}
			fmt.Println(ui.Divider(70))
			fmt.Println("\nTo view full mistake category definitions, run: drills mistakes --help")
			fmt.Println()
			return nil
		},
	}
	cmd.Flags().StringVarP(&category, "category", "c", "", "Filter mistakes by exercise category")
	return cmd
}

func (a *App) newHintCmd() *cobra.Command {
	var level int
	cmd := &cobra.Command{
		Use:   "hint <exercise-id>",
		Short: "Request an incremental hint (Level 1: Failing example, Level 2: Area, Level 3: Invariant, Level 4: Concept, Level 5: Reference Solution)",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			id := args[0]
			ex, ok := a.Registry.Get(id)
			if !ok {
				return fmt.Errorf("exercise '%s' not found", id)
			}

			if level <= 0 {
				level = 1
			}
			if level > 5 {
				level = 5
			}

			if level == 5 {
				// Explicit confirmation needed for level 5 (reference solution)
				fmt.Print("Level 5 reveals the full reference solution. Are you sure? [y/N]: ")
				reader := bufio.NewReader(os.Stdin)
				input, _ := reader.ReadString('\n')
				input = strings.TrimSpace(strings.ToLower(input))
				if input != "y" && input != "yes" {
					fmt.Println("Hint request cancelled.")
					return nil
				}
			}

			hintText, exists := ex.Hints[level]
			if !exists || hintText == "" {
				hintText = fmt.Sprintf("No prewritten hint available for Level %d. Think carefully about edge cases and invariants.", level)
			}

			// If level 5 and hint says to check reference path, show reference file content
			if level == 5 && strings.Contains(hintText, "reference file") {
				refAbs := filepath.Join(a.ProjectRoot, ex.ReferencePath)
				content, err := os.ReadFile(refAbs)
				if err == nil {
					hintText = fmt.Sprintf("Reference Implementation (%s):\n\n%s", ex.ReferencePath, string(content))
				}
			}

			// Update active session hint level
			activeSess, _ := session.LoadActiveSession(a.ProjectRoot)
			if activeSess != nil && activeSess.ExerciseID == id {
				if level > activeSess.HintLevelUsed {
					activeSess.HintLevelUsed = level
					_ = session.SaveActiveSession(a.ProjectRoot, activeSess)
				}
			}

			fmt.Println()
			fmt.Println(ui.HeaderStyle.Render(fmt.Sprintf(" HINT LEVEL %d: %s ", level, ex.Name)))
			fmt.Println(ui.Divider(65))
			fmt.Println(strings.TrimSpace(hintText))
			fmt.Println(ui.Divider(65))
			fmt.Printf("Note: Using Level %d hint has been logged to your practice attempt record.\n\n", level)
			return nil
		},
	}
	cmd.Flags().IntVarP(&level, "level", "l", 1, "Hint level (1-5)")
	return cmd
}

func (a *App) newDoctorCmd() *cobra.Command {
	return &cobra.Command{
		Use:   "doctor",
		Short: "Verify Python compatibility, max-heap APIs, dependencies, exercise metadata, and database health",
		RunE: func(cmd *cobra.Command, args []string) error {
			results := doctor.RunDoctor(a.ProjectRoot, a.Config)
			ok := doctor.PrintDoctorReport(results)
			if !ok {
				return fmt.Errorf("doctor check found configuration issues")
			}
			return nil
		},
	}
}

func ParseInt(s string, def int) int {
	v, err := strconv.Atoi(s)
	if err != nil {
		return def
	}
	return v
}
