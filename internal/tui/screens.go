package tui

import (
	"fmt"
	"strings"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
	"github.com/user/algorithm-drills/internal/config"
	"github.com/user/algorithm-drills/internal/exercise"
	"github.com/user/algorithm-drills/internal/mistakes"
	"github.com/user/algorithm-drills/internal/ui"
)

// ----------------------------------------------------
// 1. DASHBOARD
// ----------------------------------------------------

func (m *Model) renderDashboard() string {
	var sections []string

	// Welcome & Overview
	totalEx := m.Registry.Count()
	started := 0
	mastered := 0
	for _, p := range m.ProgressMap {
		if p.TotalAttempts > 0 {
			started++
		}
		if p.MasteryLevel == 5 {
			mastered++
		}
	}

	overviewBox := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(ui.ColorPrimary).
		Padding(0, 1).
		Width(m.Width - 4).
		Render(fmt.Sprintf(
			"OVERALL MASTERY: %s   |   MASTERED: %d / %d   |   IN-PROGRESS: %d",
			ui.ProgressBar(started, totalEx, 25),
			mastered, totalEx, started-mastered,
		))
	sections = append(sections, overviewBox)

	// Today's Planned Drills
	var todayLines []string
	todayLines = append(todayLines, ui.TitleStyle.Render(fmt.Sprintf("TODAY'S TRAINING PLAN (%d MIN)", m.DailyMinutes)))
	todayLines = append(todayLines, ui.Divider(m.Width-8))
	if m.DailyPlan != nil && len(m.DailyPlan.Items) > 0 {
		for i, item := range m.DailyPlan.Items {
			p := m.ProgressMap[item.Exercise.ID]
			mastery := 1
			if p != nil {
				mastery = p.MasteryLevel
			}
			line := fmt.Sprintf(" %2d. %-24s %-14s %2d min   %-16s %s",
				i+1,
				item.Exercise.Name,
				item.Exercise.Category,
				item.EstimatedMinutes,
				lipgloss.NewStyle().Foreground(ui.ColorWarning).Render(item.Reason),
				ui.MasteryBadge(mastery),
			)
			todayLines = append(todayLines, line)
		}
		todayLines = append(todayLines, "")
		todayLines = append(todayLines, lipgloss.NewStyle().Foreground(ui.ColorSuccess).Render("Press [Enter] on Daily Plan tab (5) to start any exercise directly."))
	} else {
		todayLines = append(todayLines, "No scheduled reviews due today! You are all caught up.")
	}

	planBox := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(ui.ColorSecondary).
		Padding(0, 1).
		Width(m.Width - 4).
		Render(lipgloss.JoinVertical(lipgloss.Left, todayLines...))
	sections = append(sections, planBox)

	// Quick Actions Card
	quickContent := fmt.Sprintf(
		"%s\n%s\n"+
			" [2] Browse 88 Algorithm Drills      [4] Open Active Practice Session\n"+
			" [5] Customize Today's Workout       [6] Spaced Repetition Review Queue\n"+
			" [7] Mistakes & Analytics Dash       [?] Keyboard Shortcuts Guide",
		ui.TitleStyle.Render("QUICK NAVIGATION"),
		ui.Divider(m.Width-8),
	)
	quickBox := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(ui.ColorSubtle).
		Padding(0, 1).
		Width(m.Width - 4).
		Render(quickContent)
	sections = append(sections, quickBox)

	return lipgloss.JoinVertical(lipgloss.Left, sections...)
}

func (m *Model) updateDashboard(msg tea.KeyMsg) {
	switch msg.String() {
	case "enter":
		// Quick start first today item
		if m.DailyPlan != nil && len(m.DailyPlan.Items) > 0 {
			m.SelectedExercise = m.DailyPlan.Items[0].Exercise
			m.startDrill(m.SelectedExercise, false)
		}
	}
}

// ----------------------------------------------------
// 2. EXERCISE BROWSER
// ----------------------------------------------------

