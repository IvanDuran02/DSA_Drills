package scheduler

import (
	"sort"
	"strings"
	"time"

	"github.com/user/algorithm-drills/internal/db"
	"github.com/user/algorithm-drills/internal/exercise"
)

type ScheduledItem struct {
	Exercise           *exercise.Exercise
	Reason             string // "Due review", "Weak area", "Focus", "New", "Retention"
	EstimatedMinutes   int
	MasteryLevel       int
	DaysOverdue        int
}

type DailyPlan struct {
	TotalMinutes   int
	TargetMinutes  int
	Items          []ScheduledItem
}

// Category interview importance weights
var categoryWeights = map[string]int{
	"graphs":              10,
	"trees":               10,
	"binary_search":        9,
	"heaps":                9,
	"sliding_window":       9,
	"backtracking":         8,
	"dynamic_programming":  8,
	"stacks":               7,
	"linked_lists":         7,
}

func UpdateProgressOnAttempt(
	p *db.ExerciseProgress,
	ex *exercise.Exercise,
	passed bool,
	durationSec float64,
	hintsUsed int,
	intervals []int,
) {
	now := time.Now().UTC()
	p.TotalAttempts++
	p.UpdatedAt = now

	// Check if already practiced today (UTC date)
	alreadyPracticedToday := false
	if p.LastPracticeAt != nil {
		y1, m1, d1 := p.LastPracticeAt.UTC().Date()
		y2, m2, d2 := now.Date()
		if y1 == y2 && m1 == m2 && d1 == d2 {
			alreadyPracticedToday = true
		}
	}
	p.LastPracticeAt = &now

	if !passed {
		// Failed attempt: review tomorrow, reset streak
		p.Streak = 0
		p.IntervalDays = 1
		next := now.Add(24 * time.Hour)
		p.NextReviewAt = &next
		if p.MasteryLevel == 0 {
			p.MasteryLevel = 1
		}
		return
	}

	// Passed attempt
	p.SuccessfulAttempts++
	if p.TotalAttempts == 1 {
		p.FirstAttemptSuccess = true
	}
	p.TotalHintsUsed += hintsUsed

	// Update average and best completion times
	if p.BestCompletionTimeSec == 0 || durationSec < p.BestCompletionTimeSec {
		p.BestCompletionTimeSec = durationSec
	}
	if p.AvgCompletionTimeSec == 0 {
		p.AvgCompletionTimeSec = durationSec
	} else {
		p.AvgCompletionTimeSec = (p.AvgCompletionTimeSec*float64(p.SuccessfulAttempts-1) + durationSec) / float64(p.SuccessfulAttempts)
	}

	// Only advance interval and streak if this is the first success today
	if !alreadyPracticedToday {
		p.Streak++

		if hintsUsed >= 3 {
			// Significant hints: review in 1 day
			p.IntervalDays = 1
		} else if durationSec > float64(ex.RecommendedMinutes*60*2) {
			// Significantly slow: short interval
			p.IntervalDays = 1
		} else {
			// Normal or fast independent success: advance interval
			currentIdx := -1
			for i, val := range intervals {
				if p.IntervalDays <= val {
					currentIdx = i
					break
				}
			}
			if currentIdx == -1 || currentIdx >= len(intervals)-1 {
				p.IntervalDays = p.IntervalDays * 2
				if p.IntervalDays > 90 {
					p.IntervalDays = 90
				}
			} else {
				p.IntervalDays = intervals[currentIdx+1]
			}
		}
	}

	next := now.Add(time.Duration(p.IntervalDays) * 24 * time.Hour)
	p.NextReviewAt = &next

	// Recalculate Mastery Level:
	// 1: Not Started
	// 2: Learning (1 success)
	// 3: Improving (2+ successes)
	// 4: Proficient (3+ successes, streak >= 2, avg time <= 1.5x recommended)
	// 5: Mastered (4+ successes, streak >= 3, best time <= recommended, hints <= 1)
	recommendedSec := float64(ex.RecommendedMinutes * 60)
	if p.SuccessfulAttempts >= 4 && p.Streak >= 3 && p.BestCompletionTimeSec <= recommendedSec && p.TotalHintsUsed <= 1 {
		p.MasteryLevel = 5 // Mastered
	} else if p.SuccessfulAttempts >= 3 && p.Streak >= 2 && p.AvgCompletionTimeSec <= recommendedSec*1.5 {
		p.MasteryLevel = 4 // Proficient
	} else if p.SuccessfulAttempts >= 2 {
		p.MasteryLevel = 3 // Improving
	} else if p.SuccessfulAttempts >= 1 {
		p.MasteryLevel = 2 // Learning
	} else {
		p.MasteryLevel = 1 // Not Started
	}
}

