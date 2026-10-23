package tui

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/user/algorithm-drills/internal/cleanroom"
	"github.com/user/algorithm-drills/internal/config"
	"github.com/user/algorithm-drills/internal/db"
	"github.com/user/algorithm-drills/internal/exercise"
	"github.com/user/algorithm-drills/internal/mistakes"
	"github.com/user/algorithm-drills/internal/runner"
	"github.com/user/algorithm-drills/internal/scheduler"
	"github.com/user/algorithm-drills/internal/session"
)

type Screen int

const (
	ScreenDashboard Screen = iota
	ScreenBrowser
	ScreenDetails
	ScreenPractice
	ScreenDaily
	ScreenReviews
	ScreenAnalytics
	ScreenSettings
)

var screenNames = []string{
	"Dashboard",
	"Exercises",
	"Details",
	"Practice",
	"Daily Plan",
	"Reviews",
	"Analytics",
	"Settings",
}

// Messages
type tickMsg time.Time
type testFinishedMsg struct {
	report *runner.TestReport
	err    error
}
type editorFinishedMsg struct {
	err error
}

type Model struct {
	ProjectRoot string
	Config      *config.Config
	DB          *db.DB
	Registry    *exercise.ExerciseRegistry

	// Screen & Navigation
	CurrentScreen  Screen
	PreviousScreen Screen
	Width          int
	Height         int

	// Search & Filter
	SearchActive bool
	SearchQuery  string

	// Modals & Overlays
	ShowHelpModal     bool
	ShowMistakeModal  bool
	ConfirmResetModal bool
	StatusMessage     string
	StatusIsError     bool

	// Selection state
	SelectedCategoryIdx int
	SelectedExerciseIdx int
	ActiveExercise      *exercise.Exercise
	SelectedExercise    *exercise.Exercise

	// Practice state
	ActiveSession  *session.ActiveSession
	SessionElapsed time.Duration
	IsTesting      bool
	LastTestReport *runner.TestReport
	CurrentHint    int
	CurrentHintTxt string

	// Mistake logging modal selection
	SelectedMistakeIdxs map[int]bool
	MistakeCursorIdx    int
	ConfidenceRating    int

	// Daily training state
	DailyMinutes int
	DailyPlan    *scheduler.DailyPlan
	DailyCursor  int

	// Reviews state
	ReviewsCursor int

	// Cached data
	ProgressMap   map[string]*db.ExerciseProgress
	MistakeFreq   map[string]int
	FilteredExList []*exercise.Exercise
}

func NewModel(projectRoot string, cfg *config.Config, database *db.DB, reg *exercise.ExerciseRegistry) *Model {
	m := &Model{
		ProjectRoot:         projectRoot,
		Config:              cfg,
		DB:                  database,
		Registry:            reg,
		CurrentScreen:       ScreenDashboard,
		PreviousScreen:      ScreenDashboard,
		DailyMinutes:        60,
		ConfidenceRating:    4,
		SelectedMistakeIdxs: make(map[int]bool),
		ProgressMap:         make(map[string]*db.ExerciseProgress),
		MistakeFreq:         make(map[string]int),
	}
	m.RefreshData()
	return m
}

func (m *Model) RefreshData() {
	if m.DB != nil {
		allProg, err := m.DB.GetAllProgress()
		if err == nil {
			m.ProgressMap = allProg
		}
		freq, err := m.DB.GetMistakeFrequency("")
		if err == nil {
			m.MistakeFreq = freq
		}
	}

	// Active session
	sess, _ := session.LoadActiveSession(m.ProjectRoot)
	m.ActiveSession = sess
	if sess != nil {
		m.ActiveExercise, _ = m.Registry.Get(sess.ExerciseID)
		m.SessionElapsed = time.Since(sess.StartTime)
	}

	// Daily plan
	m.DailyPlan = scheduler.GenerateDailyTraining(
		m.Registry,
		m.ProgressMap,
		m.MistakeFreq,
		m.DailyMinutes,
		"",
	)

	m.updateFilteredExercises()
}