func (m *Model) renderBrowser() string {
	cats := m.Registry.Categories()
	leftWidth := 24
	rightWidth := m.Width - leftWidth - 6

	// Left: Category list
	var catLines []string
	catLines = append(catLines, ui.TitleStyle.Render("CATEGORIES"))
	catLines = append(catLines, ui.Divider(leftWidth-4))

	for i, cat := range cats {
		cursor := "  "
		style := lipgloss.NewStyle().Foreground(ui.ColorMuted)
		if i == m.SelectedCategoryIdx {
			cursor = "▶ "
			style = lipgloss.NewStyle().Bold(true).Foreground(ui.ColorPrimary)
		}
		count := len(m.Registry.FilterByCategory(cat))
		catLines = append(catLines, fmt.Sprintf("%s%s (%d)", cursor, style.Render(cat), count))
	}

	leftPane := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(ui.ColorPrimary).
		Width(leftWidth).
		Height(m.Height - 6).
		Padding(0, 1).
		Render(lipgloss.JoinVertical(lipgloss.Left, catLines...))

	// Right: Exercise list + Search
	var rightLines []string
	searchHeader := "EXERCISES (Press '/' to search)"
	if m.SearchActive {
		searchHeader = fmt.Sprintf("SEARCHING: %s █", m.SearchQuery)
	} else if m.SearchQuery != "" {
		searchHeader = fmt.Sprintf("FILTER: '%s' (Esc to clear)", m.SearchQuery)
	}
	rightLines = append(rightLines, ui.TitleStyle.Render(searchHeader))
	rightLines = append(rightLines, ui.Divider(rightWidth-4))
	rightLines = append(rightLines, fmt.Sprintf(" %-24s %-8s %-6s %-16s", "EXERCISE", "DIFF", "TIME", "MASTERY"))
	rightLines = append(rightLines, ui.Divider(rightWidth-4))

	if len(m.FilteredExList) == 0 {
		rightLines = append(rightLines, " No exercises match current filter.")
	} else {
		for i, ex := range m.FilteredExList {
			cursor := "  "
			style := lipgloss.NewStyle()
			if i == m.SelectedExerciseIdx {
				cursor = "▶ "
				style = lipgloss.NewStyle().Bold(true).Foreground(ui.ColorPrimary)
			}
			p := m.ProgressMap[ex.ID]
			mastery := 1
			if p != nil {
				mastery = p.MasteryLevel
			}

			line := fmt.Sprintf("%s%-24s %-8s %2d min %-16s",
				cursor,
				style.Render(ex.ID),
				ui.DifficultyBadge(ex.Difficulty),
				ex.RecommendedMinutes,
				ui.MasteryBadge(mastery),
			)
			rightLines = append(rightLines, line)
			if len(rightLines) >= m.Height-10 {
				break
			}
		}
	}

	rightPane := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(ui.ColorSecondary).
		Width(rightWidth).
		Height(m.Height - 6).
		Padding(0, 1).
		Render(lipgloss.JoinVertical(lipgloss.Left, rightLines...))

	return lipgloss.JoinHorizontal(lipgloss.Top, leftPane, rightPane)
}

func (m *Model) updateBrowser(msg tea.KeyMsg) {
	cats := m.Registry.Categories()
	switch msg.String() {
	case "up", "k":
		if m.SelectedExerciseIdx > 0 {
			m.SelectedExerciseIdx--
			m.updateFilteredExercises()
		}
	case "down", "j":
		if m.SelectedExerciseIdx < len(m.FilteredExList)-1 {
			m.SelectedExerciseIdx++
			m.updateFilteredExercises()
		}
	case "tab":
		m.SelectedCategoryIdx = (m.SelectedCategoryIdx + 1) % len(cats)
		m.SelectedExerciseIdx = 0
		m.updateFilteredExercises()
	case "enter":
		if len(m.FilteredExList) > 0 {
			m.SelectedExercise = m.FilteredExList[m.SelectedExerciseIdx]
			m.SwitchScreen(ScreenDetails)
		}
	}
}

