package tui

import (
	"fmt"
	"strings"

	"github.com/charmbracelet/lipgloss"
	"github.com/user/algorithm-drills/internal/mistakes"
	"github.com/user/algorithm-drills/internal/ui"
)

func (m *Model) View() string {
	if m.Width == 0 {
		m.Width = 100
	}
	if m.Height == 0 {
		m.Height = 30
	}

	// 1. Header & Navigation Tabs
	header := m.renderHeader()

	// 2. Active Screen Content
	var content string
	switch m.CurrentScreen {
	case ScreenDashboard:
		content = m.renderDashboard()
	case ScreenBrowser:
		content = m.renderBrowser()
	case ScreenDetails:
		content = m.renderDetails()
	case ScreenPractice:
		content = m.renderPractice()
	case ScreenDaily:
		content = m.renderDaily()
	case ScreenReviews:
		content = m.renderReviews()
	case ScreenAnalytics:
		content = m.renderAnalytics()
	case ScreenSettings:
		content = m.renderSettings()
	}

	// 3. Status bar & footer
	footer := m.renderFooter()

	baseView := lipgloss.JoinVertical(lipgloss.Left, header, content, footer)

	// Overlays
	if m.ShowHelpModal {
		return m.renderHelpModal(baseView)
	}
	if m.ConfirmResetModal {
		return m.renderResetModal(baseView)
	}
	if m.ShowMistakeModal {
		return m.renderMistakeModal(baseView)
	}

	return baseView
}

func (m *Model) renderHeader() string {
	var tabs []string
	for i, name := range screenNames {
		idxStr := fmt.Sprintf("%d", i+1)
		if Screen(i) == m.CurrentScreen {
			tabStyle := lipgloss.NewStyle().
				Bold(true).
				Foreground(lipgloss.Color("#FFFFFF")).
				Background(ui.ColorPrimary).
				Padding(0, 1)
			tabs = append(tabs, tabStyle.Render(fmt.Sprintf("%s %s", idxStr, name)))
		} else {
			tabStyle := lipgloss.NewStyle().
				Foreground(ui.ColorMuted).
				Padding(0, 1)
			tabs = append(tabs, tabStyle.Render(fmt.Sprintf("%s %s", idxStr, name)))
		}
	}

	tabBar := lipgloss.JoinHorizontal(lipgloss.Top, tabs...)

	title := lipgloss.NewStyle().
		Bold(true).
		Foreground(lipgloss.Color("#38BDF8")).
		Render("⚡ ALGORITHM DRILLS")

	sessionBadge := ""
	if m.ActiveSession != nil && m.ActiveExercise != nil {
		mins := int(m.SessionElapsed.Minutes())
		secs := int(m.SessionElapsed.Seconds()) % 60
		sessionBadge = lipgloss.NewStyle().
			Bold(true).
			Foreground(lipgloss.Color("#0F172A")).
			Background(ui.ColorWarning).
			Padding(0, 1).
			Render(fmt.Sprintf("ACTIVE: %s (%02d:%02d)", m.ActiveExercise.ID, mins, secs))
	}

	topRow := lipgloss.JoinHorizontal(lipgloss.Center, title, "   ", sessionBadge)
	divider := lipgloss.NewStyle().Foreground(ui.ColorSubtle).Render(strings.Repeat("─", m.Width))

	return lipgloss.JoinVertical(lipgloss.Left, topRow, tabBar, divider)
}

func (m *Model) renderFooter() string {
	divider := lipgloss.NewStyle().Foreground(ui.ColorSubtle).Render(strings.Repeat("─", m.Width))

	// Status message if present
	var statusLine string
	if m.StatusMessage != "" {
		if m.StatusIsError {
			statusLine = ui.DangerStyle.Render("✖ " + m.StatusMessage)
		} else {
			statusLine = ui.SuccessStyle.Render("✔ " + m.StatusMessage)
		}
	} else {
		statusLine = lipgloss.NewStyle().Foreground(ui.ColorMuted).Render("Ready. Navigate with j/k, select with Enter, press ? for help.")
	}

	// Shortcuts bar
	keyBar := lipgloss.NewStyle().Foreground(ui.ColorSubtle).Render(
		"[1-8] Tabs  [j/k] Move  [Enter] Select  [/] Search  [e] Edit  [t] Test  [h] Hint  [f] Finish  [?] Help  [q] Quit",
	)

	return lipgloss.JoinVertical(lipgloss.Left, divider, statusLine, keyBar)
}

