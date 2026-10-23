package tui

type KeyHelp struct {
	Key  string
	Desc string
}

var CommonKeys = []KeyHelp{
	{"1-8", "Switch screens directly (1: Dash, 2: Browse, 3: Details, 4: Practice, 5: Daily, 6: Reviews, 7: Stats, 8: Settings)"},
	{"Tab / Shift+Tab", "Next / Previous panel"},
	{"j / k / ↑ / ↓", "Navigate up / down"},
	{"Enter", "Select / Confirm / Drill In"},
	{"Esc", "Go back / Close overlay / Cancel search"},
	{"/", "Filter / Search exercises"},
	{"e", "Launch $EDITOR on current exercise starter file"},
	{"t", "Execute automated tests against current implementation"},
	{"h", "Request incremental hint (Levels 1-5)"},
	{"f", "Finish drill and update spaced repetition schedule"},
	{"r", "Reset starter code cleanly (safely archives previous code)"},
	{"?", "Toggle keyboard shortcuts help overlay"},
	{"q", "Quit application (or back)"},
}