// ----------------------------------------------------
// 3. EXERCISE DETAILS
// ----------------------------------------------------

func (m *Model) renderDetails() string {
	ex := m.SelectedExercise
	if ex == nil {
		if m.ActiveExercise != nil {
			ex = m.ActiveExercise
		} else {
			return "No exercise selected. Go to [2] Exercises to select an exercise."
		}
	}

	p := m.ProgressMap[ex.ID]
	mastery := 1
	attempts := 0
	successes := 0
	bestTime := 0.0
	streak := 0
	if p != nil {
		mastery = p.MasteryLevel
		attempts = p.TotalAttempts
		successes = p.SuccessfulAttempts
		bestTime = p.BestCompletionTimeSec
		streak = p.Streak
	}

	details := fmt.Sprintf(
		"%s\n%s\n"+
			"Category:        %s\n"+
			"Difficulty:      %s   (Level %d)\n"+
			"Target Time:     %s\n"+
			"Target Space:    %s\n"+
			"Recommended:     %d minutes\n\n"+
			"Progress:\n"+
			"  Mastery Level: %s\n"+
			"  Attempts:      %d (%d successful, streak: %d)\n"+
			"  Best Time:     %0.1f sec\n\n"+
			"Files:\n"+
			"  Starter File:  %s\n"+
			"  Test Suite:    %s\n\n"+
			"Specification:\n%s\n\n"+
			"%s\n"+
			"[Enter] Start Practice Session   [e] Open Editor   [r] Reset Starter Code   [Esc] Back",
		ui.TitleStyle.Render(fmt.Sprintf("%s (%s)", ex.Name, ex.ID)),
		ui.Divider(m.Width-8),
		ex.Category,
		ui.DifficultyBadge(ex.Difficulty),
		ex.Level,
		ex.TargetComplexity.Time,
		ex.TargetComplexity.Space,
		ex.RecommendedMinutes,
		ui.MasteryBadge(mastery),
		attempts, successes, streak, bestTime,
		ex.StarterPath,
		ex.TestPath,
		strings.TrimSpace(ex.Description),
		ui.Divider(m.Width-8),
	)

	return lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(ui.ColorPrimary).
		Padding(1, 2).
		Width(m.Width - 4).
		Height(m.Height - 6).
		Render(details)
}

func (m *Model) updateDetails(msg tea.KeyMsg) {
	switch msg.String() {
	case "enter":
		if m.SelectedExercise != nil {
			m.startDrill(m.SelectedExercise, false)
		}
	case "esc":
		m.SwitchScreen(ScreenBrowser)
	}
}

// ----------------------------------------------------
// 4. PRACTICE SESSION
// ----------------------------------------------------