func (m *Model) updateFilteredExercises() {
	cats := m.Registry.Categories()
	var baseList []*exercise.Exercise

	if len(cats) > 0 && m.SelectedCategoryIdx < len(cats) {
		cat := cats[m.SelectedCategoryIdx]
		baseList = m.Registry.FilterByCategory(cat)
	} else {
		baseList = m.Registry.All()
	}

	if m.SearchQuery == "" {
		m.FilteredExList = baseList
	} else {
		query := strings.ToLower(m.SearchQuery)
		var filtered []*exercise.Exercise
		for _, ex := range baseList {
			if strings.Contains(strings.ToLower(ex.Name), query) ||
				strings.Contains(strings.ToLower(ex.ID), query) {
				filtered = append(filtered, ex)
			}
		}
		m.FilteredExList = filtered
	}

	if m.SelectedExerciseIdx >= len(m.FilteredExList) {
		m.SelectedExerciseIdx = 0
	}
	if len(m.FilteredExList) > 0 {
		m.SelectedExercise = m.FilteredExList[m.SelectedExerciseIdx]
	} else {
		m.SelectedExercise = nil
	}
}

func (m *Model) Init() tea.Cmd {
	return tea.Batch(
		tea.EnterAltScreen,
		tickerCmd(),
	)
}

func tickerCmd() tea.Cmd {
	return tea.Tick(time.Second, func(t time.Time) tea.Msg {
		return tickMsg(t)
	})
}

func (m *Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmds []tea.Cmd

	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		m.Width = msg.Width
		m.Height = msg.Height

	case tickMsg:
		if m.ActiveSession != nil {
			m.SessionElapsed = time.Since(m.ActiveSession.StartTime)
		}
		cmds = append(cmds, tickerCmd())

	case editorFinishedMsg:
		m.RefreshData()
		m.SetStatus("Returned from editor. Code saved.", false)

	case testFinishedMsg:
		m.IsTesting = false
		if msg.err != nil {
			m.SetStatus(fmt.Sprintf("Test runner error: %v", msg.err), true)
		} else {
			m.LastTestReport = msg.report
			if msg.report.IsUnimplemented {
				m.SetStatus("Implementation contains raise NotImplementedError.", true)
			} else if msg.report.Failed > 0 || msg.report.Errors > 0 {
				m.SetStatus(fmt.Sprintf("%d test(s) failed. Inspect failures below.", msg.report.Failed+msg.report.Errors), true)
			} else {
				m.SetStatus(fmt.Sprintf("All %d test(s) passed successfully! (%0.1fms)", msg.report.Passed, msg.report.DurationMs), false)
			}
		}

	case tea.KeyMsg:
		// Modal handling first
		if m.ShowHelpModal {
			if msg.String() == "?" || msg.String() == "esc" || msg.String() == "q" {
				m.ShowHelpModal = false
			}
			return m, nil
		}

		if m.ConfirmResetModal {
			switch msg.String() {
			case "y", "Y", "enter":
				m.ConfirmResetModal = false
				if m.SelectedExercise != nil {
					_, err := cleanroom.BackupAndReset(m.ProjectRoot, m.SelectedExercise, m.DB, m.SelectedExercise.FunctionSignature)
					if err != nil {
						m.SetStatus(fmt.Sprintf("Reset error: %v", err), true)
					} else {
						m.SetStatus(fmt.Sprintf("Starter code reset for %s (backup archived).", m.SelectedExercise.Name), false)
					}
				}
			case "n", "N", "esc", "q":
				m.ConfirmResetModal = false
			}
			return m, nil
		}

		if m.ShowMistakeModal {
			switch msg.String() {
			case "up", "k":
				if m.MistakeCursorIdx > 0 {
					m.MistakeCursorIdx--
				}
			case "down", "j":
				if m.MistakeCursorIdx < len(mistakes.AllMistakes)-1 {
					m.MistakeCursorIdx++
				}
			case " ":
				m.SelectedMistakeIdxs[m.MistakeCursorIdx] = !m.SelectedMistakeIdxs[m.MistakeCursorIdx]
			case "1", "2", "3", "4", "5":
				m.ConfidenceRating = int(msg.String()[0] - '0')
			case "enter":
				m.ShowMistakeModal = false
				m.finalizeFinishedDrill()
			case "esc":
				m.ShowMistakeModal = false
			}
			return m, nil
		}

		// Search input handling
		if m.SearchActive {
			switch msg.String() {
			case "esc":
				m.SearchActive = false
				m.SearchQuery = ""
				m.updateFilteredExercises()
			case "enter":
				m.SearchActive = false
			case "backspace":
				if len(m.SearchQuery) > 0 {
					m.SearchQuery = m.SearchQuery[:len(m.SearchQuery)-1]
					m.updateFilteredExercises()
				}
			default:
				if len(msg.String()) == 1 {
					m.SearchQuery += msg.String()
					m.updateFilteredExercises()
				}
			}
			return m, nil
		}

		// Global shortcuts
		switch msg.String() {
		case "q", "ctrl+c":
			if m.CurrentScreen != ScreenDashboard {
				m.SwitchScreen(ScreenDashboard)
				return m, nil
			}
			return m, tea.Quit

		case "?":
			m.ShowHelpModal = true
			return m, nil

		case "/":
			if m.CurrentScreen == ScreenBrowser {
				m.SearchActive = true
				return m, nil
			}

		case "1":
			m.SwitchScreen(ScreenDashboard)
		case "2":
			m.SwitchScreen(ScreenBrowser)
		case "3":
			m.SwitchScreen(ScreenDetails)
		case "4":
			m.SwitchScreen(ScreenPractice)
		case "5":
			m.SwitchScreen(ScreenDaily)
		case "6":
			m.SwitchScreen(ScreenReviews)
		case "7":
			m.SwitchScreen(ScreenAnalytics)
		case "8":
			m.SwitchScreen(ScreenSettings)

		case "e":
			// Launch editor
			targetEx := m.ActiveExercise
			if targetEx == nil {
				targetEx = m.SelectedExercise
			}
			if targetEx != nil {
				cmd := m.launchEditor(targetEx)
				if cmd != nil {
					return m, cmd
				}
			}

		case "t":
			// Run tests
			if m.ActiveExercise != nil {
				return m, m.runTestsAsync("all")
			}

		case "b":
			if m.ActiveExercise != nil {
				return m, m.runTestsAsync("basic")
			}

		case "x":
			if m.ActiveExercise != nil {
				return m, m.runTestsAsync("edge")
			}

		case "s":
			if m.ActiveExercise != nil {
				return m, m.runTestsAsync("stress")
			}

		case "h":
			// Request hint
			if m.ActiveExercise != nil {
				m.requestNextHint()
			}

		case "f":
			// Finish drill
			if m.ActiveExercise != nil {
				if m.LastTestReport == nil || m.LastTestReport.Failed > 0 || m.LastTestReport.IsUnimplemented {
					m.SetStatus("Cannot finish: Please run and pass all tests first ('t')", true)
				} else {
					m.ShowMistakeModal = true
				}
			}

		case "r":
			// Reset confirmation
			if m.SelectedExercise != nil || m.ActiveExercise != nil {
				m.ConfirmResetModal = true
			}

		case "esc":
			if m.CurrentScreen != ScreenDashboard {
				m.SwitchScreen(m.PreviousScreen)
			}
		}

		// Screen-specific navigation
		switch m.CurrentScreen {
		case ScreenDashboard:
			m.updateDashboard(msg)
		case ScreenBrowser:
			m.updateBrowser(msg)
		case ScreenDetails:
			m.updateDetails(msg)
		case ScreenPractice:
			m.updatePractice(msg)
		case ScreenDaily:
			m.updateDaily(msg)
		case ScreenReviews:
			m.updateReviews(msg)
		case ScreenAnalytics:
			m.updateAnalytics(msg)
		case ScreenSettings:
			m.updateSettings(msg)
		}
	}

	return m, tea.Batch(cmds...)
}

