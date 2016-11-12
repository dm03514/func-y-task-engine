package usertasks

import (
	"github.com/looplab/fsm"
	"fmt"
	"github.com/dm03514/async-states-task-engine/task"
	"github.com/satori/go.uuid"
)


// Performs two searches on google
// Completes when the second search has completed
type doubleSearchTask struct {
	task.Task
}


func (dst *doubleSearchTask) firstRequest(e *fsm.Event) {
	dst.Task.Emit(fmt.Sprintf("first Request %+v\n", e))
}

func (dst *doubleSearchTask) secondRequest(e *fsm.Event) {
	dst.Task.Emit(fmt.Sprintf("second Request %+v\n", e))
}


func NewDoubleSearchTask(events chan *task.TaskEvent) task.ITask {
	tcs := task.TransitionConditions{
		"first_request": func(t *task.Task, nextState chan string) {
			t.Emit(
				fmt.Sprintf("Executing transition 'first_request'"),
			)
			nextState <- "second"
			return
		},
		"second_request": func(t *task.Task, nextState chan string) {
			t.Emit(
				fmt.Sprintf("Executing transition 'second_request'"),
			)
			nextState <- "finished"
			return
		},
	}

	dst := &doubleSearchTask{
		task.Task{
			StartState: "first",
			FinalState: "finished",
			TCs: tcs,
			EventChannel: events,
			Id: uuid.NewV4(),
		},
	}
	dst.Task.FSM = fsm.NewFSM(
		"pending",
		fsm.Events{
			{Name: "initial", Src: []string{"unitialized"}, Dst: "pending"},
			{Name: "first", Src: []string{"pending"}, Dst: "first_request"},
			{Name: "second", Src: []string{"first_request"}, Dst: "second_request"},
			{Name: "finished", Src: []string{"second_request"}, Dst: "finished"},
		},
		fsm.Callbacks{
			"first_request": dst.firstRequest,
			"second_request": dst.secondRequest,
		},
	)
	return dst
}