func (m *Model) renderPractice() string {
	if m.ActiveExercise == nil {
		return lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			Padding(1, 2).
			Render("No active drill in progress. Select an exercise from [2] Exercises or [5] Daily Plan to start.")
	}

	ex := m.ActiveExercise
	mins := int(m.SessionElapsed.Minutes())
	secs := int(m.SessionElapsed.Seconds()) % 60
	timerStr := fmt.Sprintf("%02d:%02d", mins, secs)

	topBar := fmt.Sprintf(
		"EXERCISE: %s   |   TIMER: %s (Recommended: %d min)   |   STATUS: %s",
		lipgloss.NewStyle().Bold(true).Foreground(ui.ColorPrimary).Render(ex.Name),
		lipgloss.NewStyle().Bold(true).Foreground(ui.ColorWarning).Render(timerStr),
		ex.RecommendedMinutes,
		ui.DifficultyBadge(ex.Difficulty),
	)

	// Action controls bar
	controls := lipgloss.NewStyle().
		Foreground(ui.ColorPrimary).
		Render("[e] Open in Editor   [t] Run All Tests   [b] Basic Tests   [x] Edge Tests   [h] Hint   [f] Finish Drill")

	// Test output panel
	var testLines []string
	testLines = append(testLines, ui.TitleStyle.Render("TEST EXECUTION RESULTS"))
	testLines = append(testLines, ui.Divider(m.Width-8))

	if m.IsTesting {
		testLines = append(testLines, lipgloss.NewStyle().Foreground(ui.ColorWarning).Render("Running automated tests in isolated Python subprocess..."))
	} else if m.LastTestReport == nil {
		testLines = append(testLines, "No tests executed yet. Implement code in your editor, then press 't' to test.")
	} else {
		rep := m.LastTestReport
		if rep.IsUnimplemented {
			testLines = append(testLines, ui.WarningStyle.Render("UNIMPLEMENTED: Starter code raises NotImplementedError."))
		} else if rep.Failed > 0 || rep.Errors > 0 {
			testLines = append(testLines, ui.DangerStyle.Render(fmt.Sprintf("FAILED: %d passed, %d failed (%0.1fms)", rep.Passed, rep.Failed+rep.Errors, rep.DurationMs)))
			for _, tc := range rep.Tests {
				if tc.Status == "failed" || tc.Status == "error" {
					testLines = append(testLines, fmt.Sprintf("  ✖ [%s] %s: %s", tc.Level, tc.Name, tc.Message))
				}
			}
		} else {
			testLines = append(testLines, ui.SuccessStyle.Render(fmt.Sprintf("✔ ALL TESTS PASSED! (%d tests in %0.1fms)", rep.Passed, rep.DurationMs)))
			testLines = append(testLines, "Ready to record completion: Press 'f' to finish and log hurdles.")
		}
	}

	testBox := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(ui.ColorSecondary).
		Padding(0, 1).
		Width(m.Width - 4).
		Height(10).
		Render(lipgloss.JoinVertical(lipgloss.Left, testLines...))

	// Hint panel if revealed
	var hintContent string
	if m.CurrentHint > 0 && m.CurrentHintTxt != "" {
		hintLines := []string{
			ui.TitleStyle.Render(fmt.Sprintf("HINT LEVEL %d OF 5", m.CurrentHint)),
			ui.Divider(m.Width - 8),
			m.CurrentHintTxt,
		}
		hintContent = lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			BorderForeground(ui.ColorWarning).
			Padding(0, 1).
			Width(m.Width - 4).
			Render(lipgloss.JoinVertical(lipgloss.Left, hintLines...))
	}

	return lipgloss.JoinVertical(lipgloss.Left, topBar, controls, testBox, hintContent)
}

func (m *Model) updatePractice(msg tea.KeyMsg) {
	// Handled by global shortcuts in model.go (e, t, b, x, s, h, f)
}

// ----------------------------------------------------
// 5. DAILY TRAINING PLAN
// ----------------------------------------------------

