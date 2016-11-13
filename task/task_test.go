package task

import (
	"fmt"
	"github.com/looplab/fsm"
	"testing"
)

func TestTaskTransitionConditionNoCondition(t *testing.T) {
	defer func() {
		if r := recover(); r != nil {
			var ok bool
			err, ok := r.(error)
			if !ok {
				err = fmt.Errorf("pkg: %v", r)
				fmt.Println(err)
			}
		}
	}()
	events := fsm.Events{
		{Name: "pending", Src: []string{}, Dst: "finished"},
		{Name: "finished", Src: []string{"pending"}, Dst: "finished"},
	}

	task := &Task{
		FSM: fsm.NewFSM(
			"pending",
			events,
			fsm.Callbacks{},
		),
		TCs: TransitionConditions{},
	}
	task.TransitionFn()
}

// Checks that
// given a current state
func TestTaskTransitionConditionSingleCondition(t *testing.T) {
	fn := func(nextState chan string) {
		nextState <- "next_state"
	}

	tcs := TransitionConditions{"pending": fn}
	events := fsm.Events{
		{Name: "pending", Src: []string{}, Dst: "finished"},
		{Name: "finished", Src: []string{"pending"}, Dst: "finished"},
	}

	task := &Task{
		FSM: fsm.NewFSM(
			"pending",
			events,
			fsm.Callbacks{},
		),
		TCs: tcs,
	}

	transitionConditionFn := task.TransitionFn()
	nextState := make(chan string)
	go transitionConditionFn(nextState)
	expectedResp := <-nextState

	if expectedResp != "next_state" {
		t.Error(fmt.Printf(
			"Expected 'correct_function' recieved %s",
			expectedResp,
		))
	}
}
