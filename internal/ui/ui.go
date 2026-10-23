package ui

import (
	"fmt"
	"strings"

	"github.com/charmbracelet/lipgloss"
)

var (
	// Colors
	ColorPrimary   = lipgloss.Color("#38BDF8") // Sky blue
	ColorSecondary = lipgloss.Color("#818CF8") // Indigo
	ColorSuccess   = lipgloss.Color("#34D399") // Emerald green
	ColorWarning   = lipgloss.Color("#FBBF24") // Amber
	ColorDanger    = lipgloss.Color("#F87171") // Coral red
	ColorMuted     = lipgloss.Color("#94A3B8") // Slate
	ColorSubtle    = lipgloss.Color("#475569") // Dark slate
	ColorBg        = lipgloss.Color("#0F172A") // Deep navy

	// Styles
	TitleStyle = lipgloss.NewStyle().
			Bold(true).
			Foreground(ColorPrimary).
			MarginBottom(1)

	HeaderStyle = lipgloss.NewStyle().
			Bold(true).
			Foreground(lipgloss.Color("#F8FAFC")).
			Background(ColorSecondary).
			Padding(0, 1)

	CardStyle = lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			BorderForeground(ColorPrimary).
			Padding(1, 2).
			MarginBottom(1)

	SuccessStyle = lipgloss.NewStyle().
			Bold(true).
			Foreground(ColorSuccess)

	WarningStyle = lipgloss.NewStyle().
			Bold(true).
			Foreground(ColorWarning)

	DangerStyle = lipgloss.NewStyle().
			Bold(true).
			Foreground(ColorDanger)

	MutedStyle = lipgloss.NewStyle().
			Foreground(ColorMuted)

	BadgeStyle = lipgloss.NewStyle().
			Bold(true).
			Foreground(lipgloss.Color("#FFFFFF")).
			Padding(0, 1)
)

func DifficultyBadge(diff string) string {
	switch strings.ToLower(diff) {
	case "easy":
		return BadgeStyle.Background(lipgloss.Color("#059669")).Render("EASY")
	case "medium":
		return BadgeStyle.Background(lipgloss.Color("#D97706")).Render("MEDIUM")
	case "hard":
		return BadgeStyle.Background(lipgloss.Color("#DC2626")).Render("HARD")
	default:
		return BadgeStyle.Background(ColorSubtle).Render(strings.ToUpper(diff))
	}
}

func MasteryBadge(level int) string {
	switch level {
	case 1:
		return lipgloss.NewStyle().Foreground(ColorMuted).Render("⚪ Not Started")
	case 2:
		return lipgloss.NewStyle().Foreground(lipgloss.Color("#60A5FA")).Render("🔵 Learning")
	case 3:
		return lipgloss.NewStyle().Foreground(lipgloss.Color("#FBBF24")).Render("🟡 Improving")
	case 4:
		return lipgloss.NewStyle().Foreground(lipgloss.Color("#34D399")).Render("🟢 Proficient")
	case 5:
		return lipgloss.NewStyle().Foreground(lipgloss.Color("#A855F7")).Bold(true).Render("⭐ Mastered")
	default:
		return lipgloss.NewStyle().Foreground(ColorMuted).Render("⚪ Not Started")
	}
}

func ProgressBar(completed, total int, width int) string {
	if total <= 0 {
		return strings.Repeat("░", width)
	}
	ratio := float64(completed) / float64(total)
	if ratio > 1.0 {
		ratio = 1.0
	}
	filledLen := int(ratio * float64(width))
	emptyLen := width - filledLen

	filled := lipgloss.NewStyle().Foreground(ColorSuccess).Render(strings.Repeat("█", filledLen))
	empty := lipgloss.NewStyle().Foreground(ColorSubtle).Render(strings.Repeat("░", emptyLen))
	percent := int(ratio * 100)

	return fmt.Sprintf("%s%s %3d%% (%d/%d)", filled, empty, percent, completed, total)
}

func Divider(width int) string {
	if width <= 0 {
		width = 60
	}
	return lipgloss.NewStyle().Foreground(ColorSubtle).Render(strings.Repeat("─", width))
}