func (m *Model) renderDaily() string {
	var lines []string
	lines = append(lines, ui.TitleStyle.Render(fmt.Sprintf("AUTOMATED DAILY TRAINING GENERATOR — %d MINUTES", m.DailyMinutes)))
	lines = append(lines, "Press '[' / ']' to change duration (30 / 60 / 90 min). Press Enter to start highlighted drill.")
	lines = append(lines, ui.Divider(m.Width-8))
	lines = append(lines, fmt.Sprintf(" #  %-24s %-14s %-8s %-16s %s", "EXERCISE", "CATEGORY", "TIME", "SELECTION REASON", "MASTERY"))
	lines = append(lines, ui.Divider(m.Width-8))

	if m.DailyPlan != nil && len(m.DailyPlan.Items) > 0 {
		for i, item := range m.DailyPlan.Items {
			cursor := "  "
			style := lipgloss.NewStyle()
			if i == m.DailyCursor {
				cursor = "▶ "
				style = lipgloss.NewStyle().Bold(true).Foreground(ui.ColorPrimary)
			}
			p := m.ProgressMap[item.Exercise.ID]
			mastery := 1
			if p != nil {
				mastery = p.MasteryLevel
			}

			lines = append(lines, fmt.Sprintf("%s%2d. %-24s %-14s %2d min   %-16s %s",
				cursor,
				i+1,
				style.Render(item.Exercise.Name),
				item.Exercise.Category,
				item.EstimatedMinutes,
				lipgloss.NewStyle().Foreground(ui.ColorWarning).Render(item.Reason),
				ui.MasteryBadge(mastery),
			))
		}
		lines = append(lines, ui.Divider(m.Width-8))
		lines = append(lines, fmt.Sprintf("Total Estimated Duration: %d minutes", m.DailyPlan.TotalMinutes))
	} else {
		lines = append(lines, "No drills currently due.")
	}

	return lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(ui.ColorPrimary).
		Padding(1, 2).
		Width(m.Width - 4).
		Height(m.Height - 6).
		Render(lipgloss.JoinVertical(lipgloss.Left, lines...))
}

func (m *Model) updateDaily(msg tea.KeyMsg) {
	switch msg.String() {
	case "[":
		if m.DailyMinutes > 30 {
			m.DailyMinutes -= 30
			m.RefreshData()
		}
	case "]":
		if m.DailyMinutes < 120 {
			m.DailyMinutes += 30
			m.RefreshData()
		}
	case "up", "k":
		if m.DailyCursor > 0 {
			m.DailyCursor--
		}
	case "down", "j":
		if m.DailyPlan != nil && m.DailyCursor < len(m.DailyPlan.Items)-1 {
			m.DailyCursor++
		}
	case "enter":
		if m.DailyPlan != nil && len(m.DailyPlan.Items) > 0 {
			m.SelectedExercise = m.DailyPlan.Items[m.DailyCursor].Exercise
			m.startDrill(m.SelectedExercise, false)
		}
	}
}

// ----------------------------------------------------
// 6. SPACED REVIEWS
// ----------------------------------------------------

func (m *Model) renderReviews() string {
	var lines []string
	lines = append(lines, ui.TitleStyle.Render("SPACED REPETITION REVIEW QUEUE"))
	lines = append(lines, ui.Divider(m.Width-8))
	lines = append(lines, fmt.Sprintf(" %-24s %-14s %-16s %-18s %s", "EXERCISE", "CATEGORY", "MASTERY", "NEXT REVIEW", "STATUS"))
	lines = append(lines, ui.Divider(m.Width-8))

	now := time.Now().UTC()
	var reviewItems []*exercise.Exercise
	for _, ex := range m.Registry.All() {
		p := m.ProgressMap[ex.ID]
		if p != nil && p.NextReviewAt != nil {
			reviewItems = append(reviewItems, ex)
		}
	}

	if len(reviewItems) == 0 {
		lines = append(lines, "No scheduled reviews found. Complete exercises to populate spaced repetition schedule.")
	} else {
		for i, ex := range reviewItems {
			cursor := "  "
			if i == m.ReviewsCursor {
				cursor = "▶ "
			}
			p := m.ProgressMap[ex.ID]
			status := ui.SuccessStyle.Render("Scheduled")
			if now.After(*p.NextReviewAt) {
				status = ui.DangerStyle.Render("OVERDUE")
			}
			lines = append(lines, fmt.Sprintf("%s%-24s %-14s %-16s %-18s %s",
				cursor,
				ex.Name,
				ex.Category,
				ui.MasteryBadge(p.MasteryLevel),
				p.NextReviewAt.Format("2006-01-02 15:04"),
				status,
			))
			if len(lines) >= m.Height-10 {
				break
			}
		}
	}

	return lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(ui.ColorPrimary).
		Padding(1, 2).
		Width(m.Width - 4).
		Height(m.Height - 6).
		Render(lipgloss.JoinVertical(lipgloss.Left, lines...))
}