func (m *Model) SwitchScreen(s Screen) {
	m.PreviousScreen = m.CurrentScreen
	m.CurrentScreen = s
	m.StatusMessage = ""
}

func (m *Model) SetStatus(msg string, isError bool) {
	m.StatusMessage = msg
	m.StatusIsError = isError
}

func (m *Model) launchEditor(ex *exercise.Exercise) tea.Cmd {
	editor := m.Config.Practice.Editor
	if editor == "" {
		editor = os.Getenv("EDITOR")
	}
	if editor == "" {
		if path, err := exec.LookPath("nvim"); err == nil {
			editor = path
		} else if path, err := exec.LookPath("vim"); err == nil {
			editor = path
		} else {
			editor = "nano"
		}
	}

	filePath := filepath.Join(m.ProjectRoot, ex.StarterPath)

	// Ensure starter file exists
	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		_ = os.MkdirAll(filepath.Dir(filePath), 0755)
		_ = os.WriteFile(filePath, []byte(ex.FunctionSignature), 0644)
	}

	c := exec.Command(editor, filePath)
	return tea.ExecProcess(c, func(err error) tea.Msg {
		return editorFinishedMsg{err}
	})
}

func (m *Model) runTestsAsync(level string) tea.Cmd {
	if m.ActiveExercise == nil {
		return nil
	}
	m.IsTesting = true
	m.SetStatus(fmt.Sprintf("Running %s tests...", level), false)

	exID := m.ActiveExercise.ID
	testPath := m.ActiveExercise.TestPath
	root := m.ProjectRoot
	cfg := m.Config

	return func() tea.Msg {
		pyRunner, err := runner.NewPythonRunner(root, cfg)
		if err != nil {
			return testFinishedMsg{err: err}
		}

		rep, err := pyRunner.RunTests(
			context.Background(),
			exID,
			testPath,
			"student",
			level,
			"",
			cfg.Testing.TimeoutSeconds,
		)
		return testFinishedMsg{report: rep, err: err}
	}
}