func (m *Model) renderHelpModal(background string) string {
	boxWidth := 64
	var lines []string
	lines = append(lines, ui.TitleStyle.Render("KEYBOARD SHORTCUTS REFERENCE"))
	lines = append(lines, ui.Divider(boxWidth-4))

	for _, k := range CommonKeys {
		line := fmt.Sprintf(" %-18s : %s",
			lipgloss.NewStyle().Bold(true).Foreground(ui.ColorPrimary).Render(k.Key),
			k.Desc,
		)
		lines = append(lines, line)
	}

	lines = append(lines, ui.Divider(boxWidth-4))
	lines = append(lines, lipgloss.NewStyle().Foreground(ui.ColorMuted).Render("Press ? or Esc to close"))

	boxContent := lipgloss.JoinVertical(lipgloss.Left, lines...)
	modal := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(ui.ColorPrimary).
		Background(lipgloss.Color("#0F172A")).
		Padding(1, 2).
		Width(boxWidth).
		Render(boxContent)

	return lipgloss.Place(m.Width, m.Height, lipgloss.Center, lipgloss.Center, modal)
}

func (m *Model) renderResetModal(background string) string {
	exName := "current exercise"
	if m.SelectedExercise != nil {
		exName = m.SelectedExercise.Name
	}
	content := fmt.Sprintf(
		"%s\n%s\n"+
			"Are you sure you want to reset starter code for:\n"+
			"  %s\n\n"+
			"Your existing code will be safely backed up to .drills/backups/\n"+
			"and can be restored at any time with 'drills recover'.\n\n"+
			"[Y] Confirm Reset   [N/Esc] Cancel",
		ui.WarningStyle.Render("CONFIRM CLEAN-ROOM RESET"),
		ui.Divider(55),
		lipgloss.NewStyle().Bold(true).Foreground(ui.ColorPrimary).Render(exName),
	)

	modal := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(ui.ColorWarning).
		Background(lipgloss.Color("#0F172A")).
		Padding(1, 2).
		Width(60).
		Render(content)

	return lipgloss.Place(m.Width, m.Height, lipgloss.Center, lipgloss.Center, modal)
}

func (m *Model) renderMistakeModal(background string) string {
	boxWidth := 70
	var lines []string
	lines = append(lines, ui.TitleStyle.Render("FINISH DRILL — LOG HURDLES & CONFIDENCE"))
	lines = append(lines, ui.Divider(boxWidth-4))
	lines = append(lines, fmt.Sprintf("Confidence Rating: %d / 5 (Press 1-5 to adjust)", m.ConfidenceRating))
	lines = append(lines, "Identify any mistakes encountered (Space to toggle, Enter to confirm):")
	lines = append(lines, "")

	for i, mis := range mistakes.AllMistakes {
		cursor := "  "
		if i == m.MistakeCursorIdx {
			cursor = lipgloss.NewStyle().Foreground(ui.ColorPrimary).Render("▶ ")
		}
		checked := "[ ]"
		if m.SelectedMistakeIdxs[i] {
			checked = ui.SuccessStyle.Render("[✔]")
		}
		lines = append(lines, fmt.Sprintf("%s%s %-24s : %s", cursor, checked, mis.Name, mis.Description))
		if i >= 12 { // Limit displayed items in modal
			break
		}
	}

	lines = append(lines, ui.Divider(boxWidth-4))
	lines = append(lines, "[Enter] Save & Finish Attempt    [Esc] Cancel")

	modal := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(ui.ColorSuccess).
		Background(lipgloss.Color("#0F172A")).
		Padding(1, 2).
		Width(boxWidth).
		Render(lipgloss.JoinVertical(lipgloss.Left, lines...))

	return lipgloss.Place(m.Width, m.Height, lipgloss.Center, lipgloss.Center, modal)
}