func GenerateDailyTraining(
	registry *exercise.ExerciseRegistry,
	progressMap map[string]*db.ExerciseProgress,
	mistakesMap map[string]int,
	targetMinutes int,
	focusCategory string,
) *DailyPlan {
	if targetMinutes <= 0 {
		targetMinutes = 60
	}

	now := time.Now().UTC()
	var overdueItems []ScheduledItem
	var weakItems []ScheduledItem
	var focusItems []ScheduledItem
	var newItems []ScheduledItem
	var retentionItems []ScheduledItem

	usedIDs := make(map[string]bool)

	allExercises := registry.All()

	for _, ex := range allExercises {
		p, exists := progressMap[ex.ID]
		estMin := ex.RecommendedMinutes
		if estMin <= 0 {
			estMin = 10
		}

		if focusCategory != "" && strings.EqualFold(ex.Category, focusCategory) {
			focusItems = append(focusItems, ScheduledItem{
				Exercise:         ex,
				Reason:           "Focus category",
				EstimatedMinutes: estMin,
				MasteryLevel:     pMastery(p),
			})
			continue
		}

		if !exists || p.TotalAttempts == 0 {
			newItems = append(newItems, ScheduledItem{
				Exercise:         ex,
				Reason:           "New",
				EstimatedMinutes: estMin,
				MasteryLevel:     1,
			})
			continue
		}

		// Check overdue
		if p.NextReviewAt != nil && now.After(*p.NextReviewAt) {
			daysOverdue := int(now.Sub(*p.NextReviewAt).Hours() / 24)
			overdueItems = append(overdueItems, ScheduledItem{
				Exercise:         ex,
				Reason:           "Due review",
				EstimatedMinutes: estMin,
				MasteryLevel:     p.MasteryLevel,
				DaysOverdue:      daysOverdue,
			})
			continue
		}

		// Weak area check: mastery <= 2 with attempts > 0 or mistakes logged
		if p.MasteryLevel <= 2 && p.TotalAttempts > 0 {
			weakItems = append(weakItems, ScheduledItem{
				Exercise:         ex,
				Reason:           "Weak area",
				EstimatedMinutes: estMin,
				MasteryLevel:     p.MasteryLevel,
			})
			continue
		}

		// Retention check: mastery >= 4
		retentionItems = append(retentionItems, ScheduledItem{
			Exercise:         ex,
			Reason:           "Retention",
			EstimatedMinutes: estMin,
			MasteryLevel:     p.MasteryLevel,
		})
	}

	// Sort overdue by days overdue descending
	sort.Slice(overdueItems, func(i, j int) bool {
		return overdueItems[i].DaysOverdue > overdueItems[j].DaysOverdue
	})

	// Sort new items by category interview weight descending
	sort.Slice(newItems, func(i, j int) bool {
		w1 := categoryWeights[newItems[i].Exercise.Category]
		w2 := categoryWeights[newItems[j].Exercise.Category]
		if w1 != w2 {
			return w1 > w2
		}
		return newItems[i].Exercise.Level < newItems[j].Exercise.Level
	})

	plan := &DailyPlan{
		TargetMinutes: targetMinutes,
		Items:         make([]ScheduledItem, 0),
	}
	currentMin := 0

	addItem := func(item ScheduledItem) bool {
		if usedIDs[item.Exercise.ID] {
			return false
		}
		if currentMin+item.EstimatedMinutes > targetMinutes && currentMin > 0 {
			return false
		}
		usedIDs[item.Exercise.ID] = true
		plan.Items = append(plan.Items, item)
		currentMin += item.EstimatedMinutes
		return true
	}

	// 1. Focus category if provided
	for _, it := range focusItems {
		if currentMin >= targetMinutes {
			break
		}
		addItem(it)
	}

	// 2. Overdue reviews
	for _, it := range overdueItems {
		if currentMin >= targetMinutes {
			break
		}
		addItem(it)
	}

	// 3. Weak areas
	for _, it := range weakItems {
		if currentMin >= targetMinutes {
			break
		}
		addItem(it)
	}

	// 4. New exercises
	for _, it := range newItems {
		if currentMin >= targetMinutes {
			break
		}
		addItem(it)
	}

	// 5. Retention
	for _, it := range retentionItems {
		if currentMin >= targetMinutes {
			break
		}
		addItem(it)
	}

	plan.TotalMinutes = currentMin
	return plan
}

func pMastery(p *db.ExerciseProgress) int {
	if p == nil {
		return 1
	}
	return p.MasteryLevel
}