func (m *Model) requestNextHint() {
	if m.ActiveExercise == nil {
		return
	}
	if m.CurrentHint < 5 {
		m.CurrentHint++
	}
	txt, ok := m.ActiveExercise.Hints[m.CurrentHint]
	if !ok || txt == "" {
		txt = fmt.Sprintf("Think carefully about data structures and invariants for Level %d.", m.CurrentHint)
	}
	if m.CurrentHint == 5 {
		refAbs := filepath.Join(m.ProjectRoot, m.ActiveExercise.ReferencePath)
		content, err := os.ReadFile(refAbs)
		if err == nil {
			txt = fmt.Sprintf("Reference Implementation:\n\n%s", string(content))
		}
	}
	m.CurrentHintTxt = txt
	m.SetStatus(fmt.Sprintf("Revealed Hint Level %d of 5", m.CurrentHint), false)
}

func (m *Model) startDrill(ex *exercise.Exercise, fresh bool) {
	if fresh {
		_, _ = cleanroom.BackupAndReset(m.ProjectRoot, ex, m.DB, ex.FunctionSignature)
	}
	sess, err := session.StartSession(m.ProjectRoot, ex.ID, "default")
	if err == nil {
		m.ActiveSession = sess
		m.ActiveExercise = ex
		m.SessionElapsed = 0
		m.LastTestReport = nil
		m.CurrentHint = 0
		m.CurrentHintTxt = ""
		m.SwitchScreen(ScreenPractice)
		m.SetStatus(fmt.Sprintf("Started drill: %s. Press 'e' to open editor.", ex.Name), false)
	}
}

func (m *Model) finalizeFinishedDrill() {
	if m.ActiveExercise == nil || m.ActiveSession == nil {
		return
	}

	var mistakeIDs []string
	for idx, checked := range m.SelectedMistakeIdxs {
		if checked && idx < len(mistakes.AllMistakes) {
			mistakeIDs = append(mistakeIDs, mistakes.AllMistakes[idx].ID)
		}
	}

	mistakesStr := strings.Join(mistakeIDs, ",")
	now := time.Now().UTC()
	durationSec := m.SessionElapsed.Seconds()
	if durationSec < 10 {
		durationSec = float64(m.ActiveExercise.RecommendedMinutes * 60)
	}

	attempt := &db.Attempt{
		ExerciseID:       m.ActiveExercise.ID,
		SessionID:        m.ActiveSession.SessionID,
		Variant:          m.ActiveSession.Variant,
		StartTime:        m.ActiveSession.StartTime,
		EndTime:          &now,
		DurationSec:      durationSec,
		Status:           "passed",
		BasicPassed:      m.ActiveSession.BasicPassed,
		HintLevelUsed:    m.CurrentHint,
		ConfidenceRating: m.ConfidenceRating,
		Mistakes:         mistakesStr,
	}

	attID, _ := m.DB.RecordAttempt(attempt)
	for _, mID := range mistakeIDs {
		_ = m.DB.LogMistake(&db.MistakeLog{
			AttemptID:  attID,
			ExerciseID: m.ActiveExercise.ID,
			Category:   m.ActiveExercise.Category,
			MistakeID:  mID,
		})
	}

	p, _ := m.DB.GetProgress(m.ActiveExercise.ID)
	scheduler.UpdateProgressOnAttempt(
		p,
		m.ActiveExercise,
		true,
		durationSec,
		m.CurrentHint,
		m.Config.Reviews.IntervalsDays,
	)
	_ = m.DB.SaveProgress(p)
	_ = session.ClearActiveSession(m.ProjectRoot)

	m.ActiveSession = nil
	m.ActiveExercise = nil
	m.RefreshData()
	m.SwitchScreen(ScreenDashboard)
	m.SetStatus("🎉 Drill completed and recorded! Progress and spaced review updated.", false)
}
