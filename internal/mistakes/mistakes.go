package mistakes

import "fmt"

type MistakeCategory struct {
	ID          string
	Name        string
	Description string
}

var AllMistakes = []MistakeCategory{
	{"base_case", "Incorrect base case", "Missing or incorrect recursion base case"},
	{"off_by_one", "Off-by-one error", "Loop indexing, slice bounds, or length check mismatch"},
	{"boundary_condition", "Incorrect boundary condition", "Empty array, zero, single node, or boundary limits"},
	{"data_structure", "Wrong data structure", "Used suboptimal or improper structure (e.g., list instead of set/deque)"},
	{"edge_direction", "Incorrect graph edge direction", "Reversed or missing directional edge in directed graph"},
	{"visited_state", "Missing visited-state handling", "Forgot to mark node visited or clear visited in backtracking"},
	{"recursion_state", "Incorrect recursion state", "Passed wrong arguments or omitted necessary state in recursion"},
	{"backtracking_undo", "Missing backtracking undo", "Failed to pop or restore state upon backtrack step"},
	{"memo_key", "Incorrect memoization key", "Incomplete cache key omitting essential state parameters"},
	{"dp_transition", "Invalid DP transition", "Incorrect recurrence relation or order of subproblem evaluation"},
	{"loop_invariant", "Incorrect loop invariant", "Binary search pointers or sliding window condition invalid"},
	{"heap_operation", "Incorrect heap operation", "Used min-heap instead of max-heap or inverted operation semantics"},
	{"python_syntax", "Python syntax/API mistake", "Standard library API misuse, mutable default arg, or scope bug"},
	{"time_complexity", "Time complexity problem", "Accidental O(N^2) instead of O(N) or redundant recomputations"},
	{"space_complexity", "Space complexity problem", "Exceeded allowed auxiliary space"},
	{"misunderstood_spec", "Misunderstood specification", "Misinterpreted requirements, constraints, or return type"},
	{"other", "Other", "Unclassified error or conceptual hurdle"},
}

var mistakesMap = func() map[string]MistakeCategory {
	m := make(map[string]MistakeCategory)
	for _, c := range AllMistakes {
		m[c.ID] = c
	}
	return m
}()

func GetMistake(id string) (MistakeCategory, bool) {
	c, ok := mistakesMap[id]
	return c, ok
}

func FormatMistakeMenu() string {
	res := "Available mistake categories:\n"
	for i, c := range AllMistakes {
		res += fmt.Sprintf("  [%2d] %-22s : %s\n", i+1, c.ID, c.Name)
	}
	return res
}