func (m *Model) updateReviews(msg tea.KeyMsg) {
	// Navigation in reviews queue
}

// ----------------------------------------------------
// 7. ANALYTICS & PROGRESS
// ----------------------------------------------------

func (m *Model) renderAnalytics() string {
	var lines []string
	lines = append(lines, ui.TitleStyle.Render("PERFORMANCE ANALYTICS & MISTAKE PATTERNS"))
	lines = append(lines, ui.Divider(m.Width-8))

	// Category mastery breakdown
	lines = append(lines, lipgloss.NewStyle().Bold(true).Render("Category Progress:"))
	for _, cat := range m.Registry.Categories() {
		catExercises := m.Registry.FilterByCategory(cat)
		done := 0
		for _, ex := range catExercises {
			p := m.ProgressMap[ex.ID]
			if p != nil && p.SuccessfulAttempts > 0 {
				done++
			}
		}
		lines = append(lines, fmt.Sprintf("  %-22s : %s", cat, ui.ProgressBar(done, len(catExercises), 20)))
	}

	lines = append(lines, "")
	lines = append(lines, ui.Divider(m.Width-8))
	lines = append(lines, lipgloss.NewStyle().Bold(true).Render("Recurring Mistake Categories:"))
	lines = append(lines, fmt.Sprintf("  %-24s %-30s %s", "MISTAKE ID", "NAME", "OCCURRENCES"))

	hasMistakes := false
	for _, mis := range mistakes.AllMistakes {
		count := m.MistakeFreq[mis.ID]
		if count > 0 {
			hasMistakes = true
			lines = append(lines, fmt.Sprintf("  %-24s %-30s %4d", mis.ID, mis.Name, count))
		}
	}
	if !hasMistakes {
		lines = append(lines, "  No mistakes logged yet. As you practice, log any difficulties with 'f'.")
	}

	return lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(ui.ColorPrimary).
		Padding(1, 2).
		Width(m.Width - 4).
		Height(m.Height - 6).
		Render(lipgloss.JoinVertical(lipgloss.Left, lines...))
}

func (m *Model) updateAnalytics(msg tea.KeyMsg) {
}

// ----------------------------------------------------
// 8. SETTINGS
// ----------------------------------------------------

func (m *Model) renderSettings() string {
	editor := config.ResolveEditor(m.Config.Practice.Editor)

	content := fmt.Sprintf(
		"%s\n%s\n"+
			"Environment & Application Preferences:\n\n"+
			"  Configured Editor:       %s\n"+
			"  Python Virtualenv:       %s\n"+
			"  Testing Timeout:         %d seconds\n"+
			"  Hypothesis Examples:     %d iterations\n"+
			"  Spaced Intervals:        %v days\n"+
			"  Default Session:         %d minutes\n\n"+
			"Database:\n"+
			"  Location:                .drills/progress.db\n"+
			"  Driver:                  modernc.org/sqlite (Pure Go, Zero CGO)\n\n"+
			"Python 3.14+ Engine:\n"+
			"  Native Max-Heaps:        Enabled (heapq.heapify_max, heappush_max, heappop_max)\n"+
			"  Test Isolation:          Subprocess with JSON report streaming\n\n"+
			"To modify settings permanently, edit .drills/config.yaml.",
		ui.TitleStyle.Render("CONFIGURATION & SYSTEM SETTINGS"),
		ui.Divider(m.Width-8),
		editor,
		m.Config.Python.VenvPath,
		m.Config.Testing.TimeoutSeconds,
		m.Config.Testing.HypothesisExamples,
		m.Config.Reviews.IntervalsDays,
		m.Config.Practice.DefaultSessionMinutes,
	)

	return lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(ui.ColorPrimary).
		Padding(1, 2).
		Width(m.Width - 4).
		Height(m.Height - 6).
		Render(content)
}

func (m *Model) updateSettings(msg tea.KeyMsg) {
}
