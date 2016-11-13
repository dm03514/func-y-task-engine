package task

import (
	"fmt"
	"github.com/looplab/fsm"
	"github.com/satori/go.uuid"
	"time"
)

type ITask interface {
	Run(done chan string)
	CurrentState() string
	IdString() string
}

// should write the next state and return when condition is met.
type TransitionCondition func(*Task, chan string)

// string should be the current state,
// and TransitionCondition will be a function to trigger the next state
type TransitionConditions map[string]TransitionCondition

type Task struct {
	Version      string
	FSM          *fsm.FSM `json:"-"`
	StartState   string
	FinalState   string
	TCs          TransitionConditions `json:"-"`
	Id           uuid.UUID
	EventChannel chan *TaskEvent `json:"-"`
}

// Emitted when notable task state changes occur
type TaskEvent struct {
	TaskId  uuid.UUID
	Message string
	Event   string
	Level   int
}

// Sends a message on the EventChannel
func (t *Task) Emit(message string) {
	t.EventChannel <- &TaskEvent{
		TaskId:  t.Id,
		Message: message,
	}
}

func (t *Task) IdString() string {
	return t.Id.String()
}

func (t *Task) CurrentState() string {
	return t.FSM.Current()
}

// Returns the function that will allow transition out of the current state
func (t *Task) TransitionFn() TransitionCondition {
	// get all states that could be transitioned from the current
	// state and return the TransitionCondition (if any) associated
	// with it.

	// Is reading here a race condition??
	// only a single go routine should ever be doing this
	// do we still need to protect ourselves?
	t.Emit(
		fmt.Sprintf("finding transition function for current state %q", t.FSM.Current()),
	)
	fn, ok := t.TCs[t.FSM.Current()]
	if !ok {
		panic(fmt.Sprintf(
			"TransitionFn for state '%s' not found!",
			t.FSM.Current(),
		))
	}
	return fn
}

func (t *Task) Run(done chan string) {
	t.Emit("starting_task")

	nextState := make(chan string)
	// go routine usage needs a formal plan

	// issue transition to the first state specified by the client
	go func() {
		nextState <- t.StartState
	}()

	for {
		// main loop run until the final state is not reached
		select {
		// while time is not reached
		case <-time.After(1 * time.Hour):
			t.Emit("Timeout")
			done <- t.IdString()
			return

		// and not final state
		case requestedState := <-nextState:

			t.Emit(fmt.Sprintf("state %v requested", requestedState))

			// apply the state
			t.FSM.Event(requestedState)

			// if this is end state complete
			if requestedState == t.FinalState {
				t.Emit(fmt.Sprintf("final state reached %q", t.FinalState))
				done <- t.IdString()
				// apply the finished state and update in log
				return
			}

			// get next state condition fn
			transitionFn := t.TransitionFn()

			// start polling for the next state
			go transitionFn(t, nextState)
		default:
			time.Sleep(50 * time.Millisecond)
		}
	}
}
